"""Assassin's Creed Chronicles (2015-2016): China 1526, India 1841, Russia 1918."""

import math
import random

from .. import structures as S
from ..palettes import CHINA, INDIA, RUSSIA
from ..registry import Build, World
from ..voxel import Voxel

# ------------------------------------------------------------------ helpers

_STAIR_FACING = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}


def _lamp(v: Voxel, x: int, y: int, z: int, post: str = "oak_fence", h: int = 3,
          light: str = "lantern") -> None:
    """Street lamp: a fence post with a lantern on top (base block at ``y``)."""
    v.column(x, y, z, h, post)
    v.set(x, y + h, z, light)


def _balustrade(v: Voxel, x1: int, y: int, z1: int, x2: int, z2: int, post: str,
                rail: str, period: int = 4) -> None:
    """Rail along the perimeter of a rectangle with posts every ``period`` blocks."""
    xa, xb = sorted((x1, x2)); za, zb = sorted((z1, z2))
    v.walls(xa, y, za, xb, y, zb, rail)
    for x in range(xa, xb + 1, period):
        v.set(x, y, za, post); v.set(x, y, zb, post)
    for z in range(za, zb + 1, period):
        v.set(xa, y, z, post); v.set(xb, y, z, post)


def _banner(v: Voxel, x: int, y: int, z: int, color: str, rotation: int = 8) -> None:
    v.set(x, y, z, f"{color}_banner[rotation={rotation}]")


def _snow_roof(v: Voxel, x1: int, z1: int, x2: int, z2: int, y: int, layers: int = 2) -> None:
    """Snow layers on every exposed roof block of a rectangle (block at ``y`` must be solid)."""
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for z in range(min(z1, z2), max(z1, z2) + 1):
            if v.get(x, y, z) not in (None, "minecraft:air") and v.get(x, y + 1, z) in (None, "minecraft:air"):
                v.set(x, y + 1, z, f"snow[layers={layers}]")


# ============================================================ CHINA 1526

def _wall_height(x: int, z: int) -> int:
    """Rolling hill terrain: a ridge along z = 0 (which the wall rides) over broad valleys."""
    ridge = 8.0 * math.exp(-(z / 16.0) ** 2)
    hills = 6 * math.sin(x / 23.0) + 3 * math.sin(x / 7.0 + 1.0) + 2.5 * math.cos(z / 11.0 + x / 31.0)
    hills += 1.5 * math.sin((x + 2 * z) / 5.0)
    return max(2, int(7 + ridge + hills))


def _wall_z(x: int) -> int:
    """The wall snakes across the ridge."""
    return int(round(4 * math.sin(x / 29.0) + 2 * math.sin(x / 11.0)))


def _watchtower(v: Voxel, x: int, y: int, z: int, lit: bool = True) -> None:
    """Two-storey Ming beacon tower straddling the wall.  ``y`` is the wall-walk floor level."""
    half = 5
    base = y - 7                                                     # footing sunk into the hill
    v.fill(x - half, base, z - half, x + half, y + 13, z + half, "stone_bricks")
    v.fill(x - half + 1, y - 5, z - half + 1, x + half - 1, y + 12, z + half - 1, "air")
    for yy in range(base, y + 14):                                    # weathered masonry
        for xx in range(x - half, x + half + 1):
            for zz in (z - half, z + half):
                if (xx * 7 + yy * 13 + zz * 3) % 11 == 0:
                    v.set(xx, yy, zz, "mossy_stone_bricks")
                if (xx * 5 + yy * 3 + zz * 7) % 17 == 0:
                    v.set(xx, yy, zz, "cracked_stone_bricks")
    v.fill(x - half + 1, y - 6, z - half + 1, x + half - 1, y - 6, z + half - 1, "stone_bricks")   # cellar floor
    v.fill(x - half + 1, y - 1, z - half + 1, x + half - 1, y - 1, z + half - 1, "stone_bricks")   # wall-walk floor
    v.fill(x - half + 1, y + 6, z - half + 1, x + half - 1, y + 6, z + half - 1, "spruce_planks")  # upper floor
    v.fill(x - half + 1, y + 12, z - half + 1, x + half - 1, y + 12, z + half - 1, "spruce_planks")  # roof deck base
    v.fill(x - half, y + 13, z - half, x + half, y + 13, z + half, "gray_terracotta")               # roof deck
    # doorways from the wall-walk (east / west) and down into the cellar
    for dx in (-half, half):
        v.fill(x + dx, y, z - 1, x + dx, y + 2, z + 1, "air")
        v.set(x + dx, y + 3, z - 1, "stone_brick_stairs[facing=east,half=top]")
        v.set(x + dx, y + 3, z + 1, "stone_brick_stairs[facing=west,half=top]")
    v.fill(x - 1, y - 1, z - 1, x + 1, y - 1, z + 1, "air")          # hatch to the cellar (ladder below)
    v.column(x, y - 6, z - half + 1, 6, "ladder[facing=south]")
    v.fill(x - half + 1, y - 6, z - half + 1, x - half + 1, y - 6, z - half + 1, "stone_bricks")
    # interior staircase: a square spiral of stone stairs round the walls up to the upper floor
    steps = [((x - 4, z + 4), "west"), ((x - 4, z + 3), "north"), ((x - 4, z + 2), "north"), ((x - 4, z + 1), "north"),
             ((x - 4, z), "north"), ((x - 4, z - 1), "north"), ((x - 4, z - 2), "north"), ((x - 4, z - 3), "north"),
             ((x - 3, z - 4), "east"), ((x - 2, z - 4), "east"), ((x - 1, z - 4), "east"), ((x, z - 4), "east"),
             ((x + 1, z - 4), "east"), ((x + 2, z - 4), "east")]
    for i, ((sx, sz), f) in enumerate(steps[:6]):
        v.fill(sx, y, sz, sx, y + i // 1 - 1, sz, "stone_bricks") if i > 0 else None
        v.set(sx, y + i, sz, f"stone_brick_stairs[facing={f},half=bottom]")
    v.fill(x - 4, y + 5, z - 4, x - 4, y + 5, z - 2, "air")          # landing opening through the upper floor
    v.fill(x - 4, y + 6, z - 4, x - 4, y + 6, z - 2, "air")
    # ladder from the upper floor to the roof deck
    v.column(x + 4, y + 7, z + 4, 6, "ladder[facing=west]")
    v.fill(x + 3, y + 12, z + 3, x + 4, y + 13, z + 4, "air")
    v.set(x + 4, y + 13, z + 4, "oak_trapdoor[facing=west,half=top,open=true]")
    # arrow slits: narrow openings on both floors, every other block
    for lvl in (y + 2, y + 8):
        for i in range(-3, 4, 2):
            v.set(x + i, lvl, z - half, "air"); v.set(x + i, lvl, z + half, "air")
            v.set(x - half, lvl, z + i, "air"); v.set(x + half, lvl, z + i, "air")
    # upper-floor windows with a timber lintel, and a tiled hood over the doors
    for i in (-2, 2):
        v.set(x + i, y + 9, z - half, "spruce_trapdoor[facing=north,half=top,open=true]")
        v.set(x + i, y + 9, z + half, "spruce_trapdoor[facing=south,half=top,open=true]")
    # parapet with merlons and corner piers
    v.walls(x - half, y + 14, z - half, x + half, y + 14, z + half, "stone_bricks")
    v.crenellate(x - half, y + 15, z - half, x + half, z + half, "stone_bricks", period=2)
    for px in (x - half, x + half):
        for pz in (z - half, z + half):
            v.column(px, y + 14, pz, 3, "stone_bricks")
            v.set(px, y + 17, pz, "lantern" if lit else "stone_brick_slab")
    # beacon brazier: stone plinth, campfire, and a signal-smoke chimney of hay
    v.fill(x - 1, y + 14, z - 1, x + 1, y + 14, z + 1, "polished_andesite")
    v.set(x, y + 15, z, "campfire[lit=true,facing=north]")
    v.set(x - 2, y + 14, z + 2, "hay_block"); v.set(x + 2, y + 14, z - 2, "hay_block")
    v.set(x + 2, y + 14, z + 2, "barrel[facing=up]")
    # a flag on a pole
    v.column(x - 2, y + 14, z - 2, 5, "spruce_fence")
    _banner(v, x - 2, y + 19, z - 2, "red", 4)
    # upper floor furnishings: bed-roll, table, weapon rack
    v.set(x + 3, y + 7, z - 3, "red_carpet"); v.set(x + 2, y + 7, z - 3, "red_carpet")
    v.set(x - 3, y + 7, z + 3, "crafting_table")
    v.set(x + 3, y + 7, z + 1, "spruce_fence"); v.set(x + 3, y + 8, z + 1, "lantern")
    v.set(x, y + 7, z + 3, "soul_lantern") if lit else None
    v.set(x - 2, y + 1, z + 3, "barrel[facing=up]"); v.set(x - 1, y + 1, z + 3, "barrel[facing=up]")
    v.set(x + 3, y + 1, z + 3, "campfire[lit=true,facing=north]")


def _gate_fortress(v: Voxel, hx: int, y: int, hz: int) -> None:
    """A Ming pass fortress (guan) with the road tunnelling through the wall under a two-tier gate tower."""
    half = 12
    v.fill(hx - half, y - 8, hz - 9, hx + half, y + 8, hz + 9, "stone_bricks")
    for yy in range(y - 8, y + 9):                                     # masonry variety
        for xx in range(hx - half, hx + half + 1):
            for zz in (hz - 9, hz + 9):
                if (xx * 3 + yy * 7 + zz) % 13 == 0:
                    v.set(xx, yy, zz, "mossy_stone_bricks")
    # barrel-vaulted road tunnel north-south through the fortress
    v.arch(hx - 4, y - 7, hz - 9, 9, 8, 19, "stone_bricks", axis="x")
    v.fill(hx - 3, y - 7, hz - 9, hx + 3, y - 2, hz + 9, "air")
    v.fill(hx - 3, y - 8, hz - 9, hx + 3, y - 8, hz + 9, "polished_andesite")      # paved road
    v.fill(hx - 3, y - 7, hz - 10, hx + 3, y - 2, hz - 10, "air"); v.fill(hx - 3, y - 7, hz + 10, hx + 3, y - 2, hz + 10, "air")
    for zz in (hz - 9, hz + 9):                                        # iron-studded gates (half open)
        v.fill(hx - 3, y - 7, zz, hx - 3, y - 3, zz, "dark_oak_planks")
        v.fill(hx + 3, y - 7, zz, hx + 3, y - 3, zz, "dark_oak_planks")
        v.fill(hx - 2, y - 2, zz, hx + 2, y - 2, zz, "iron_bars")      # portcullis
    for zz in (hz - 9, hz + 9):
        for dx in (-5, 5):
            v.set(hx + dx, y - 3, zz, "wall_torch[facing=north]" if zz < hz else "wall_torch[facing=south]")
    # ramparts on top of the fortress block, crenellated
    v.fill(hx - half, y + 9, hz - 9, hx + half, y + 9, hz + 9, "stone_bricks")
    v.walls(hx - half, y + 10, hz - 9, hx + half, y + 10, hz + 9, "stone_bricks")
    v.crenellate(hx - half, y + 11, hz - 9, hx + half, hz + 9, "stone_bricks", period=2)
    for dx in (-half, half):                                           # doorways from the wall-walk
        v.fill(hx + dx, y, hz - 1, hx + dx, y + 2, hz + 1, "air")
        v.fill(hx + dx, y + 3, hz - 1, hx + dx, y + 8, hz + 1, "air")   # open stairwell up to the ramparts
        v.fill(hx + dx, y + 9, hz - 1, hx + dx, y + 10, hz + 1, "air")
    for i in range(8):                                                 # ramp stairs west side, inside the block
        v.set(hx - half + 1 + i, y + 1 + i, hz, "stone_brick_stairs[facing=east,half=bottom]")
        v.fill(hx - half + 1 + i, y + 2 + i, hz - 1, hx - half + 1 + i, y + 9, hz + 1, "air")
        v.set(hx - half + 1 + i, y + 1 + i, hz - 1, "stone_brick_stairs[facing=east,half=bottom]")
        v.set(hx - half + 1 + i, y + 1 + i, hz + 1, "stone_brick_stairs[facing=east,half=bottom]")
    v.fill(hx - half + 9, y + 9, hz - 1, hx - half + 9, y + 9, hz + 1, "air")
    v.fill(hx - half, y + 1, hz - 1, hx - half, y + 9, hz + 1, "air")
    # two-tier gate tower: red columns, white infill, gray tiled roofs with upturned eaves and a yellow ridge
    tx1, tz1, tx2, tz2 = hx - 9, hz - 5, hx + 9, hz + 5
    base = y + 10
    v.fill(tx1, base, tz1, tx2, base + 5, tz2, "white_terracotta")
    v.fill(tx1 + 1, base, tz1 + 1, tx2 - 1, base + 11, tz2 - 1, "air")
    v.fill(tx1 + 1, base, tz1 + 1, tx2 - 1, base, tz2 - 1, "polished_andesite")
    for xx in range(tx1, tx2 + 1, 3):
        v.column(xx, base, tz1, 6, "red_terracotta"); v.column(xx, base, tz2, 6, "red_terracotta")
    for zz in range(tz1, tz2 + 1, 5):
        v.column(tx1, base, zz, 6, "red_terracotta"); v.column(tx2, base, zz, 6, "red_terracotta")
    for xx in range(tx1 + 1, tx2, 3):
        v.set(xx + 1, base + 2, tz1, "glass_pane"); v.set(xx + 1, base + 2, tz2, "glass_pane")
        v.set(xx + 1, base + 3, tz1, "glass_pane"); v.set(xx + 1, base + 3, tz2, "glass_pane")
    v.fill(hx - 1, base, tz2, hx + 1, base + 3, tz2, "air")
    v.fill(hx - 1, base, tz1, hx + 1, base + 3, tz1, "air")
    v.set(hx - 1, base + 4, tz2, "red_wall_banner[facing=south]"); v.set(hx + 1, base + 4, tz2, "red_wall_banner[facing=south]")
    v.set(hx - 3, base + 1, tz2 + 1, "lantern"); v.set(hx + 3, base + 1, tz2 + 1, "lantern")
    v.set(hx - 3, base, tz2 + 1, "spruce_fence"); v.set(hx + 3, base, tz2 + 1, "spruce_fence")
    # lower eave
    v.fill(tx1 - 2, base + 6, tz1 - 2, tx2 + 2, base + 6, tz2 + 2, "gray_terracotta")
    v.walls(tx1 - 2, base + 7, tz1 - 2, tx2 + 2, base + 7, tz2 + 2, "gray_terracotta")
    for xx in range(tx1 - 2, tx2 + 3):
        v.set(xx, base + 6, tz1 - 2, "deepslate_tile_stairs[facing=north,half=bottom]")
        v.set(xx, base + 6, tz2 + 2, "deepslate_tile_stairs[facing=south,half=bottom]")
    for pz in (tz1 - 2, tz2 + 2):
        for px in (tx1 - 2, tx2 + 2):
            v.set(px, base + 7, pz, "gold_block")                       # upturned corner finials
    # upper tier
    v.fill(tx1 + 2, base + 7, tz1 + 2, tx2 - 2, base + 11, tz2 - 2, "white_terracotta")
    v.fill(tx1 + 3, base + 7, tz1 + 3, tx2 - 3, base + 11, tz2 - 3, "air")
    v.fill(tx1 + 3, base + 6, tz1 + 3, tx2 - 3, base + 6, tz2 - 3, "spruce_planks")
    for xx in range(tx1 + 2, tx2 - 1, 3):
        v.column(xx, base + 7, tz1 + 2, 5, "red_terracotta"); v.column(xx, base + 7, tz2 - 2, 5, "red_terracotta")
    for xx in range(tx1 + 3, tx2 - 2, 3):
        v.set(xx + 1, base + 9, tz1 + 2, "glass_pane"); v.set(xx + 1, base + 9, tz2 - 2, "glass_pane")
    v.column(tx1 + 2, base + 7, tz1 + 2, 5, "red_terracotta"); v.column(tx2 - 2, base + 7, tz1 + 2, 5, "red_terracotta")
    v.column(tx1 + 2, base + 7, tz2 - 2, 5, "red_terracotta"); v.column(tx2 - 2, base + 7, tz2 - 2, 5, "red_terracotta")
    v.column(hx + 7, base + 1, hz - 4, 5, "ladder[facing=west]")       # up to the upper tier
    v.set(hx + 7, base + 6, hz - 4, "air")
    v.set(hx + 7, base + 6, hz - 4, "spruce_trapdoor[facing=west,half=top,open=true]")
    v.set(hx, base + 8, hz, "lantern[hanging=true]")
    v.set(hx, base + 11, hz, "spruce_planks")
    top = v.gable_roof(tx1 + 1, base + 12, tz1 + 1, tx2 - 1, tz2 - 1, "gray_terracotta", ridge_axis="x", overhang=1)
    v.fill(tx1 + 1, top, tz1 + 1, tx2 - 1, top, tz2 - 1, "yellow_terracotta")
    v.fill(tx1 + 1, top + 1, hz, tx2 - 1, top + 1, hz, "yellow_terracotta")
    for xx in range(tx1 + 1, tx2):                                      # eave stairs on the upper roof
        v.set(xx, base + 12, tz1, "deepslate_tile_stairs[facing=north,half=bottom]")
        v.set(xx, base + 12, tz2, "deepslate_tile_stairs[facing=south,half=bottom]")
    v.set(tx1, top + 1, hz, "gold_block"); v.set(tx2, top + 1, hz, "gold_block")   # ridge-end dragons
    v.set(hx, top + 2, hz, "gold_block")
    # bastion towers at the fortress corners with lanterns
    for px in (hx - half, hx + half):
        for pz in (hz - 9, hz + 9):
            v.fill(px - 1, y - 8, pz - 1, px + 1, y + 11, pz + 1, "stone_bricks")
            v.set(px, y + 12, pz, "campfire[lit=true,facing=north]")
    # moat-side bridge on the south approach and banners at the gate
    for dx in (-5, 5):
        v.column(hx + dx, y - 8, hz + 11, 4, "spruce_fence")
        _banner(v, hx + dx, y - 4, hz + 11, "red", 0)


def _tent(v: Voxel, x: int, y: int, z: int, r: int = 3, cloth: str = "white_wool") -> None:
    """Ming army bell tent: a cone of cloth over a wooden pole, open on the south side."""
    v.fill(x - r, y, z - r, x + r, y, z + r, "oak_planks")             # groundsheet / duckboards
    for k in range(r + 1):
        rr = r - k
        v.disc(x, y + 1 + k, z, rr, cloth, hollow=rr > 1)
    v.column(x, y + 1, z, r + 2, "oak_fence")
    v.set(x, y + r + 2, z, "red_banner[rotation=8]")
    v.fill(x, y + 1, z + r, x, y + 2, z + r, "air")                     # flap
    v.set(x + 1, y + 1, z - 1, "red_carpet"); v.set(x - 1, y + 1, z - 1, "white_carpet")
    v.set(x - 1, y + 1, z + 1, "barrel[facing=up]")


def _ming_camp(v: Voxel, x1: int, z1: int, x2: int, z2: int) -> None:
    """Palisaded army camp on the southern slope: tents, cook fires, horse lines, banners, a drill ground."""
    rng = random.Random(1526)
    # level the camp onto the hillside (each column already carries terrain up to _wall_height)
    gy = max(_wall_height(x, z) for x in range(x1, x2 + 1) for z in range(z1, z2 + 1))
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            h = _wall_height(x, z)
            v.fill(x, h + 1, z, x, gy, z, "coarse_dirt")
            v.set(x, gy, z, "dirt_path" if (x + z) % 3 else "coarse_dirt")
    # palisade of sharpened spruce with a gate on the north (wall) side
    for x in range(x1, x2 + 1):
        for z in (z1, z2):
            v.column(x, gy + 1, z, 3 if x % 2 else 4, "spruce_log")
            if x % 2 == 0:
                v.set(x, gy + 5, z, "spruce_fence")
    for z in range(z1, z2 + 1):
        for x in (x1, x2):
            v.column(x, gy + 1, z, 3 if z % 2 else 4, "spruce_log")
            if z % 2 == 0:
                v.set(x, gy + 5, z, "spruce_fence")
    gx = (x1 + x2) // 2
    v.fill(gx - 1, gy + 1, z1, gx + 1, gy + 4, z1, "air")
    v.fill(gx - 2, gy + 5, z1, gx + 2, gy + 5, z1, "spruce_planks")
    for dx in (-2, 2):
        v.set(gx + dx, gy + 6, z1, "spruce_fence"); v.set(gx + dx, gy + 7, z1, "red_banner[rotation=0]")
    v.set(gx - 2, gy + 4, z1 + 1, "wall_torch[facing=south]"); v.set(gx + 2, gy + 4, z1 + 1, "wall_torch[facing=south]")
    # the general's pavilion: a square timber-framed tent with a gray tiled roof
    px, pz = x1 + 7, z1 + 7
    v.fill(px - 4, gy + 1, pz - 4, px + 4, gy + 4, pz + 4, "white_wool")
    v.fill(px - 3, gy + 1, pz - 3, px + 3, gy + 4, pz + 3, "air")
    v.fill(px - 3, gy + 1, pz - 3, px + 3, gy + 1, pz + 3, "red_carpet")
    for cx in (px - 4, px + 4):
        for cz in (pz - 4, pz + 4):
            v.column(cx, gy + 1, cz, 4, "stripped_spruce_log")
    v.fill(px - 1, gy + 1, pz + 4, px + 1, gy + 3, pz + 4, "air")
    v.hip_roof(px - 4, gy + 5, pz - 4, px + 4, pz + 4, "gray_terracotta")
    v.set(px, gy + 9, pz, "gold_block")
    v.set(px, gy + 4, pz, "lantern[hanging=true]")
    v.set(px - 2, gy + 2, pz - 2, "lectern[facing=south]"); v.set(px + 2, gy + 2, pz - 2, "barrel[facing=up]")
    v.set(px, gy + 2, pz - 2, "yellow_banner[rotation=8]")
    # rows of bell tents
    for i, tx in enumerate(range(x1 + 18, x2 - 3, 7)):
        for j, tz in enumerate(range(z1 + 4, z2 - 3, 7)):
            if (i + j) % 3 == 2:
                continue
            _tent(v, tx, gy, tz, r=2 if (i + j) % 2 else 3, cloth=rng.choice(("white_wool", "white_wool", "light_gray_wool")))
    # cook fires, cauldrons and supply dumps along the east fence
    for z in range(z1 + 4, z2 - 3, 6):
        v.set(x2 - 3, gy + 1, z, "campfire[lit=true,facing=north]")
        v.set(x2 - 3, gy + 1, z + 1, "water_cauldron[level=3]")
        v.set(x2 - 2, gy + 1, z + 1, "hay_block"); v.set(x2 - 2, gy + 2, z + 1, "hay_block")
        v.set(x2 - 2, gy + 1, z, "barrel[facing=up]")
    # horse lines: hitching rail with troughs and hay
    hz = z2 - 3
    v.fill(x1 + 3, gy + 1, hz, x1 + 16, gy + 1, hz, "spruce_fence")
    for x in range(x1 + 4, x1 + 16, 3):
        v.set(x, gy + 1, hz - 1, "hay_block")
        v.set(x + 1, gy + 1, hz - 1, "water_cauldron[level=3]")
    # weapon racks and the drill ground banner line
    for x in range(x1 + 4, x1 + 16, 4):
        v.set(x, gy + 1, pz + 8, "iron_bars"); v.set(x, gy + 2, pz + 8, "iron_bars")
        v.set(x, gy + 3, pz + 8, "stone_brick_slab[type=bottom]")
    for x in range(gx - 6, gx + 7, 3):
        v.column(x, gy + 1, z1 + 3, 3, "spruce_fence")
        _banner(v, x, gy + 4, z1 + 3, "red" if x % 2 else "yellow", 8)
    # night lighting: lanterns on posts at the paths
    for x in range(x1 + 2, x2, 9):
        for z in (z1 + 2, z2 - 2):
            _lamp(v, x, gy + 1, z, post="spruce_fence", h=3)
    # a supply cart by the gate
    v.fill(gx + 4, gy + 2, z1 + 2, gx + 7, gy + 2, z1 + 3, "spruce_planks")
    v.fill(gx + 4, gy + 3, z1 + 2, gx + 7, gy + 3, z1 + 3, "hay_block")
    for cz in (z1 + 1, z1 + 4):
        v.set(gx + 5, gy + 1, cz, "stripped_spruce_log[axis=x]"); v.set(gx + 6, gy + 1, cz, "stripped_spruce_log[axis=x]")
    v.set(gx + 8, gy + 2, z1 + 2, "oak_fence"); v.set(gx + 9, gy + 2, z1 + 2, "oak_fence")


def great_wall(v: Voxel) -> None:
    """A Ming-dynasty stretch of the Great Wall over hills, with beacon towers (Shao Jun's China, 1526)."""
    S.pad(v, -100, -40, 100, 40, "grass_block")
    rng = random.Random(7)
    # ---- terrain: a ridge with the wall on its crest, valleys either side, rock outcrops and pines
    for x in range(-100, 101):
        for z in range(-40, 41):
            h = _wall_height(x, z)
            v.fill(x, 1, z, x, max(1, h - 3), z, "stone")
            v.fill(x, max(1, h - 2), z, x, h - 1, z, "dirt")
            top = "grass_block"
            steep = abs(_wall_height(x + 1, z) - _wall_height(x - 1, z)) + abs(_wall_height(x, z + 1) - _wall_height(x, z - 1))
            if steep >= 4:
                top = "stone" if (x * 3 + z * 5) % 4 else "cobblestone"
            elif (x * 7 + z * 11) % 23 == 0:
                top = "coarse_dirt"
            v.set(x, h, z, top)
            if top == "grass_block" and abs(z) > 7 and rng.random() < 0.05:
                v.set(x, h + 1, z, rng.choice(("short_grass", "short_grass", "fern", "poppy", "dandelion")))
    for _ in range(70):                                                   # pines on the slopes
        x = rng.randint(-98, 98); z = rng.choice((rng.randint(-38, -11), rng.randint(11, 38)))
        if -45 <= x <= -8 and 12 <= z <= 40:                              # keep the camp clear
            continue
        if 56 <= x <= 86 and -12 <= z <= 14:                              # and the fortress
            continue
        h = _wall_height(x, z)
        v.tree(x, h + 1, z, "spruce_log", "spruce_leaves[persistent=true]", height=rng.randint(5, 8), canopy=2)
    for _ in range(25):                                                   # boulders
        x = rng.randint(-98, 98); z = rng.choice((rng.randint(-38, -10), rng.randint(10, 38)))
        h = _wall_height(x, z)
        v.sphere(x, h, z, rng.choice((1, 1.5, 2)), rng.choice(("stone", "andesite", "cobblestone")), hollow=False)
    # ---- the wall: a 7-wide rampart snaking along the crest, with a walkway, parapets and arrow slits
    towers_x = [-80, -40, 0, 40]
    fort_x = 70
    for x in range(-100, 101):
        zc = _wall_z(x)
        h = _wall_height(x, zc)
        base = h - 6
        top = h + 6                                                       # walkway floor level
        v.fill(x, base, zc - 3, x, top, zc + 3, "stone_bricks")
        v.fill(x, base, zc - 4, x, h + 1, zc - 4, "stone_bricks")        # battered footing
        v.fill(x, base, zc + 4, x, h + 1, zc + 4, "stone_bricks")
        v.set(x, h + 2, zc - 4, "stone_brick_stairs[facing=south,half=bottom]")
        v.set(x, h + 2, zc + 4, "stone_brick_stairs[facing=north,half=bottom]")
        v.fill(x, top + 1, zc - 2, x, top + 1, zc + 2, "polished_andesite" if x % 5 else "stone_bricks")   # paved walkway
        v.fill(x, top + 1, zc - 2, x, top + 1, zc + 2, "stone_bricks") if x % 5 == 0 else None
        # parapets: a tall crenellated outer (north) parapet and a lower inner (south) one
        v.fill(x, top + 1, zc - 3, x, top + 3, zc - 3, "stone_bricks")
        v.fill(x, top + 1, zc + 3, x, top + 2, zc + 3, "stone_bricks")
        if x % 2 == 0:
            v.set(x, top + 4, zc - 3, "stone_bricks")
        else:
            v.set(x, top + 3, zc - 3, "stone_brick_slab[type=bottom]")
        if x % 6 == 3:                                                    # arrow slit in the outer parapet
            v.set(x, top + 2, zc - 3, "air")
        if x % 2 == 0:
            v.set(x, top + 3, zc + 3, "stone_brick_wall")
        # weathering
        for zz in (zc - 3, zc + 3, zc - 4, zc + 4):
            for yy in range(base, top + 1):
                if (x * 5 + yy * 7 + zz * 3) % 13 == 0:
                    v.set(x, yy, zz, "mossy_stone_bricks")
                elif (x * 3 + yy * 11 + zz) % 19 == 0:
                    v.set(x, yy, zz, "cracked_stone_bricks")
        # ramps between different walkway heights
        zn = _wall_z(x + 1); hn = _wall_height(x + 1, zn) + 6
        if hn > top:
            for zz in range(zc - 2, zc + 3):
                v.set(x, top + 2, zz, "stone_brick_stairs[facing=east,half=bottom]")
        elif hn < top:
            for zz in range(zc - 2, zc + 3):
                v.set(x + 1, hn + 2, zz, "stone_brick_stairs[facing=west,half=bottom]")
        if zn != zc:                                                      # bridge the bend in the parapet
            lo, hi = sorted((zc, zn))
            v.fill(x, top + 1, lo - 3, x, top + 3, hi - 3, "stone_bricks")
            v.fill(x, top + 1, lo + 3, x, top + 2, hi + 3, "stone_bricks")
            v.fill(x, base, lo - 3, x, top + 1, hi + 3, "stone_bricks")
            v.fill(x, top + 1, lo - 2, x, top + 1, hi + 2, "polished_andesite")
        # lanterns on the inner parapet every 8 blocks
        if x % 8 == 4:
            v.set(x, top + 3, zc + 3, "stone_bricks")
            v.set(x, top + 4, zc + 3, "lantern")
        # drainage spouts on the valley side
        if x % 10 == 5:
            v.set(x, top, zc - 4, "stone_brick_stairs[facing=south,half=top]")
    for tx in towers_x:
        zc = _wall_z(tx)
        _watchtower(v, tx, _wall_height(tx, zc) + 7, zc)
    zc = _wall_z(fort_x)
    _gate_fortress(v, fort_x, _wall_height(fort_x, zc) + 7, zc)
    # a stone stair climbing the southern slope up to the wall-walk at x = -60
    sx = -60
    zc = _wall_z(sx)
    top = _wall_height(sx, zc) + 6
    for i in range(14):
        z = zc + 4 + i
        y = top - i
        v.fill(sx - 1, 1, z, sx + 1, y - 1, z, "stone_bricks")
        v.fill(sx - 1, y, z, sx + 1, y, z, "stone_brick_stairs[facing=north,half=bottom]")
        v.fill(sx - 2, 1, z, sx - 2, y, z, "stone_bricks"); v.fill(sx + 2, 1, z, sx + 2, y, z, "stone_bricks")
        v.set(sx - 2, y + 1, z, "stone_brick_wall"); v.set(sx + 2, y + 1, z, "stone_brick_wall")
        if i % 4 == 1:
            v.set(sx - 2, y + 2, z, "lantern"); v.set(sx + 2, y + 2, z, "lantern")
    v.fill(sx - 1, top + 1, zc + 3, sx + 1, top + 3, zc + 3, "air")
    # the Ming garrison camp on the southern slope
    _ming_camp(v, -44, 13, -9, 38)
    # a paved road from the camp gate to the pass, lanterns along it
    for z in range(12, 0, -1):
        for x in range(-28, -24):
            h = _wall_height(x, z)
            v.set(x, h, z, "dirt_path")
    for x in range(-24, 60):
        z = 11 + int(3 * math.sin(x / 15.0))
        for dz in (-1, 0, 1):
            v.set(x, _wall_height(x, z + dz), z + dz, "dirt_path" if (x + dz) % 7 else "gravel")
        if x % 12 == 0:
            _lamp(v, x, _wall_height(x, z + 2) + 1, z + 2, post="spruce_fence", h=2)


# ============================================================ INDIA 1841

def _chhatri(v: Voxel, x: int, y: int, z: int, half: int = 1, block: str = "gold_block") -> None:
    """A small domed kiosk on slender pillars."""
    for px in (x - half, x + half):
        for pz in (z - half, z + half):
            v.column(px, y, pz, 3, block)
    v.fill(x - half, y + 3, z - half, x + half, y + 3, z + half, block)
    v.dome(x, y + 3, z, half + 0.5, block)
    v.set(x, y + 4 + half, z, "end_rod[facing=up]")


def _harmandir(v: Voxel, x: int, z: int) -> None:
    """The Harmandir Sahib: marble lower storey, gold-plated upper storeys, the fluted central dome and four chhatris."""
    hw = 10
    v.fill(x - hw - 2, 0, z - hw - 2, x + hw + 2, 0, z + hw + 2, "white_concrete")      # marble plinth in the pool
    v.fill(x - hw - 2, 1, z - hw - 2, x + hw + 2, 1, z + hw + 2, "smooth_quartz")
    for px in range(x - hw - 2, x + hw + 3, 2):                                             # inlaid pietra-dura border
        for pz in (z - hw - 2, z + hw + 2):
            v.set(px, 1, pz, "chiseled_quartz_block")
    for pz in range(z - hw - 2, z + hw + 3, 2):
        for px in (x - hw - 2, x + hw + 2):
            v.set(px, 1, pz, "chiseled_quartz_block")
    # lower storey: white marble with cusped arches on all four sides
    v.fill(x - hw, 2, z - hw, x + hw, 7, z + hw, "white_concrete")
    v.fill(x - hw + 1, 2, z - hw + 1, x + hw - 1, 7, z + hw - 1, "air")
    v.fill(x - hw + 1, 2, z - hw + 1, x + hw - 1, 2, z + hw - 1, "polished_diorite")
    for i in range(-hw, hw + 1):                                                            # marble floor inlay
        for j in range(-hw, hw + 1):
            if (i + j) % 2 == 0 and abs(i) < hw and abs(j) < hw:
                v.set(x + i, 2, z + j, "smooth_quartz")
    for side in range(4):
        for off in (-6, 0, 6):
            # arch openings (doors on every face: the temple is open to all four directions)
            if side == 0:
                v.fill(x + off - 1, 3, z + hw, x + off + 1, 5, z + hw, "air"); v.set(x + off, 6, z + hw, "air")
                v.set(x + off - 1, 6, z + hw, "quartz_stairs[facing=east,half=top]"); v.set(x + off + 1, 6, z + hw, "quartz_stairs[facing=west,half=top]")
            elif side == 1:
                v.fill(x + off - 1, 3, z - hw, x + off + 1, 5, z - hw, "air"); v.set(x + off, 6, z - hw, "air")
                v.set(x + off - 1, 6, z - hw, "quartz_stairs[facing=east,half=top]"); v.set(x + off + 1, 6, z - hw, "quartz_stairs[facing=west,half=top]")
            elif side == 2:
                v.fill(x + hw, 3, z + off - 1, x + hw, 5, z + off + 1, "air"); v.set(x + hw, 6, z + off, "air")
                v.set(x + hw, 6, z + off - 1, "quartz_stairs[facing=south,half=top]"); v.set(x + hw, 6, z + off + 1, "quartz_stairs[facing=north,half=top]")
            else:
                v.fill(x - hw, 3, z + off - 1, x - hw, 5, z + off + 1, "air"); v.set(x - hw, 6, z + off, "air")
                v.set(x - hw, 6, z + off - 1, "quartz_stairs[facing=south,half=top]"); v.set(x - hw, 6, z + off + 1, "quartz_stairs[facing=north,half=top]")
    for px in range(x - hw, x + hw + 1, 3):                                                 # marble pilasters
        v.column(px, 2, z - hw, 6, "quartz_pillar"); v.column(px, 2, z + hw, 6, "quartz_pillar")
        v.column(x - hw, 2, px - x + z, 6, "quartz_pillar"); v.column(x + hw, 2, px - x + z, 6, "quartz_pillar")
    for px in range(x - hw + 3, x + hw, 6):                                                 # between the doors: windows
        for pz in (z - hw, z + hw):
            v.set(px, 4, pz, "white_stained_glass_pane"); v.set(px, 5, pz, "white_stained_glass_pane")
        for pz in (x - hw, x + hw):
            v.set(pz, 4, z + px - x, "white_stained_glass_pane"); v.set(pz, 5, z + px - x, "white_stained_glass_pane")
    # the sanctum: the Guru Granth Sahib on a canopied palki under a chandelier
    v.fill(x - 2, 3, z - 2, x + 2, 3, z + 2, "red_carpet")
    v.set(x, 3, z, "lectern[facing=south]")
    for px in (x - 2, x + 2):
        for pz in (z - 2, z + 2):
            v.column(px, 3, pz, 3, "gold_block")
    v.fill(x - 2, 6, z - 2, x + 2, 6, z + 2, "gold_block")
    v.set(x, 5, z, "sea_lantern")
    v.set(x - 4, 3, z + 4, "lantern"); v.set(x + 4, 3, z - 4, "lantern")
    v.set(x - 4, 3, z - 4, "lantern"); v.set(x + 4, 3, z + 4, "lantern")
    # gilded chhajja (eave) around the first storey, carried on gold brackets
    v.fill(x - hw - 1, 8, z - hw - 1, x + hw + 1, 8, z + hw + 1, "gold_block")
    for px in range(x - hw - 1, x + hw + 2, 2):
        v.set(px, 7, z - hw - 1, "gold_block"); v.set(px, 7, z + hw + 1, "gold_block")
        v.set(x - hw - 1, 7, z + px - x, "gold_block"); v.set(x + hw + 1, 7, z + px - x, "gold_block")
    # upper storey: gold with arched windows, prayer hall inside lit by sea lanterns
    uw = 7
    v.fill(x - uw, 9, z - uw, x + uw, 14, z + uw, "gold_block")
    v.fill(x - uw + 1, 9, z - uw + 1, x + uw - 1, 13, z + uw - 1, "air")
    v.fill(x - uw + 1, 9, z - uw + 1, x + uw - 1, 9, z + uw - 1, "white_concrete")
    v.fill(x - 1, 9, z - 1, x + 1, 9, z + 1, "sea_lantern")
    for px in range(x - uw + 2, x + uw - 1, 3):
        for pz in (z - uw, z + uw):
            v.set(px, 11, pz, "yellow_stained_glass_pane"); v.set(px, 12, pz, "yellow_stained_glass_pane")
            v.set(px, 13, pz, "raw_gold_block")
        for pz in (x - uw, x + uw):
            v.set(pz, 11, z + px - x, "yellow_stained_glass_pane"); v.set(pz, 12, z + px - x, "yellow_stained_glass_pane")
            v.set(pz, 13, z + px - x, "raw_gold_block")
    v.fill(x - 1, 10, z + uw, x + 1, 12, z + uw, "air")                                     # balcony doorway south
    v.fill(x - 2, 9, z + uw + 1, x + 2, 9, z + uw + 3, "gold_block")                          # balcony
    _balustrade(v, x - 2, 10, z + uw + 1, x + 2, z + uw + 3, "gold_block", "gold_block")
    v.fill(x - 1, 10, z + uw + 1, x + 1, 10, z + uw + 2, "air")
    v.column(x + uw - 1, 3, z - uw + 1, 6, "ladder[facing=east]")                             # stair to the upper floor
    v.set(x + uw - 1, 9, z - uw + 1, "air")
    v.column(x + uw - 1, 9, z - uw + 1, 1, "ladder[facing=east]")
    # roof terrace with an inlaid parapet, four chhatris and the great fluted dome on its lotus drum
    v.fill(x - uw, 15, z - uw, x + uw, 15, z + uw, "gold_block")
    _balustrade(v, x - uw, 16, z - uw, x + uw, z + uw, "gold_block", "gold_block", period=2)
    for px in (x - uw + 1, x + uw - 1):
        for pz in (z - uw + 1, z + uw - 1):
            _chhatri(v, px, 16, pz, half=1)
    v.fill(x - 4, 16, z - 4, x + 4, 17, z + 4, "gold_block")                                 # drum
    v.fill(x - 3, 18, z - 3, x + 3, 18, z + 3, "gold_block")
    for a in range(0, 360, 45):                                                               # lotus petals
        px = round(x + 4.5 * math.cos(math.radians(a))); pz = round(z + 4.5 * math.sin(math.radians(a)))
        v.set(px, 18, pz, "raw_gold_block")
    v.sphere(x, 19, z, 4.5, "gold_block", hollow=True, y_min=19)
    v.fill(x - 1, 24, z - 1, x + 1, 24, z + 1, "gold_block")
    v.column(x, 25, z, 2, "gold_block")
    v.set(x, 27, z, "end_rod[facing=up]")                                                     # kalash finial
    for a in range(0, 360, 60):                                                               # rooftop lamps
        px = round(x + 6 * math.cos(math.radians(a))); pz = round(z + 6 * math.sin(math.radians(a)))
        v.set(px, 17, pz, "lantern")
    # marble steps down into the pool on all sides (for the ritual dip)
    for i in range(-3, 4):
        v.set(x + i, 0, z + hw + 3, "quartz_stairs[facing=north,half=bottom]")
        v.set(x + i, 0, z - hw - 3, "quartz_stairs[facing=south,half=bottom]")
        v.set(x + hw + 3, 0, z + i, "quartz_stairs[facing=west,half=bottom]")
        v.set(x - hw - 3, 0, z + i, "quartz_stairs[facing=east,half=bottom]")


def _clock_tower(v: Voxel, x: int, z: int) -> None:
    """The Ghanta Ghar clock tower on the north side of the parikrama, in red brick with white dressings."""
    half = 4
    v.fill(x - half - 1, 1, z - half - 1, x + half + 1, 2, z + half + 1, "white_concrete")
    v.fill(x - half, 3, z - half, x + half, 24, z + half, "bricks")
    v.fill(x - half + 1, 3, z - half + 1, x + half - 1, 24, z + half - 1, "air")
    for yy in range(3, 25):
        for px in (x - half, x + half):
            for pz in (z - half, z + half):
                v.set(px, yy, pz, "white_concrete")                                           # quoins
    for yy in (8, 14, 20):                                                                    # string courses
        v.walls(x - half, yy, z - half, x + half, yy, z + half, "white_concrete")
    v.fill(x - 1, 3, z + half, x + 1, 5, z + half, "air")                                     # door
    v.set(x - 1, 6, z + half, "quartz_stairs[facing=east,half=top]"); v.set(x + 1, 6, z + half, "quartz_stairs[facing=west,half=top]")
    for yy in (10, 16):                                                                       # arched windows
        for (dx, dz) in ((0, half), (0, -half), (half, 0), (-half, 0)):
            v.set(x + dx, yy, z + dz, "glass_pane"); v.set(x + dx, yy + 1, z + dz, "glass_pane")
            v.set(x + dx, yy + 2, z + dz, "white_concrete")
    # the clock faces: white dial, black hands and numerals
    for (dx, dz) in ((0, half), (0, -half), (half, 0), (-half, 0)):
        if dz:
            v.fill(x - 2, 20, z + dz, x + 2, 24, z + dz, "white_concrete")
            v.fill(x, 21, z + dz, x, 23, z + dz, "black_concrete")
            v.fill(x - 2, 22, z + dz, x + 2, 22, z + dz, "black_concrete")
            v.set(x, 22, z + dz, "gold_block")
            v.set(x - 1, 23, z + dz, "black_concrete") if dz > 0 else v.set(x + 1, 23, z + dz, "black_concrete")
        else:
            v.fill(x + dx, 20, z - 2, x + dx, 24, z + 2, "white_concrete")
            v.fill(x + dx, 21, z, x + dx, 23, z, "black_concrete")
            v.fill(x + dx, 22, z - 2, x + dx, 22, z + 2, "black_concrete")
            v.set(x + dx, 22, z, "gold_block")
    # interior spiral stair (ladder) and bell chamber
    v.column(x + half - 1, 3, z - half + 1, 22, "ladder[facing=east]")
    v.fill(x - half + 1, 25, z - half + 1, x + half - 1, 25, z + half - 1, "oak_planks")
    v.set(x + half - 1, 25, z - half + 1, "air")
    v.fill(x - half, 26, z - half, x + half, 26, z + half, "white_concrete")
    v.fill(x - half + 1, 26, z - half + 1, x + half - 1, 26, z + half - 1, "air")
    for px in (x - half, x + half):
        for pz in (z - half, z + half):
            v.column(px, 26, pz, 4, "white_concrete")
    v.set(x, 29, z, "bell[attachment=ceiling]")
    v.fill(x - half, 30, z - half, x + half, 30, z + half, "white_concrete")
    v.dome(x, 30, z, half + 0.5, "lime_terracotta")
    v.set(x, 35, z, "gold_block"); v.set(x, 36, z, "end_rod[facing=up]")
    for px in (x - half, x + half):
        for pz in (z - half, z + half):
            v.set(px, 31, pz, "lantern")
    _lamp(v, x - 3, 3, z + half + 2, post="polished_diorite_wall") if False else None
    for dx in (-3, 3):
        v.column(x + dx, 3, z + half + 2, 2, "quartz_pillar"); v.set(x + dx, 5, z + half + 2, "lantern")


def _langar(v: Voxel, x1: int, z1: int, x2: int, z2: int) -> None:
    """The langar hall: a long arcaded dining hall with its kitchen, cauldrons and rows of mats."""
    v.fill(x1, 1, z1, x2, 1, z2, "polished_diorite")
    v.fill(x1, 2, z1, x2, 8, z2, "white_concrete")
    v.fill(x1 + 1, 2, z1 + 1, x2 - 1, 8, z2 - 1, "air")
    v.fill(x1 + 1, 2, z1 + 1, x2 - 1, 2, z2 - 1, "polished_diorite")
    for z in range(z1 + 2, z2 - 1, 4):                                                        # open arcade on the west
        v.fill(x1, 3, z, x1, 5, z + 1, "air")
        v.set(x1, 6, z, "quartz_stairs[facing=south,half=top]"); v.set(x1, 6, z + 1, "quartz_stairs[facing=north,half=top]")
    for z in range(z1 + 2, z2 - 1, 4):                                                        # windows on the east
        v.set(x2, 4, z, "glass_pane"); v.set(x2, 5, z, "glass_pane")
    v.fill(x1, 9, z1, x2, 9, z2, "red_sandstone")
    v.crenellate(x1, 10, z1, x2, z2, "cut_red_sandstone", period=2)
    for z in range(z1 + 3, z2 - 2, 4):                                                        # rows of mats and plates
        for x in range(x1 + 3, x2 - 2, 3):
            v.set(x, 3, z, "orange_carpet" if (x + z) % 2 else "white_carpet")
    for z in range(z1 + 4, z2 - 2, 8):
        v.set(x1 + 1 + (x2 - x1) // 2, 8, z, "lantern[hanging=true]")
    # kitchen at the north end: hearths, cauldrons, sacks of flour and the chapati griddles
    kz = z1 + 1
    v.fill(x1 + 1, 3, kz, x2 - 1, 3, kz, "bricks")
    for x in range(x1 + 2, x2 - 1, 3):
        v.set(x, 3, kz, "campfire[lit=true,facing=north]")
        v.set(x, 4, kz, "water_cauldron[level=3]")
        v.set(x + 1, 3, kz + 1, "hay_block")
    v.fill(x1 + 1, 9, kz, x2 - 1, 11, kz, "bricks")                                           # chimney stack
    v.set(x1 + 2 + (x2 - x1) // 2, 12, kz, "campfire[lit=true,facing=north]")
    # serving verandah with seated rows outside
    v.fill(x1 - 4, 1, z1, x1 - 1, 1, z2, "smooth_red_sandstone")
    for z in range(z1, z2 + 1, 4):
        v.column(x1 - 4, 2, z, 5, "cut_red_sandstone")
    v.fill(x1 - 5, 7, z1 - 1, x1 - 1, 7, z2 + 1, "red_sandstone_slab[type=top]")
    for z in range(z1 + 2, z2, 4):
        v.set(x1 - 4, 6, z, "lantern[hanging=true]")


def _bazaar(v: Voxel, x1: int, z1: int, x2: int, z2: int, seed: int = 1841) -> None:
    """A bazaar street: two-storey shophouses with balconies, cloth awnings over market stalls, lamps."""
    rng = random.Random(seed)
    v.fill(x1, 0, z1, x2, 0, z2, "red_sand")
    for x in range(x1, x2 + 1):                                                               # paved street
        for z in range(z1, z2 + 1):
            if (x + z) % 5 == 0:
                v.set(x, 0, z, "cut_red_sandstone")
    cloths = ("orange_wool", "red_wool", "lime_wool", "yellow_wool", "magenta_wool", "light_blue_wool", "white_wool")
    x = x1
    while x + 6 <= x2:
        w = rng.choice((6, 7, 8))
        if x + w > x2:
            w = x2 - x
        wall = rng.choice(("red_sandstone", "smooth_red_sandstone", "white_terracotta", "white_concrete"))
        floors = rng.choice((2, 2, 3))
        h = floors * 4
        v.fill(x, 1, z2 - 9, x + w - 1, h, z2, wall)
        v.fill(x + 1, 1, z2 - 8, x + w - 2, h, z2 - 1, "air")
        v.fill(x + 1, 1, z2 - 8, x + w - 2, 1, z2 - 1, "polished_diorite")
        for f in range(1, floors):
            v.fill(x + 1, f * 4, z2 - 8, x + w - 2, f * 4, z2 - 1, "oak_planks")
        # shopfront: open arches on the ground floor facing the street (north), jharokha balcony above
        for dx in range(1, w - 1, 3):
            v.fill(x + dx, 1, z2 - 9, x + dx + 1 if dx + 1 < w - 1 else x + dx, 3, z2 - 9, "air")
        v.fill(x + 1, 5, z2 - 10, x + w - 2, 5, z2 - 10, "cut_red_sandstone")
        v.fill(x + 1, 6, z2 - 10, x + w - 2, 6, z2 - 10, "oak_fence")
        for dx in range(2, w - 2, 2):
            v.set(x + dx, 6, z2 - 9, "glass_pane"); v.set(x + dx, 7, z2 - 9, "glass_pane")
            if floors == 3:
                v.set(x + dx, 10, z2 - 9, "glass_pane"); v.set(x + dx, 11, z2 - 9, "glass_pane")
        v.set(x + w // 2, 6, z2 - 9, "air"); v.set(x + w // 2, 7, z2 - 9, "air")
        # roof: flat with a parapet, or a little domed chhatri
        v.fill(x, h + 1, z2 - 9, x + w - 1, h + 1, z2, "white_concrete")
        v.crenellate(x, h + 2, z2 - 9, x + w - 1, z2, "cut_red_sandstone", period=2)
        if rng.random() < 0.4:
            _chhatri(v, x + w // 2, h + 2, z2 - 4, half=1, block="white_concrete")
        # cloth awning on poles over the stall in front
        cloth = rng.choice(cloths)
        v.fill(x + 1, 4, z2 - 13, x + w - 2, 4, z2 - 10, cloth)
        v.fill(x + 1, 4, z2 - 14, x + w - 2, 4, z2 - 14, cloth.replace("wool", "carpet") if False else cloth)
        v.set(x + 1, 3, z2 - 14, "oak_fence"); v.set(x + w - 2, 3, z2 - 14, "oak_fence")
        v.set(x + 1, 2, z2 - 14, "oak_fence"); v.set(x + w - 2, 2, z2 - 14, "oak_fence")
        v.set(x + 1, 1, z2 - 14, "oak_fence"); v.set(x + w - 2, 1, z2 - 14, "oak_fence")
        # the stall and its wares
        v.fill(x + 1, 1, z2 - 12, x + w - 2, 1, z2 - 12, "oak_slab[type=bottom]")
        for dx in range(1, w - 1):
            v.set(x + dx, 2, z2 - 12, rng.choice(("hay_block", "melon", "pumpkin", "barrel[facing=up]", "yellow_wool",
                                                   "red_wool", "cake", "honey_block", "bookshelf", "dried_kelp_block")))
        v.set(x + 1, 1, z2 - 11, "barrel[facing=up]"); v.set(x + w - 2, 1, z2 - 11, "barrel[facing=up]")
        # lamp outside each shop
        v.set(x + w - 1, 3, z2 - 10, "wall_torch[facing=north]")
        x += w
    for x in range(x1 + 3, x2, 9):                                                             # street lamps
        _lamp(v, x, 1, z1 + 1, post="cut_red_sandstone", h=3)


def _sikh_fort_gate(v: Voxel, cx: int, z: int) -> None:
    """A Gobindgarh-style fort gate: twin round bastions, a cusped arch, battlements and the Nishan Sahib."""
    for dx in (-8, 8):
        v.cylinder(cx + dx, 1, z + 5, 4, 13, "red_sandstone", hollow=True)
        v.cylinder(cx + dx, 1, z + 5, 3, 1, "polished_diorite")
        v.disc(cx + dx, 13, z + 5, 4, "red_sandstone")
        for a in range(0, 360, 36):
            px = round(cx + dx + 4 * math.cos(math.radians(a))); pz = round(z + 5 + 4 * math.sin(math.radians(a)))
            v.set(px, 14, pz, "cut_red_sandstone")
        for yy in (5, 9):
            for a in (45, 135, 225, 315):
                px = round(cx + dx + 4 * math.cos(math.radians(a))); pz = round(z + 5 + 4 * math.sin(math.radians(a)))
                v.set(px, yy, pz, "air")
        v.column(cx + dx, 1, z + 5, 12, "ladder[facing=north]")
        v.set(cx + dx, 13, z + 5, "air")
        v.set(cx + dx, 15, z + 5, "lantern")
    v.fill(cx - 5, 1, z + 2, cx + 5, 10, z + 8, "red_sandstone")
    v.arch(cx - 3, 1, z + 2, 7, 8, 7, "red_sandstone", axis="x")
    v.fill(cx - 2, 1, z + 2, cx + 2, 5, z + 8, "air")
    v.fill(cx - 2, 0, z + 2, cx + 2, 0, z + 8, "smooth_red_sandstone")
    v.fill(cx - 5, 11, z + 2, cx + 5, 11, z + 8, "cut_red_sandstone")
    v.crenellate(cx - 5, 12, z + 2, cx + 5, z + 8, "red_sandstone", period=2)
    for dx in (-3, 3):                                                                        # jharokhas over the arch
        v.set(cx + dx, 8, z + 1, "cut_red_sandstone"); v.set(cx + dx, 9, z + 1, "red_sandstone_wall")
        v.set(cx + dx, 10, z + 1, "glass_pane")
    v.fill(cx - 1, 1, z + 5, cx + 1, 1, z + 5, "iron_bars")                                   # the portcullis rests open
    v.fill(cx - 1, 6, z + 5, cx + 1, 6, z + 5, "iron_bars")
    v.set(cx - 2, 5, z + 1, "wall_torch[facing=north]"); v.set(cx + 2, 5, z + 1, "wall_torch[facing=north]")
    v.set(cx, 6, z + 1, "gold_block")                                                         # the Khanda over the gate
    v.set(cx, 7, z + 1, "gold_block")
    # the Nishan Sahib: a tall saffron flag on the gate
    v.column(cx, 12, z + 5, 10, "white_concrete")
    v.set(cx, 22, z + 5, "orange_banner[rotation=0]")
    v.set(cx, 21, z + 4, "orange_wall_banner[facing=north]")
    for dx in (-4, 4):
        v.set(cx + dx, 12, z + 2, "lantern"); v.set(cx + dx, 12, z + 8, "lantern")


def _elephant(v: Voxel, x: int, y: int, z: int, facing: int = 1) -> None:
    """A blocky war elephant (5 long, 3 wide) facing +z or -z, with a red howdah cloth."""
    body = "gray_concrete"; dark = "light_gray_concrete"
    for lx in (x - 1, x + 1):
        for lz in (z - 2, z + 1):
            v.fill(lx, y, lz, lx, y + 2, lz, body)
    v.fill(x - 1, y + 3, z - 2, x + 1, y + 5, z + 1, body)                                    # body
    v.fill(x - 1, y + 4, z - 2, x + 1, y + 4, z + 1, dark)
    hz = z + 3 * facing if facing > 0 else z - 4
    v.fill(x - 1, y + 4, hz - (0 if facing > 0 else 0), x + 1, y + 6, hz, body)                # head
    v.set(x - 2, y + 5, hz, dark); v.set(x + 2, y + 5, hz, dark)                               # ears
    tz = hz + facing
    v.fill(x, y + 2, tz, x, y + 4, tz, body)                                                   # trunk
    v.set(x, y + 1, tz + facing, body)
    v.set(x - 1, y + 3, tz, "white_concrete"); v.set(x + 1, y + 3, tz, "white_concrete")       # tusks
    v.set(x, y + 6, hz - facing, "black_concrete") if False else None
    v.fill(x - 1, y + 6, z - 2, x + 1, y + 6, z + 1, "red_carpet")                             # caparison
    v.set(x, y + 6, z - 1, "red_wool"); v.set(x, y + 7, z - 1, "gold_block")                   # howdah


def _elephant_stables(v: Voxel, x1: int, z1: int, x2: int, z2: int) -> None:
    """The maharaja's elephant lines: tall arched stalls, hay lofts, water troughs and two elephants."""
    v.fill(x1, 0, z1, x2, 0, z2, "coarse_dirt")
    v.fill(x1, 1, z1, x2, 10, z1 + 8, "red_sandstone")
    v.fill(x1 + 1, 1, z1 + 1, x2 - 1, 9, z1 + 7, "air")
    v.fill(x1 + 1, 1, z1 + 1, x2 - 1, 1, z1 + 7, "coarse_dirt")
    for x in range(x1 + 2, x2 - 1, 8):                                                        # stall arches on the south
        v.arch(x - 1, 1, z1 + 8, 7, 8, 1, "red_sandstone", axis="x")
        v.fill(x, 1, z1 + 8, x + 4, 6, z1 + 8, "air")
        v.fill(x, 1, z1 + 2, x + 4, 1, z1 + 6, "hay_block")
        v.set(x + 2, 1, z1 + 1, "water_cauldron[level=3]")
        v.set(x + 2, 9, z1 + 4, "lantern[hanging=true]")
    for x in range(x1 + 7, x2 - 1, 8):                                                        # dividing piers
        v.fill(x, 1, z1 + 1, x, 9, z1 + 7, "cut_red_sandstone")
    v.fill(x1, 11, z1, x2, 11, z1 + 8, "white_concrete")
    v.crenellate(x1, 12, z1, x2, z1 + 8, "cut_red_sandstone", period=2)
    v.fill(x1 + 2, 7, z1 + 2, x2 - 2, 7, z1 + 3, "oak_planks")                                 # hay loft
    v.fill(x1 + 2, 8, z1 + 2, x2 - 2, 8, z1 + 3, "hay_block")
    _elephant(v, x1 + 4, 1, z1 + 12, facing=-1)
    _elephant(v, x1 + 14, 1, z1 + 13, facing=1)
    v.fill(x1, 1, z2, x2, 1, z2, "oak_fence")                                                  # paddock fence
    v.set(x1 + 9, 1, z2, "oak_fence_gate[facing=north]")
    for x in range(x1 + 2, x2, 6):
        v.set(x, 1, z1 + 11, "hay_block")
    _lamp(v, x1 + 1, 1, z2 - 1, post="cut_red_sandstone", h=3); _lamp(v, x2 - 1, 1, z2 - 1, post="cut_red_sandstone", h=3)


def amritsar(v: Voxel) -> None:
    """The Harmandir Sahib (Golden Temple) in its sacred pool, Sikh Empire 1841 (Arbaaz Mir's India)."""
    S.pad(v, -60, -60, 60, 60, "polished_diorite")
    # ---- the sarovar (sacred pool) with its marble parikrama walkway
    pr = 40
    v.fill(-pr, -2, -pr, pr, 0, pr, "water")
    v.fill(-pr - 1, -3, -pr - 1, pr + 1, -3, pr + 1, "prismarine")                            # pool bed
    v.walls(-pr - 1, -2, -pr - 1, pr + 1, 0, pr + 1, "smooth_quartz")                         # marble pool edge
    for x in range(-pr - 1, pr + 2, 4):                                                        # inlaid edging
        v.set(x, 0, -pr - 1, "chiseled_quartz_block"); v.set(x, 0, pr + 1, "chiseled_quartz_block")
        v.set(-pr - 1, 0, x, "chiseled_quartz_block"); v.set(pr + 1, 0, x, "chiseled_quartz_block")
    v.fill(-pr - 7, 0, -pr - 7, pr + 7, 0, -pr - 2, "white_concrete")                         # parikrama
    v.fill(-pr - 7, 0, pr + 2, pr + 7, 0, pr + 7, "white_concrete")
    v.fill(-pr - 7, 0, -pr - 7, -pr - 2, 0, pr + 7, "white_concrete")
    v.fill(pr + 2, 0, -pr - 7, pr + 7, 0, pr + 7, "white_concrete")
    for i in range(-pr - 7, pr + 8):                                                           # marble chequer
        for ring in (-pr - 5, pr + 5):
            if i % 2 == 0:
                v.set(i, 0, ring, "polished_diorite"); v.set(ring, 0, i, "polished_diorite")
    for i in range(-pr - 1, pr + 2, 8):                                                        # ghats: steps into the water
        for (x, z, f) in ((i, -pr - 1, "south"), (i, pr + 1, "north"), (-pr - 1, i, "east"), (pr + 1, i, "west")):
            v.set(x, 0, z, f"quartz_stairs[facing={f},half=bottom]")
            v.set(x, -1, z, "smooth_quartz")
    # lamp posts and marble balustrade round the outer parikrama edge, arcade of the bungas behind
    for i in range(-pr - 7, pr + 8, 6):
        for (x, z) in ((i, -pr - 7), (i, pr + 7), (-pr - 7, i), (pr + 7, i)):
            if abs(i) < 6 and z == pr + 7:
                continue
            v.column(x, 1, z, 2, "quartz_pillar"); v.set(x, 3, z, "lantern")
    # ---- the Harmandir Sahib on its island, and the Guru's causeway from the south bank
    _harmandir(v, 0, 0)
    v.fill(-2, 0, 13, 2, 0, pr + 1, "white_concrete")
    v.fill(-2, -2, 13, 2, -1, pr + 1, "smooth_quartz")
    for z in range(13, pr + 1):
        if z % 2 == 0:
            v.set(0, 0, z, "polished_diorite")
    v.fill(-3, 0, 13, -3, 0, pr + 1, "smooth_quartz"); v.fill(3, 0, 13, 3, 0, pr + 1, "smooth_quartz")
    v.fill(-3, 1, 13, -3, 1, pr + 1, "diorite_wall"); v.fill(3, 1, 13, 3, 1, pr + 1, "diorite_wall")
    for z in range(15, pr + 1, 5):
        v.set(-3, 1, z, "quartz_pillar"); v.set(3, 1, z, "quartz_pillar")
        v.set(-3, 2, z, "lantern"); v.set(3, 2, z, "lantern")
    # the Darshani Deorhi gateway at the land end of the causeway
    gx, gz = 0, pr + 5
    v.fill(gx - 6, 1, gz - 3, gx + 6, 9, gz + 3, "white_concrete")
    v.fill(gx - 2, 1, gz - 3, gx + 2, 6, gz + 3, "air")
    v.set(gx - 2, 7, gz - 3, "quartz_stairs[facing=east,half=top]"); v.set(gx + 2, 7, gz - 3, "quartz_stairs[facing=west,half=top]")
    v.set(gx - 2, 7, gz + 3, "quartz_stairs[facing=east,half=top]"); v.set(gx + 2, 7, gz + 3, "quartz_stairs[facing=west,half=top]")
    v.fill(gx - 1, 7, gz - 3, gx + 1, 7, gz - 3, "air"); v.fill(gx - 1, 7, gz + 3, gx + 1, 7, gz + 3, "air")
    v.fill(gx - 2, 1, gz - 3, gx + 2, 1, gz + 3, "polished_diorite")
    v.fill(gx - 6, 10, gz - 3, gx + 6, 10, gz + 3, "gold_block")
    v.dome(gx, 10, gz, 4, "gold_block"); v.set(gx, 15, gz, "end_rod[facing=up]")
    for px in (gx - 5, gx + 5):
        for pz in (gz - 2, gz + 2):
            _chhatri(v, px, 11, pz, half=1, block="white_concrete")
    for px in range(gx - 5, gx + 6, 2):
        v.set(px, 4, gz - 3, "white_stained_glass_pane") if abs(px) > 2 else None
        v.set(px, 4, gz + 3, "white_stained_glass_pane") if abs(px) > 2 else None
    v.set(gx, 8, gz, "sea_lantern")
    v.set(gx - 3, 3, gz - 4, "wall_torch[facing=north]"); v.set(gx + 3, 3, gz - 4, "wall_torch[facing=north]")
    # ---- the Ghanta Ghar clock tower on the north parikrama, the langar on the east, the stepwell beyond
    _clock_tower(v, 0, -pr - 14)
    _langar(v, 50, -30, 59, 30)
    S.stepwell(v, 0, -80, INDIA, half=10, depth=8)
    # white bunga rest-houses along the west parikrama, with lit arcades
    for z in (-36, -12, 12):
        top = S.house(v, -59, z, 9, 12, INDIA, floors=2, roof="flat", wall="white_concrete")
        _chhatri(v, -55, top, z + 6, half=1, block="white_concrete")
        v.set(-50, 4, z + 6, "lantern[hanging=true]") if False else None
        v.fill(-50, 1, z + 1, -50, 1, z + 10, "polished_diorite")
        for zz in range(z + 2, z + 10, 3):
            v.set(-51, 2, zz, "air"); v.set(-51, 3, zz, "air")
    # ---- the bazaar street with its awnings south of the parikrama, a fort gate at its west end,
    #      the elephant stables at the east end
    _bazaar(v, -34, 48, 30, 61)
    _sikh_fort_gate(v, -47, 48)
    _elephant_stables(v, 36, 46, 58, 61)
    v.fill(-60, 0, 46, -35, 0, 47, "red_sand"); v.fill(31, 0, 46, 60, 0, 47, "red_sand")
    # Sikh guards' nishan flags on the parikrama corners
    for (x, z) in ((-pr - 7, -pr - 7), (pr + 7, -pr - 7), (-pr - 7, pr + 7), (pr + 7, pr + 7)):
        v.column(x, 1, z, 8, "white_concrete"); v.set(x, 9, z, "orange_banner[rotation=0]")


# ============================================================ RUSSIA 1918

def _onion_dome(v: Voxel, x: int, y: int, z: int, r: float, color: str) -> None:
    """Drum, bulbous onion dome, neck and a gilded cross."""
    v.cylinder(x, y, z, r - 1, 4, "white_concrete", hollow=True)
    for a in range(0, 360, 45):
        px = round(x + (r - 1) * math.cos(math.radians(a))); pz = round(z + (r - 1) * math.sin(math.radians(a)))
        v.set(px, y + 2, pz, "glass_pane")
    v.sphere(x, y + 4 + r, z, r, color, hollow=True, y_min=y + 4)
    v.cone(x, int(y + 4 + r + r * 0.6), z, max(1.5, r * 0.6), int(r) + 2, color)
    v.column(x, int(y + 4 + r + r * 0.6) + int(r) + 2, z, 3, "gold_block")
    cy = int(y + 4 + r + r * 0.6) + int(r) + 3
    v.set(x - 1, cy, z, "gold_block"); v.set(x + 1, cy, z, "gold_block")


def _winter_palace(v: Voxel, x1: int, z1: int, x2: int, z2: int) -> None:
    """The Winter Palace south facade: green walls, white two-storey columns, gold capitals, roofline statues."""
    wall, white, gold = "cyan_terracotta", "white_concrete", "gold_block"
    v.fill(x1, 1, z1, x2, 2, z2, "white_concrete")                                             # rusticated ground storey
    v.fill(x1, 3, z1, x2, 18, z2, wall)
    v.fill(x1 + 1, 1, z1 + 1, x2 - 1, 18, z2 - 1, "air")
    v.fill(x1 + 1, 1, z1 + 1, x2 - 1, 1, z2 - 1, "polished_diorite")
    for f in (7, 13):                                                                          # upper floors
        v.fill(x1 + 1, f, z1 + 1, x2 - 1, f, z2 - 1, "oak_planks")
    v.fill(x1, 6, z1, x2, 6, z2, white)                                                        # string course
    v.walls(x1, 19, z1, x2, 19, z2, white)                                                     # cornice
    v.fill(x1, 20, z1, x2, 20, z2, "polished_diorite")                                         # roof (zinc)
    v.fill(x1 + 1, 20, z1 + 1, x2 - 1, 20, z2 - 1, "light_gray_concrete")
    for x in range(x1, x2 + 1):                                                                # windows, columns, statues
        for z in (z1, z2):
            if (x - x1) % 4 == 2:
                v.fill(x, 3, z, x, 4, z, "glass_pane")                                         # ground: arched
                v.set(x, 5, z, white)
                v.fill(x, 8, z, x, 10, z, "glass_pane")                                        # piano nobile: tall
                v.set(x, 11, z, gold)
                v.fill(x, 14, z, x, 15, z, "glass_pane")
                v.set(x, 16, z, white)
            if (x - x1) % 8 == 0:
                v.column(x, 7, z, 11, white)                                                   # giant-order column
                v.set(x, 18, z, gold)                                                          # capital
                v.set(x, 3, z, white); v.set(x, 4, z, white); v.set(x, 5, z, white)            # pilaster below
                v.set(x, 21, z, "polished_diorite")                                            # plinth on the balustrade
                v.set(x, 22, z, "light_gray_concrete" if (x - x1) % 16 else white)             # statue / urn
                v.set(x, 23, z, "light_gray_concrete") if (x - x1) % 16 else None
            elif (x - x1) % 2 == 0:
                v.set(x, 21, z, "diorite_wall")                                                # balustrade
    for z in range(z1 + 2, z2 - 1, 4):                                                         # the short end facades
        for x in (x1, x2):
            v.fill(x, 8, z, x, 10, z, "glass_pane"); v.set(x, 11, z, gold)
            v.fill(x, 3, z, x, 4, z, "glass_pane")
            v.column(x, 7, z - 1, 11, white); v.set(x, 18, z - 1, gold)
    # the three grand gates onto Palace Square (south face), with the imperial eagle over the centre
    cx = (x1 + x2) // 2
    for gx in (cx - 24, cx, cx + 24):
        v.fill(gx - 1, 1, z2, gx + 1, 4, z2, "air")
        v.fill(gx - 2, 5, z2, gx + 2, 5, z2, white)
        v.set(gx - 2, 1, z2 + 1, "iron_bars"); v.set(gx + 2, 1, z2 + 1, "iron_bars")
        v.set(gx - 2, 2, z2 + 1, "iron_bars"); v.set(gx + 2, 2, z2 + 1, "iron_bars")
        v.set(gx - 3, 1, z2 + 1, "lantern"); v.set(gx + 3, 1, z2 + 1, "lantern")
        v.set(gx - 3, 0, z2 + 1, "polished_diorite"); v.set(gx + 3, 0, z2 + 1, "polished_diorite")
    v.fill(cx - 1, 20, z2, cx + 1, 21, z2, gold)
    v.set(cx, 22, z2, gold)
    # red banners of the revolution hang from the balcony and the lamps are lit
    for gx in (cx - 12, cx - 6, cx + 6, cx + 12):
        v.set(gx, 12, z2 + 1, "red_wall_banner[facing=south]") if False else None
        v.set(gx, 12, z2, "red_banner[rotation=8]") if False else None
        v.set(gx, 11, z2, "red_wall_banner[facing=south]")
    v.set(cx, 11, z2, "red_wall_banner[facing=south]")
    for gx in range(cx - 30, cx + 31, 10):                                                     # courtyard side lamps
        v.set(gx, 1, z1 - 1, "iron_bars"); v.set(gx, 2, z1 - 1, "iron_bars"); v.set(gx, 3, z1 - 1, "lantern")
    # interior: the Jordan staircase hall, lit chandeliers down the enfilade
    for x in range(x1 + 8, x2 - 7, 16):
        v.set(x, 18, z1 + (z2 - z1) // 2, "lantern[hanging=true]")
        v.set(x, 12, z1 + (z2 - z1) // 2, "lantern[hanging=true]")
        v.set(x, 6, z1 + (z2 - z1) // 2, "lantern[hanging=true]")
    v.fill(cx - 6, 1, z1 + 2, cx + 6, 1, z2 - 2, "red_carpet")
    for i in range(5):                                                                         # the grand stair
        v.fill(cx - 4, 2 + i, z1 + 3 + i, cx + 4, 2 + i, z1 + 3 + i, "quartz_stairs[facing=south,half=bottom]")
        v.fill(cx - 4, 1, z1 + 3 + i, cx + 4, 1 + i, z1 + 3 + i, "white_concrete")
    v.fill(cx - 4, 7, z1 + 8, cx + 4, 7, z1 + 10, "white_concrete")
    v.fill(cx - 4, 7, z1 + 1, cx + 4, 7, z1 + 7, "air")
    _snow_roof(v, x1, z1, x2, z2, 20, layers=3)
    for x in range(x1, x2 + 1, 2):                                                             # snow on the cornice
        for z in (z1, z2):
            v.set(x, 20, z, "snow[layers=2]") if v.get(x, 21, z) is None else None


def _alexander_column(v: Voxel, x: int, z: int) -> None:
    """The Alexander Column: granite pedestal, red granite monolith, bronze capital and the angel with a cross."""
    v.fill(x - 4, 1, z - 4, x + 4, 1, z + 4, "polished_andesite")
    v.fill(x - 3, 2, z - 3, x + 3, 5, z + 3, "polished_granite")
    v.walls(x - 3, 4, z - 3, x + 3, 4, z + 3, "copper_block")                                  # bronze reliefs
    v.fill(x - 2, 6, z - 2, x + 2, 6, z + 2, "polished_granite")
    v.cylinder(x, 7, z, 1.5, 23, "polished_granite")
    v.fill(x - 2, 30, z - 2, x + 2, 30, z + 2, "copper_block")                                 # capital
    v.fill(x - 1, 31, z - 1, x + 1, 31, z + 1, "copper_block")
    v.column(x, 32, z, 3, "oxidized_copper")                                                   # the angel
    v.set(x - 1, 34, z, "oxidized_copper"); v.set(x + 1, 34, z, "oxidized_copper")             # wings
    v.column(x, 35, z, 3, "gold_block")                                                         # cross
    v.set(x - 1, 37, z, "gold_block"); v.set(x + 1, 37, z, "gold_block")
    for dx in (-5, 5):                                                                         # railing and lamps round it
        for dz in (-5, 5):
            _lamp(v, x + dx, 1, z + dz, post="iron_bars", h=3)
    v.walls(x - 5, 1, z - 5, x + 5, 1, z + 5, "iron_bars")
    for dx, dz in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
        v.set(x + dx, 1, z + dz, "polished_andesite")
    v.fill(x - 1, 1, z + 5, x + 1, 1, z + 5, "air")


def _general_staff(v: Voxel, x1: int, z1: int, x2: int, z2: int) -> None:
    """The General Staff building: a long yellow-ochre facade with the triumphal arch and its chariot."""
    wall, white = "yellow_terracotta", "white_concrete"
    v.fill(x1, 1, z1, x2, 14, z2, wall)
    v.fill(x1 + 1, 1, z1 + 1, x2 - 1, 14, z2 - 1, "air")
    v.fill(x1 + 1, 1, z1 + 1, x2 - 1, 1, z2 - 1, "oak_planks")
    v.fill(x1 + 1, 6, z1 + 1, x2 - 1, 6, z2 - 1, "oak_planks"); v.fill(x1 + 1, 11, z1 + 1, x2 - 1, 11, z2 - 1, "oak_planks")
    v.walls(x1, 15, z1, x2, 15, z2, white)
    v.fill(x1, 16, z1, x2, 16, z2, "polished_diorite")
    for x in range(x1, x2 + 1):
        for z in (z1, z2):
            if (x - x1) % 3 == 1:
                v.fill(x, 3, z, x, 4, z, "glass_pane"); v.fill(x, 8, z, x, 9, z, "glass_pane")
                v.fill(x, 12, z, x, 13, z, "glass_pane")
                v.set(x, 5, z, white); v.set(x, 10, z, white)
            if (x - x1) % 12 == 0:
                v.column(x, 7, z, 8, white)
    # the arch in the middle: a 7-wide passage with a double arch and the Chariot of Glory on top
    cx = (x1 + x2) // 2
    v.fill(cx - 7, 1, z1, cx + 7, 18, z2, wall)
    v.arch(cx - 4, 1, z1, 9, 10, z2 - z1 + 1, wall, axis="x")
    v.fill(cx - 7, 11, z1, cx + 7, 11, z2, white)
    v.fill(cx - 7, 19, z1, cx + 7, 19, z2, white)
    v.fill(cx - 3, 20, z1 + 1, cx + 3, 20, z2 - 1, "oxidized_copper")                          # chariot plinth
    for dx in (-3, -1, 1, 3):
        v.column(cx + dx, 21, z1 + 1, 2, "oxidized_copper")                                    # the six horses, abstracted
        v.column(cx + dx, 21, z2 - 1, 2, "oxidized_copper")
    v.fill(cx - 1, 21, z1 + 2, cx + 1, 22, z2 - 2, "oxidized_copper")
    v.column(cx, 23, (z1 + z2) // 2, 3, "oxidized_copper")                                     # Nike
    v.set(cx - 1, 25, (z1 + z2) // 2, "gold_block"); v.set(cx + 1, 25, (z1 + z2) // 2, "gold_block")
    for dx in (-5, 5):
        v.set(cx + dx, 7, z1 - 1, "lantern"); v.set(cx + dx, 6, z1 - 1, "iron_bars")
        v.set(cx + dx, 5, z1 - 1, "iron_bars"); v.set(cx + dx, 4, z1 - 1, "iron_bars"); v.set(cx + dx, 3, z1 - 1, "iron_bars")
        v.fill(cx + dx, 1, z1 - 1, cx + dx, 2, z1 - 1, "polished_andesite")
    _snow_roof(v, x1, z1, x2, z2, 16, layers=3)
    _snow_roof(v, cx - 7, z1, cx + 7, z2, 19, layers=2)


def _barricade(v: Voxel, x1: int, y: int, z: int, x2: int, seed: int = 1917) -> None:
    """A revolutionary barricade across a street: cobbles, timber, overturned carts, sandbags and red flags."""
    rng = random.Random(seed + x1 + z)
    for x in range(x1, x2 + 1):
        h = rng.choice((1, 2, 2, 3))
        for yy in range(h):
            v.set(x, y + yy, z, rng.choice(("cobblestone", "oak_log", "oak_planks", "spruce_planks", "barrel[facing=up]",
                                              "brown_wool", "cobblestone", "iron_bars", "oak_fence", "stone_bricks")))
        if rng.random() < 0.5:
            v.set(x, y, z - 1, rng.choice(("cobblestone", "brown_wool", "oak_fence", "snow_block")))
        if rng.random() < 0.25:
            v.set(x, y + h, z, "snow[layers=1]")
    v.set(x1 + 2, y + 3, z, "red_banner[rotation=8]"); v.set(x1 + 2, y, z, "oak_log"); v.set(x1 + 2, y + 1, z, "oak_log"); v.set(x1 + 2, y + 2, z, "oak_fence")
    v.set(x2 - 2, y + 2, z, "red_banner[rotation=8]"); v.set(x2 - 2, y, z, "cobblestone"); v.set(x2 - 2, y + 1, z, "oak_fence")
    v.set((x1 + x2) // 2, y, z + 1, "campfire[lit=true,facing=north]")                         # a brazier behind it


def _armoured_train(v: Voxel, x: int, z: int, length: int = 60) -> None:
    """An armoured train on a siding: engine, tender, two turreted armoured wagons and a flatcar, on real rails."""
    v.fill(x, 0, z - 2, x + length, 0, z + 2, "gravel")                                        # ballast
    for xx in range(x, x + length + 1):
        v.fill(xx, 0, z - 1, xx, 0, z + 1, "dark_oak_slab[type=top]") if xx % 2 == 0 else None
    v.fill(x, 1, z, x + length, 1, z, "rail[shape=east_west]")
    gray, dark = "gray_concrete", "black_concrete"
    cx = x + 4
    # locomotive (armoured): boiler, cab, smoke stack
    v.fill(cx, 2, z - 1, cx + 13, 2, z + 1, "iron_block")                                       # frame
    v.fill(cx, 1, z - 1, cx + 13, 1, z - 1, "polished_blackstone") if False else None
    v.cylinder(cx + 7, 4, z, 1.5, 1, dark) if False else None
    v.fill(cx + 1, 3, z - 1, cx + 9, 5, z + 1, dark)                                            # boiler armour
    v.fill(cx + 10, 3, z - 1, cx + 13, 6, z + 1, gray)                                          # cab
    v.set(cx + 11, 5, z - 1, "glass_pane") if False else None
    v.set(cx + 11, 5, z - 2, "iron_bars"); v.set(cx + 11, 5, z + 2, "iron_bars")
    v.fill(cx + 10, 7, z - 1, cx + 13, 7, z + 1, dark)
    v.column(cx + 2, 6, z, 2, dark)                                                             # stack
    v.set(cx + 2, 8, z, "campfire[lit=true,facing=north]")                                     # smoke
    v.set(cx, 3, z, "iron_block"); v.set(cx, 4, z, "lantern")                                   # headlamp
    for wx in range(cx + 1, cx + 13, 3):                                                        # wheels
        v.set(wx, 1, z - 1, "iron_bars"); v.set(wx, 1, z + 1, "iron_bars")
    v.fill(cx + 14, 2, z - 1, cx + 19, 4, z + 1, gray)                                          # tender
    v.fill(cx + 15, 5, z - 1, cx + 18, 5, z + 1, "coal_block")
    # two armoured wagons with gun turrets and firing slits
    for wx in (cx + 21, cx + 34):
        v.fill(wx, 2, z - 1, wx + 11, 6, z + 1, gray)
        v.fill(wx + 1, 3, z - 2, wx + 10, 3, z - 2, "iron_bars") if False else None
        for i in range(1, 11, 2):
            v.set(wx + i, 4, z - 1, "iron_trapdoor[facing=north,half=top,open=false]") if False else None
            v.set(wx + i, 4, z - 2, "iron_bars"); v.set(wx + i, 4, z + 2, "iron_bars")
        v.cylinder(wx + 5, 7, z, 1.5, 2, dark)                                                 # turret
        v.fill(wx + 5, 8, z + 2, wx + 5, 8, z + 4, "iron_bars") if False else None
        v.fill(wx + 5, 8, z - 4, wx + 5, 8, z - 2, "polished_blackstone_wall") if False else None
        v.set(wx + 5, 8, z - 2, "end_rod[facing=north]")                                       # gun barrel
        v.set(wx + 5, 8, z - 3, "end_rod[facing=north]")
        v.set(wx + 2, 7, z, "red_banner[rotation=4]")
        v.fill(wx, 7, z - 1, wx + 11, 7, z + 1, "snow[layers=2]")
        v.fill(wx + 4, 7, z - 1, wx + 6, 7, z + 1, "air")
        for i in range(1, 11, 3):
            v.set(wx + i, 1, z - 1, "iron_bars"); v.set(wx + i, 1, z + 1, "iron_bars")
    # a flatcar with sandbags and a field gun
    fx = cx + 47
    v.fill(fx, 2, z - 1, fx + 9, 2, z + 1, "spruce_planks")
    v.fill(fx, 3, z - 1, fx + 9, 3, z - 1, "brown_wool"); v.fill(fx, 3, z + 1, fx + 9, 3, z + 1, "brown_wool")
    v.set(fx + 4, 3, z, "anvil[facing=north]"); v.set(fx + 4, 4, z, "end_rod[facing=north]")
    v.set(fx + 4, 4, z - 1, "end_rod[facing=north]")
    v.set(fx + 1, 3, z, "campfire[lit=true,facing=north]"); v.set(fx + 8, 3, z, "barrel[facing=up]")
    # buffer stop at the end of the siding
    v.fill(x + length - 1, 1, z - 1, x + length, 2, z + 1, "spruce_log[axis=z]")
    v.fill(x + length - 1, 1, z, x + length, 1, z, "rail[shape=east_west]")


def petrograd(v: Voxel) -> None:
    """Revolutionary Petrograd 1918: a Kremlin-style wall, an onion-domed cathedral and the Winter Palace facade (Nikolai Orelov's Russia)."""
    S.pad(v, -80, -60, 80, 60, "snow_block")
    rng = random.Random(1918)
    # ---- the frozen Neva along the north edge, with its granite embankment and the Palace Bridge
    v.fill(-80, -1, -60, 80, -1, -47, "water")
    v.fill(-80, 0, -60, 80, 0, -47, "packed_ice")
    for _ in range(260):
        x = rng.randint(-80, 80); z = rng.randint(-60, -47)
        v.set(x, 0, z, rng.choice(("ice", "blue_ice", "packed_ice", "snow_block")))
    for _ in range(90):
        x = rng.randint(-80, 80); z = rng.randint(-60, -48)
        v.set(x, 1, z, f"snow[layers={rng.randint(1, 3)}]")
    v.fill(-80, 0, -46, 80, 1, -46, "polished_andesite")                                        # granite quay
    v.fill(-80, 0, -45, 80, 0, -45, "stone_bricks")
    v.fill(-80, 2, -46, 80, 2, -46, "iron_bars")                                                 # railing
    for x in range(-78, 79, 12):
        v.set(x, 2, -46, "polished_andesite"); _lamp(v, x, 3, -46, post="iron_bars", h=2)
    for x in range(-74, 79, 24):                                                                 # steps down to the ice
        v.set(x, 0, -47, "stone_brick_stairs[facing=south,half=bottom]")
        v.set(x, 2, -46, "air"); v.set(x, 1, -46, "stone_brick_stairs[facing=south,half=bottom]")
    # Palace Bridge: stone piers, iron deck and railings, lamps, a raised bascule leaf
    bx = -58
    v.fill(bx - 4, 0, -60, bx + 4, 2, -47, "polished_andesite")
    v.fill(bx - 3, 0, -60, bx + 3, 2, -47, "air")
    v.fill(bx - 3, 0, -60, bx + 3, 0, -47, "packed_ice")
    v.fill(bx - 3, 2, -60, bx + 3, 2, -47, "polished_andesite")
    v.fill(bx - 3, 1, -60, bx + 3, 1, -47, "stone_bricks")
    v.fill(bx - 4, 3, -60, bx - 4, 3, -47, "iron_bars"); v.fill(bx + 4, 3, -60, bx + 4, 3, -47, "iron_bars")
    for z in range(-59, -47, 4):
        v.set(bx - 4, 3, z, "polished_andesite"); v.set(bx + 4, 3, z, "polished_andesite")
        v.set(bx - 4, 4, z, "lantern"); v.set(bx + 4, 4, z, "lantern")
    for z in (-56, -51):                                                                         # piers in the ice
        v.fill(bx - 5, -1, z - 1, bx + 5, 0, z + 1, "stone_bricks")
        v.set(bx - 5, 1, z, "lantern"); v.set(bx + 5, 1, z, "lantern")
    v.fill(bx - 3, 2, -60, bx + 3, 2, -58, "snow[layers=2]") if False else None
    v.set(bx, 2, -47, "stone_brick_stairs[facing=south,half=bottom]")
    v.fill(bx - 4, 0, -46, bx + 4, 2, -46, "polished_andesite"); v.fill(bx - 3, 1, -46, bx + 3, 2, -46, "air")
    v.fill(bx - 3, 1, -46, bx + 3, 1, -46, "stone_bricks") if False else None
    v.fill(bx - 3, 1, -46, bx + 3, 1, -46, "polished_andesite")
    # ---- the Winter Palace between the river and the square
    _winter_palace(v, -78, -40, 78, -24)
    # ---- Palace Square: granite setts, the Alexander Column, the General Staff arch, barricades and banners
    for x in range(-78, 79):
        for z in range(-22, 13):
            d = math.hypot(x, z + 5)
            v.set(x, 0, z, "polished_andesite" if int(d) % 6 == 0 else ("stone_bricks" if (x + z) % 2 else "andesite"))
    for x in range(-78, 79):                                                                     # fresh snow on the setts
        for z in range(-22, 13):
            if rng.random() < 0.08:
                v.set(x, 1, z, "snow[layers=1]")
    _alexander_column(v, 0, -5)
    _general_staff(v, -78, 14, 78, 24)
    for x in range(-72, 79, 24):                                                                 # square lamps
        _lamp(v, x, 1, -21, post="iron_bars", h=3)
        _lamp(v, x, 1, 12, post="iron_bars", h=3)
    _barricade(v, -40, 1, -14, -18)
    _barricade(v, 16, 1, 2, 40)
    _barricade(v, -8, 1, 10, 8, seed=3)
    for x in (-30, -20, 20, 30):                                                                  # banners on the square
        v.column(x, 1, 0, 4, "oak_fence"); v.set(x, 5, 0, "red_banner[rotation=8]")
    # ---- behind the General Staff: the fortress with its cathedral (west) and the rail yard (east)
    S.curtain_wall(v, -78, 28, -14, 58, 9, {**RUSSIA, "wall": "bricks"}, gate="north", tower_r=4)
    for (x, z) in ((-78, 28), (-14, 28), (-78, 58), (-14, 58)):
        v.cone(x, 14, z, 5, 10, "green_terracotta")
        v.set(x, 24, z, "gold_block")
        v.set(x, 25, z, "end_rod[facing=up]")
        _snow_roof(v, x - 5, z - 5, x + 5, z + 5, 15, layers=2)
    v.fill(-47, 1, 28, -45, 4, 29, "air")                                                        # gate to the square
    v.set(-48, 5, 27, "lantern"); v.set(-44, 5, 27, "lantern")
    v.set(-48, 4, 27, "iron_bars"); v.set(-44, 4, 27, "iron_bars")
    v.set(-48, 3, 27, "iron_bars"); v.set(-44, 3, 27, "iron_bars"); v.set(-48, 2, 27, "iron_bars"); v.set(-44, 2, 27, "iron_bars")
    v.set(-48, 1, 27, "polished_andesite"); v.set(-44, 1, 27, "polished_andesite")
    # the cathedral with five onion domes
    cx, cz = -46, 44
    v.fill(cx - 12, 1, cz - 12, cx + 12, 14, cz + 12, "white_concrete")
    v.fill(cx - 11, 1, cz - 11, cx + 11, 13, cz + 11, "air")
    v.fill(cx - 11, 1, cz - 11, cx + 11, 1, cz + 11, RUSSIA["floor"])
    for i in range(-9, 10, 6):                                                                   # tall arched windows
        for (x, z) in ((cx + i, cz - 12), (cx + i, cz + 12), (cx - 12, cz + i), (cx + 12, cz + i)):
            v.fill(x, 4, z, x, 9, z, "glass_pane"); v.set(x, 10, z, "gold_block")
    v.walls(cx - 12, 15, cz - 12, cx + 12, 15, cz + 12, "gold_block")                             # kokoshnik band
    v.fill(cx - 11, 15, cz - 11, cx + 11, 15, cz + 11, "lime_terracotta")
    for (dx, dz, r, c) in ((0, 0, 5, "gold_block"), (-8, -8, 3, "blue_concrete"), (8, -8, 3, "lime_concrete"),
                           (-8, 8, 3, "red_concrete"), (8, 8, 3, "yellow_concrete")):
        _onion_dome(v, cx + dx, 16, cz + dz, r, c)
    v.fill(cx - 2, 1, cz - 12, cx + 2, 5, cz - 12, "air")                                        # west door toward the gate
    v.set(cx - 3, 3, cz - 13, "wall_torch[facing=north]"); v.set(cx + 3, 3, cz - 13, "wall_torch[facing=north]")
    v.fill(cx - 11, 1, cz - 11, cx + 11, 1, cz + 11, "red_carpet") if False else None
    v.fill(cx - 1, 1, cz - 11, cx + 1, 1, cz + 11, "red_carpet")
    for i in range(-8, 9, 4):                                                                    # candle stands / chandeliers
        v.set(cx + i, 13, cz, "lantern[hanging=true]")
        v.set(cx - 8, 2, cz + i, "gold_block"); v.set(cx - 8, 3, cz + i, "lantern")
        v.set(cx + 8, 2, cz + i, "gold_block"); v.set(cx + 8, 3, cz + i, "lantern")
    v.fill(cx - 5, 2, cz + 8, cx + 5, 6, cz + 9, "gold_block")                                    # iconostasis
    for i in range(-4, 5, 2):
        v.set(cx + i, 3, cz + 8, "red_concrete"); v.set(cx + i, 5, cz + 8, "blue_concrete")
    v.fill(cx - 11, 14, cz - 11, cx + 11, 14, cz + 11, "white_concrete")
    _snow_roof(v, cx - 12, cz - 12, cx + 12, cz + 12, 15, layers=2)
    # rows of snowbound trees in the fortress yard and a guard post
    for (x, z) in ((-72, 34), (-72, 52), (-22, 34), (-22, 52), (-30, 40), (-66, 44)):
        v.tree(x, 1, z, "spruce_log", "spruce_leaves[persistent=true]", height=6, canopy=2)
        v.set(x, 9, z, "snow_block")
    v.set(-60, 1, 32, "campfire[lit=true,facing=north]")
    v.set(-61, 1, 32, "barrel[facing=up]"); v.set(-59, 1, 32, "hay_block")
    # ---- the rail yard east of the arch: the armoured train, a platform, a water tower, a signal box
    v.fill(-8, 0, 28, 78, 0, 60, "gravel")
    for x in range(-8, 79):
        for z in range(28, 61):
            if rng.random() < 0.3:
                v.set(x, 0, z, "snow_block")
    _armoured_train(v, 10, 44, length=66)
    v.fill(-8, 0, 36, 78, 0, 36, "rail[shape=east_west]") if False else None
    v.fill(-6, 1, 48, 78, 1, 52, "stone_bricks")                                                 # platform
    v.fill(-6, 1, 52, 78, 1, 52, "stone_brick_slab[type=bottom]") if False else None
    for x in range(-4, 78, 8):                                                                   # canopy posts and lamps
        v.column(x, 2, 51, 4, "iron_bars"); v.set(x, 6, 51, "lantern")
    v.fill(-6, 6, 50, 78, 6, 52, "spruce_slab[type=top]") if False else None
    v.fill(-6, 7, 50, 78, 7, 52, "dark_oak_planks")
    _snow_roof(v, -6, 50, 78, 52, 7, layers=3)
    for x in range(0, 78, 12):                                                                   # crates and sacks on the platform
        v.set(x, 2, 49, "barrel[facing=up]"); v.set(x + 1, 2, 49, "hay_block"); v.set(x + 1, 2, 50, "barrel[facing=up]")
    for x in range(4, 78, 20):
        v.column(x, 2, 49, 3, "oak_fence"); v.set(x, 5, 49, "red_banner[rotation=8]")
    # water tower
    v.cylinder(70, 1, 34, 3, 8, "bricks", hollow=True)
    v.cylinder(70, 9, 34, 4, 4, "iron_block", hollow=True)
    v.disc(70, 13, 34, 4, "iron_block"); v.disc(70, 14, 34, 4, "snow_block")
    v.fill(70, 9, 34, 70, 12, 34, "water")
    v.set(70, 1, 37, "air"); v.set(70, 2, 37, "air")
    # signal box with a stove, and a lit semaphore
    v.fill(-6, 1, 30, 0, 1, 34, "bricks")
    v.fill(-6, 2, 30, 0, 5, 34, "spruce_planks")
    v.fill(-5, 2, 31, -1, 5, 33, "air")
    v.fill(-5, 3, 30, -1, 4, 30, "glass_pane") if False else None
    for x in range(-5, 0):
        v.set(x, 3, 34, "glass_pane"); v.set(x, 4, 34, "glass_pane")
    v.fill(-6, 6, 30, 0, 6, 34, "dark_oak_planks")
    _snow_roof(v, -6, 30, 0, 34, 6, layers=3)
    v.set(-3, 2, 32, "lantern"); v.set(-5, 2, 31, "furnace[facing=south]"); v.set(-5, 6, 31, "air"); v.set(-5, 7, 31, "bricks")
    v.set(-5, 8, 31, "campfire[lit=true,facing=north]")
    v.column(4, 1, 40, 7, "iron_bars"); v.set(4, 8, 40, "red_concrete"); v.set(4, 7, 41, "redstone_torch")
    # ---- streets around the square: lamps, kiosks, a sentry's brazier, red banners on the facades
    for z in range(-20, 13, 8):
        _lamp(v, -79, 1, z, post="iron_bars", h=3); _lamp(v, 79, 1, z, post="iron_bars", h=3)
    for x in (-60, 60):
        v.fill(x - 1, 1, 6, x + 1, 3, 8, "dark_oak_planks")                                       # newspaper kiosk
        v.fill(x - 1, 2, 8, x + 1, 2, 8, "glass_pane") if False else None
        v.set(x, 2, 8, "glass_pane")
        v.fill(x - 2, 4, 5, x + 2, 4, 9, "spruce_slab[type=bottom]")
        v.set(x, 5, 7, "snow[layers=3]")
        v.set(x - 2, 1, 9, "lantern"); v.set(x + 2, 1, 9, "campfire[lit=true,facing=north]")
    for x in (-40, 40):
        v.column(x, 1, 24, 0, "air")
    # frozen snow drifts along the embankment and the square's north edge
    for x in range(-78, 79, 3):
        if rng.random() < 0.6:
            v.set(x, 1, -44, f"snow[layers={rng.randint(2, 5)}]")
            v.set(x, 1, -43, f"snow[layers={rng.randint(1, 3)}]")


WORLD = World(
    id="chronicles",
    name="Assassin's Creed Chronicles",
    game="AC Chronicles: China (2015), India (2016), Russia (2016)",
    era="1526, 1841 and 1918",
    description="Shao Jun's Ming China, Arbaaz Mir's Sikh Empire and Nikolai Orelov's revolutionary Russia.",
).build(Build("great_wall", "The Great Wall", "A Ming stretch of wall over rolling hills with beacon towers and a palace gate hall.", great_wall)
).build(Build("amritsar", "Amritsar", "The Golden Temple in its sacred pool with the causeway, plus a stepwell.", amritsar)
).build(Build("petrograd", "Petrograd", "Kremlin-style wall, an onion-domed cathedral, the Winter Palace facade and an armoured train.", petrograd))
