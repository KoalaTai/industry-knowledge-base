#!/usr/bin/env python3
"""ac-minecraft: an MCP server that drives a local Minecraft Java server over RCON.

Tools (all return plain text):

    run_command(cmd)                  any console command, response text back
    probe_block(x, y, z, block)       True if the block at x y z is `block` (execute if block)
    place_build(function_id, x, y, z) force-load around x z, run ac:raw/<function_id> there, release
    player_pos(name)                  a player's position and rotation
    list_players()                    who is online
    tail_log(n)                       last n lines of the server's logs/latest.log

Configuration comes from ``~/minecraft-server/rcon.env`` (RCON_HOST, RCON_PORT,
RCON_PASSWORD) or the environment; the server root can be overridden with
AC_SERVER_DIR.  Run it directly for a smoke test:

    python3 server.py --test            # connects, runs /list, prints the reply

RCON notes (why this file looks the way it does): outbound payloads are capped
at ~1446 bytes, responses are fragmented at 4096 bytes, and many commands
return nothing at all, so every mutation should be followed by a probe.
mctools handles the fragmentation; we strip Minecraft's section-sign colour
codes ourselves.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

SERVER_DIR = Path(os.environ.get("AC_SERVER_DIR", Path.home() / "minecraft-server"))
ENV_FILE = SERVER_DIR / "rcon.env"
MAX_PAYLOAD = 1446
_COLOR = re.compile("§.|\x1b\\[[0-9;]*m")     # Minecraft section-sign codes and Paper's ANSI colours


def load_env() -> dict:
    cfg = {"RCON_HOST": "127.0.0.1", "RCON_PORT": "25575", "RCON_PASSWORD": ""}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    for k in cfg:
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


class Rcon:
    """Thin wrapper around mctools.RCONClient with reconnect and colour stripping."""

    def __init__(self, host: str, port: int, password: str) -> None:
        self.host, self.port, self.password = host, port, password
        self._client = None

    def _connect(self):
        from mctools import RCONClient  # imported lazily so tests can mock it
        client = RCONClient(self.host, port=self.port, timeout=20)
        if not client.login(self.password):
            raise RuntimeError("RCON login failed (check rcon.env and server.properties)")
        return client

    def command(self, cmd: str) -> str:
        cmd = cmd.lstrip("/")
        if len(cmd.encode("utf-8")) > MAX_PAYLOAD:
            raise ValueError(f"command is {len(cmd)} bytes; RCON accepts at most {MAX_PAYLOAD}. "
                             "Put long work in a datapack function and call it.")
        for attempt in (1, 2):
            try:
                if self._client is None:
                    self._client = self._connect()
                return _COLOR.sub("", self._client.command(cmd) or "")
            except Exception:
                self._client = None
                if attempt == 2:
                    raise
                time.sleep(0.5)
        return ""


_rcon: Optional[Rcon] = None


def rcon() -> Rcon:
    global _rcon
    if _rcon is None:
        cfg = load_env()
        if not cfg["RCON_PASSWORD"]:
            raise RuntimeError(f"no RCON_PASSWORD in {ENV_FILE} or the environment")
        _rcon = Rcon(cfg["RCON_HOST"], int(cfg["RCON_PORT"]), cfg["RCON_PASSWORD"])
    return _rcon


# ------------------------------------------------------------------ tool bodies
def run_command(cmd: str) -> str:
    """Run one console command and return its response text ('' when the command prints nothing)."""
    out = rcon().command(cmd)
    return out if out else "(no output)"


def probe_block(x: int, y: int, z: int, block: str = "minecraft:air") -> str:
    """Check the block at x y z: returns 'yes' / 'no' plus the raw response."""
    if ":" not in block:
        block = "minecraft:" + block
    out = rcon().command(f"execute if block {x} {y} {z} {block}")
    low = out.lower()
    if "not loaded" in low:
        verdict = "unknown"                      # chunk not loaded: forceload it first
    elif "passed" in low:
        verdict = "yes"
    elif "failed" in low:
        verdict = "no"
    else:
        verdict = "unknown"
    return verdict + f" ({out.strip() or 'no output'})"


LOAD_RADIUS = 120        # 240x240 blocks: at most 16x16 chunks whatever the alignment (256 would straddle 17)


def _forceload(verb: str, x: int, z: int, radius: int = LOAD_RADIUS) -> str:
    return rcon().command(f"forceload {verb} {x - radius} {z - radius} {x + radius - 1} {z + radius - 1}")


def _wait_loaded(x: int, y: int, z: int, radius: int = LOAD_RADIUS, timeout: float = 15.0) -> bool:
    """Chunk loading is asynchronous: poll `execute if loaded` at the area's corners and centre."""
    corners = [(x, z), (x - radius, z - radius), (x + radius - 1, z - radius),
               (x - radius, z + radius - 1), (x + radius - 1, z + radius - 1)]
    deadline = time.time() + timeout
    while time.time() < deadline:
        if all("passed" in rcon().command(f"execute if loaded {cx} {y} {cz}").lower() for cx, cz in corners):
            return True
        time.sleep(0.5)
    return False


def place_build(function_id: str, x: int, y: int, z: int) -> str:
    """Place one AC Worlds build (e.g. 'egypt/giza' or 'tech/aqueduct') with its origin at x y z.

    Runs the raw placement function ac:raw/<function_id> from the console after
    force-loading a 256x256-block area around the origin and waiting until it is
    actually loaded (fill and place template silently skip unloaded chunks).
    Builds wider than that need a second call or a manual forceload.
    """
    fid = function_id.strip().lstrip("/").removeprefix("ac:").removeprefix("raw/")
    _forceload("add", x, z)
    if not _wait_loaded(x, y, z):
        _forceload("remove", x, z)
        return "chunks around the origin did not load within 15 s; nothing placed"
    out = rcon().command(f"execute positioned {x} {y} {z} run function ac:raw/{fid}")
    _forceload("remove", x, z)
    return out.strip() or f"ran ac:raw/{fid} at {x} {y} {z} (no output; verify with probe_block)"


def player_pos(name: str) -> str:
    """Position and rotation of an online player."""
    pos = rcon().command(f"data get entity {name} Pos")
    rot = rcon().command(f"data get entity {name} Rotation")
    return f"{pos.strip()}\n{rot.strip()}"


def list_players() -> str:
    return rcon().command("list").strip() or "(no output)"


def tail_log(n: int = 40) -> str:
    """Last n lines of the server log."""
    log = SERVER_DIR / "logs" / "latest.log"
    if not log.exists():
        return f"no log at {log}"
    lines = log.read_text(errors="replace").splitlines()
    return "\n".join(lines[-max(1, min(n, 500)):])


# ------------------------------------------------------------------ MCP wiring
def build_server():
    from mcp.server.fastmcp import FastMCP
    srv = FastMCP("ac-minecraft", instructions=(
        "Drives the local AC Worlds Paper server over RCON. Many commands return no text; "
        "after fill/setblock/function calls verify with probe_block. Keep commands short; "
        "long work belongs in datapack functions (ac:raw/<world>/<build>)."))
    srv.tool()(run_command)
    srv.tool()(probe_block)
    srv.tool()(place_build)
    srv.tool()(player_pos)
    srv.tool()(list_players)
    srv.tool()(tail_log)
    return srv


def main() -> None:
    if "--test" in sys.argv:
        print(list_players())
        print(run_command("function ac:help"))
        return
    build_server().run(transport="stdio")


if __name__ == "__main__":
    main()
