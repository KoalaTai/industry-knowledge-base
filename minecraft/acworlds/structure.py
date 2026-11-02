"""Vanilla structure templates (``.nbt``) from a Voxel, standard library only.

A structure template is a gzipped NBT compound::

    {DataVersion: int, size: [sx, sy, sz], palette: [{id, properties}],
     blocks: [{pos: [x, y, z], state: int}], entities: []}

Palette keys are the 26.x spelling (``id`` / ``properties``, DataVersion
5023).  Up to 1.21.x the keys were ``Name`` / ``Properties``; a 26.3 game
reads those as missing and silently places air for every entry, which is
how this was found.  Use ``--placement commands`` for pre-26 versions.

Minecraft caps templates at 48 blocks per axis, so a build is tiled into
<= 48x48x48 cubes and each tile is placed with one ``/place template``
command.  Air is kept as an explicit palette entry so carved rooms still
carve into existing terrain; positions a build never touched are left
alone.

Big axis-aligned slabs stay as ``/fill`` commands (one command for a
101x101 floor beats 10,201 template entries); everything smaller goes into
the templates.  Blocks that need support (torches, panes, carpets ...) go
into a second "late" template per tile that is placed after every solid
tile, so a torch never arrives before the wall it hangs on.
"""

from __future__ import annotations

import gzip
import struct
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .export import _phase, _rel, mesh
from .voxel import Coord, Voxel

DATA_VERSION = 5023      # Minecraft Java 26.3
TILE = 48                # vanilla per-axis template limit
FILL_THRESHOLD = 512     # boxes with at least this many blocks stay /fill commands
# Measured over all 119 builds (8.6M blocks, 151k greedy boxes): at 512 about
# 1,900 boxes stay as /fill and 2.8M blocks move into templates, which with
# ~1,500 tiles gives ~3,500 placement commands instead of 151,000.

# ----------------------------------------------------------------- NBT (subset)
_END, _BYTE, _SHORT, _INT, _LONG, _FLOAT, _DOUBLE, _BYTE_ARRAY, _STRING, _LIST, _COMPOUND, _INT_ARRAY, _LONG_ARRAY = range(13)


def _tag_type(v) -> int:
    if isinstance(v, dict):
        return _COMPOUND
    if isinstance(v, list):
        return _LIST
    if isinstance(v, str):
        return _STRING
    if isinstance(v, bool):
        raise TypeError("bool is ambiguous in NBT; use int")
    if isinstance(v, int):
        return _INT
    raise TypeError(f"unsupported NBT value: {v!r}")


def _w_str(s: str) -> bytes:
    b = s.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def _payload(v) -> bytes:
    t = _tag_type(v)
    if t == _COMPOUND:
        return b"".join(bytes([_tag_type(x)]) + _w_str(k) + _payload(x) for k, x in v.items()) + b"\x00"
    if t == _LIST:
        et = _tag_type(v[0]) if v else _END
        return struct.pack(">bi", et, len(v)) + b"".join(_payload(x) for x in v)
    if t == _STRING:
        return _w_str(v)
    return struct.pack(">i", v)


def dumps(root: dict, name: str = "") -> bytes:
    """Serialise a dict (int / str / list / dict values) as an NBT compound."""
    return bytes([_COMPOUND]) + _w_str(name) + _payload(root)


def _read(buf: bytes, pos: int, t: int):
    if t == _BYTE:
        return buf[pos], pos + 1
    if t == _SHORT:
        return struct.unpack_from(">h", buf, pos)[0], pos + 2
    if t == _INT:
        return struct.unpack_from(">i", buf, pos)[0], pos + 4
    if t == _LONG:
        return struct.unpack_from(">q", buf, pos)[0], pos + 8
    if t == _FLOAT:
        return struct.unpack_from(">f", buf, pos)[0], pos + 4
    if t == _DOUBLE:
        return struct.unpack_from(">d", buf, pos)[0], pos + 8
    if t == _BYTE_ARRAY:
        n = struct.unpack_from(">i", buf, pos)[0]
        return list(buf[pos + 4:pos + 4 + n]), pos + 4 + n
    if t == _STRING:
        n = struct.unpack_from(">H", buf, pos)[0]
        return buf[pos + 2:pos + 2 + n].decode("utf-8"), pos + 2 + n
    if t == _LIST:
        et, n = struct.unpack_from(">bi", buf, pos)
        pos += 5
        out = []
        for _ in range(n):
            v, pos = _read(buf, pos, et)
            out.append(v)
        return out, pos
    if t == _COMPOUND:
        out = {}
        while True:
            et = buf[pos]
            pos += 1
            if et == _END:
                return out, pos
            n = struct.unpack_from(">H", buf, pos)[0]
            key = buf[pos + 2:pos + 2 + n].decode("utf-8")
            v, pos = _read(buf, pos + 2 + n, et)
            out[key] = v
    if t in (_INT_ARRAY, _LONG_ARRAY):
        n = struct.unpack_from(">i", buf, pos)[0]
        w = 4 if t == _INT_ARRAY else 8
        fmt = ">%d%s" % (n, "i" if t == _INT_ARRAY else "q")
        return list(struct.unpack_from(fmt, buf, pos + 4)), pos + 4 + n * w
    raise ValueError(f"bad tag type {t}")


def loads(data: bytes) -> dict:
    """Parse an (uncompressed) NBT compound; the root name is dropped."""
    if data[0] != _COMPOUND:
        raise ValueError("root is not a compound")
    n = struct.unpack_from(">H", data, 1)[0]
    root, _ = _read(data, 3 + n, _COMPOUND)
    return root


def write_template(path: str, nbt: dict) -> None:
    with gzip.open(path, "wb") as f:
        f.write(dumps(nbt))


def read_template(path: str) -> dict:
    with gzip.open(path, "rb") as f:
        return loads(f.read())


# ----------------------------------------------------------------- templates
def parse_state(block: str) -> Tuple[str, Dict[str, str]]:
    """'minecraft:oak_leaves[persistent=true]' -> ('minecraft:oak_leaves', {'persistent': 'true'})."""
    name, _, rest = block.partition("[")
    props: Dict[str, str] = {}
    if rest:
        for kv in rest.rstrip("]").split(","):
            k, v = kv.split("=", 1)
            props[k] = v
    return name, props


def template_nbt(blocks: Dict[Coord, str], origin: Coord) -> dict:
    """Build the template compound for ``blocks`` whose min corner is ``origin``."""
    ox, oy, oz = origin
    palette: List[dict] = []
    index: Dict[str, int] = {}
    entries = []
    for (x, y, z), b in sorted(blocks.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0])):
        if b not in index:
            name, props = parse_state(b)
            entry = {"id": name}
            if props:
                entry["properties"] = props
            index[b] = len(palette)
            palette.append(entry)
        entries.append({"pos": [x - ox, y - oy, z - oz], "state": index[b]})
    xs = [c[0] for c in blocks]
    ys = [c[1] for c in blocks]
    zs = [c[2] for c in blocks]
    size = [max(xs) - ox + 1, max(ys) - oy + 1, max(zs) - oz + 1]
    if max(size) > TILE:
        raise ValueError(f"template exceeds {TILE} blocks per axis: {size}")
    return {"DataVersion": DATA_VERSION, "size": size, "palette": palette, "blocks": entries, "entities": []}


def blocks_from_template(nbt: dict, origin: Coord) -> Dict[Coord, str]:
    """Inverse of template_nbt (for tests and tooling)."""
    ox, oy, oz = origin
    pal = []
    for e in nbt["palette"]:
        props = e.get("properties", e.get("Properties", {}))          # accept both spellings when reading
        name = e.get("id", e.get("Name"))
        pal.append(name + ("[" + ",".join(f"{k}={v}" for k, v in props.items()) + "]" if props else ""))
    return {(p["pos"][0] + ox, p["pos"][1] + oy, p["pos"][2] + oz): pal[p["state"]] for p in nbt["blocks"]}


def tile(blocks: Dict[Coord, str], size: int = TILE) -> List[Tuple[Tuple[int, int, int], Coord, Dict[Coord, str]]]:
    """Split a sparse block dict into <= size^3 cells.

    Returns ``[(cell_index, origin, blocks)]`` where ``origin`` is the min
    corner of the blocks actually present in that cell (so ``pos`` values
    stay small and placement is exact).
    """
    if not blocks:
        return []
    x1 = min(c[0] for c in blocks)
    y1 = min(c[1] for c in blocks)
    z1 = min(c[2] for c in blocks)
    cells: Dict[Tuple[int, int, int], Dict[Coord, str]] = {}
    for (x, y, z), b in blocks.items():
        key = ((x - x1) // size, (y - y1) // size, (z - z1) // size)
        cells.setdefault(key, {})[(x, y, z)] = b
    out = []
    for key in sorted(cells):
        cb = cells[key]
        origin = (min(c[0] for c in cb), min(c[1] for c in cb), min(c[2] for c in cb))
        out.append((key, origin, cb))
    return out


@dataclass
class Template:
    name: str                 # template id suffix, e.g. "s0_0_1" (solid) / "l0_0_1" (late)
    origin: Coord             # where its min corner goes, relative to the build origin
    nbt: dict


@dataclass
class Plan:
    """What it takes to place one build: big fills, then templates, then the rest."""
    fills: List[str] = field(default_factory=list)        # /fill for large solid or air boxes
    templates: List[Template] = field(default_factory=list)
    late_fills: List[str] = field(default_factory=list)   # large boxes of support-needing blocks (rare)

    def commands(self, template_id_prefix: str) -> List[str]:
        """Placement commands in the right order.  ``template_id_prefix`` is e.g. 'ac:egypt/giza'."""
        out = list(self.fills)
        for t in sorted(self.templates, key=lambda t: t.name.startswith("l")):
            ox, oy, oz = t.origin
            out.append(f"place template {template_id_prefix}/{t.name} {_rel(ox)} {_rel(oy)} {_rel(oz)}")
        out.extend(self.late_fills)
        return out

    @property
    def command_count(self) -> int:
        return len(self.fills) + len(self.templates) + len(self.late_fills)


def build_plan(v: Voxel, fill_threshold: int = FILL_THRESHOLD) -> Plan:
    """Greedy-mesh the voxel; big boxes become /fill, small ones become templates."""
    plan = Plan()
    small: Dict[Coord, str] = {}
    late: Dict[Coord, str] = {}
    for x1, y1, z1, x2, y2, z2, b in mesh(v):
        vol = (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
        phase = _phase(b)
        if vol >= fill_threshold:
            cmd = f"fill {_rel(x1)} {_rel(y1)} {_rel(z1)} {_rel(x2)} {_rel(y2)} {_rel(z2)} {b}"
            (plan.late_fills if phase == 1 else plan.fills).append(cmd)
            continue
        target = late if phase == 1 else small
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    target[(x, y, z)] = b
    for prefix, blocks in (("s", small), ("l", late)):
        for (cx, cy, cz), origin, cb in tile(blocks):
            plan.templates.append(Template(f"{prefix}{cx}_{cy}_{cz}", origin, template_nbt(cb, origin)))
    return plan
