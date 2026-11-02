# ac-minecraft: RCON bridge for the AC Worlds server

Lets Claude Code (or any MCP client) run commands on a local Paper server and
read the replies, instead of typing into the game.

## Layout on this Mac

```
~/minecraft-server/
  paper.jar          Paper 26.3 (downloaded from fill.papermc.io, sha256-checked)
  server.properties  RCON on 127.0.0.1:25575, creative, peaceful, level-name=Animus
  rcon.env           RCON_HOST / RCON_PORT / RCON_PASSWORD (mode 600, never committed)
  start.sh           runs the server with the launcher's bundled Java 25
  Animus/            a COPY of the singleplayer world, with datapacks/ac_worlds.zip
  logs/latest.log    the server log (unlike the client's, this one is reliable)
```

## Start / stop

```bash
~/minecraft-server/start.sh            # foreground; Ctrl-C or `stop` in the console
```

Join from the game: Multiplayer > Direct Connect > `127.0.0.1`. The server's
Animus and the singleplayer Animus are separate worlds from now on.

## The MCP server

`server.py` exposes six tools over stdio: `run_command`, `probe_block`,
`place_build`, `player_pos`, `list_players`, `tail_log`. Registered for Claude
Code under the name `ac-minecraft` (user scope, in `~/.claude.json`); to add it
by hand:

```bash
claude mcp add ac-minecraft -- python3 /Users/wari/industry-knowledge-base/minecraft/rcon_bridge/server.py
```

Dependencies: `pip install --user mcp mctools`. Smoke test without an MCP client:

```bash
python3 minecraft/rcon_bridge/server.py --test
```

Unit tests (no server needed): `python3 -m unittest discover -s minecraft/rcon_bridge -q`.

## RCON gotchas baked into the bridge

- Commands over ~1446 bytes are refused; put long work in a datapack function.
- Many commands reply with nothing. `place_build` and `run_command` say so;
  follow mutations with `probe_block`.
- `place_build` runs `ac:raw/<world>/<build>` as the console (the player-facing
  `ac:<world>/<build>` functions need a player for `@s`), force-loading
  512 x 512 blocks around the origin first.
- Colour codes (`§x`) are stripped from replies.
