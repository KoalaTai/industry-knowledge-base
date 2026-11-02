"""Insomniac Events (1993-2026) - EDC Las Vegas, Beyond Wonderland, Escape, Nocturnal.

Festival stages cannot animate their LEDs in a datapack, so each build leans
on silhouette: big black truss frames, striped LED banks, end-rod spires and
a crowd field to the south of the stage so the player (standing at the
origin) looks north at the front of house.
"""

import math
import random

from .. import structures as S
from ..palettes import _p
from ..registry import Build, World
from ..voxel import Voxel

STAGE = _p(ground="grass_block", wall="black_concrete", wall2="gray_concrete", trim="white_concrete",
           roof="black_concrete", floor="gray_concrete", column="black_concrete", path="gray_concrete",
           light="sea_lantern", window="glowstone")
LED = ["sea_lantern", "magenta_stained_glass", "cyan_stained_glass", "glowstone",
       "yellow_stained_glass", "purple_stained_glass"]
LED_WARM = ["glowstone", "orange_stained_glass", "sea_lantern", "red_stained_glass", "yellow_stained_glass"]
LED_COOL = ["sea_lantern", "cyan_stained_glass", "blue_stained_glass", "glowstone", "light_blue_stained_glass"]
TRUSS = "black_concrete"
LEAVES = "jungle_leaves[persistent=true]"


# ----------------------------------------------------------------- helpers

def _led(v: Voxel, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
         colors=LED, mode: str = "y", band: int = 2) -> None:
    """LED bank: horizontal (mode y) or vertical (mode x) stripes of light blocks."""
    xa, xb = sorted((x1, x2)); ya, yb = sorted((y1, y2)); za, zb = sorted((z1, z2))
    for y in range(ya, yb + 1):
        for x in range(xa, xb + 1):
            k = (y - ya) // band if mode == "y" else (x - xa) // band
            if mode == "xy":
                k = (x - xa) // band + (y - ya) // band
            b = colors[k % len(colors)]
            for z in range(za, zb + 1):
                v.set(x, y, z, b)


def _vring(v: Voxel, u: int, cy: int, w: int, r: float, block: str,
           a1: float = 0.0, a2: float = 360.0, axis: str = "z") -> None:
    """Vertical ring.  axis 'z': in the x-y plane at z=w centred on x=u; axis 'x': z-y plane at x=w."""
    n = max(12, int(abs(a2 - a1) / 360.0 * 2 * math.pi * r * 1.5))
    for i in range(n + 1):
        a = math.radians(a1 + (a2 - a1) * i / n)
        du, dy = round(r * math.cos(a)), round(r * math.sin(a))
        if axis == "z":
            v.set(u + du, cy + dy, w, block)
        else:
            v.set(w, cy + dy, u + du, block)


def _vdisc(v: Voxel, cx: int, cy: int, z: int, r: float, block: str, depth: int = 1) -> None:
    """Filled vertical disc in the x-y plane, ``depth`` blocks thick towards +z."""
    for x in range(cx - int(r) - 1, cx + int(r) + 2):
        for y in range(cy - int(r) - 1, cy + int(r) + 2):
            if (x - cx) ** 2 + (y - cy) ** 2 <= (r + 0.5) ** 2:
                v.fill(x, y, z, x, y, z + depth - 1, block)


def _prune(v: Voxel, pred) -> None:
    for c in [c for c in v.blocks if pred(*c)]:
        del v.blocks[c]


def _truss(v: Voxel, x: int, z: int, h: int, w: int = 2, block: str = TRUSS, y: int = 1) -> None:
    v.fill(x, y, z, x + w - 1, y + h - 1, z + w - 1, block)


def _spire(v: Voxel, x: int, y: int, z: int, h: int = 6) -> None:
    v.fill(x, y, z, x, y + h - 1, z, "end_rod")


def _light_tower(v: Voxel, x: int, z: int, h: int = 18) -> None:
    """White lighting / delay tower with a black head whose south face glows."""
    v.fill(x, 1, z, x + 1, h, z + 1, "white_concrete")
    v.fill(x - 1, h + 1, z - 1, x + 2, h + 3, z + 2, "black_concrete")
    v.fill(x - 1, h + 1, z + 2, x + 2, h + 3, z + 2, "glowstone")


def _pyro(v: Voxel, x: int, z: int, h: int = 8) -> None:
    v.fill(x, 1, z, x, h, z, "black_concrete")
    v.set(x, h + 1, z, "netherrack")
    v.set(x, h + 2, z, "fire")


def _portaloos(v: Voxel, x: int, z: int, n: int) -> None:
    for i in range(n):
        v.fill(x + i * 2, 1, z, x + i * 2, 2, z, "blue_concrete")
        v.set(x + i * 2, 3, z, "white_concrete")


def _field(v: Voxel, x1: int, z1: int, x2: int, z2: int, ground: str = "grass_block",
           gate: int = 12) -> None:
    """Crowd field with a perimeter fence, open in the middle of the south edge."""
    S.pad(v, x1, z1, x2, z2, ground)
    v.walls(x1, 1, z1, x2, 1, z2, "oak_fence")
    cx = (x1 + x2) // 2
    for x in range(cx - gate // 2, cx + gate // 2 + 1):
        v.blocks.pop((x, 1, z2), None)


def _deck(v: Voxel, x1: int, z1: int, x2: int, z2: int, h: int = 3) -> None:
    """Stage deck with a DJ table at the front (south) edge."""
    v.fill(x1, 1, z1, x2, h, z2, "black_concrete")
    cx = (x1 + x2) // 2
    v.fill(cx - 4, h + 1, z2 - 3, cx + 4, h + 2, z2 - 2, "gray_concrete")
    v.fill(cx - 4, h + 1, z2 - 1, cx + 4, h + 2, z2 - 1, "sea_lantern")
    for x in (x1 + 2, x2 - 2):                                   # PA hangs
        v.fill(x - 1, h + 1, z2 - 2, x + 1, h + 12, z2, "black_concrete")


def _ferris(v: Voxel, cx: int, z: int, r: int) -> None:
    cy = r + 3
    cars = ("red_stained_glass", "lime_stained_glass", "light_blue_stained_glass", "magenta_stained_glass")
    for zz in (z, z + 2):
        _vring(v, cx, cy, zz, r, "white_concrete")
        for a in range(0, 360, 30):
            v.line((cx, cy, zz), (round(cx + r * math.cos(math.radians(a))),
                                  round(cy + r * math.sin(math.radians(a))), zz), "iron_bars")
    v.fill(cx - 1, cy - 1, z, cx + 1, cy + 1, z + 2, "yellow_concrete")
    for i, a in enumerate(range(0, 360, 30)):
        gx = round(cx + r * math.cos(math.radians(a))); gy = round(cy + r * math.sin(math.radians(a)))
        v.fill(gx - 1, gy - 2, z, gx + 1, gy - 1, z + 2, cars[i % 4])
    for zz in (z - 1, z + 3):                                     # A-frame legs
        v.line((cx - r // 2, 1, zz), (cx, cy, zz), "white_concrete")
        v.line((cx + r // 2, 1, zz), (cx, cy, zz), "white_concrete")
    v.fill(cx - r // 2 - 1, 0, z - 2, cx + r // 2 + 1, 0, z + 4, "gray_concrete")


_FONT = {
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
}


def _text(v: Voxel, text: str, x: int, y: int, z: int, block: str, scale: int = 1) -> int:
    """Block letters in the x-y plane; returns the x after the last letter."""
    for ch in text:
        rows = _FONT.get(ch)
        if rows:
            for ry, row in enumerate(rows):
                for rx, c in enumerate(row):
                    if c == "#":
                        v.fill(x + rx * scale, y + (6 - ry) * scale, z,
                               x + rx * scale + scale - 1, y + (6 - ry) * scale + scale - 1, z, block)
        x += 6 * scale
    return x


def _owl(v: Voxel, cx: int, cy: int, z: int, r: int) -> None:
    """The EDC owl: round grey face, yellow eyes, orange beak, ear tufts.  Faces +z."""
    _vdisc(v, cx, cy, z, r, "gray_concrete", depth=2)
    for sx in (-1, 1):
        ex, ey = cx + sx * int(r * 0.45), cy + int(r * 0.2)
        _vdisc(v, ex, ey, z + 1, r * 0.3, "yellow_stained_glass", depth=2)
        _vdisc(v, ex, ey, z + 2, r * 0.12, "black_concrete", depth=1)
    for k in range(int(r * 0.35)):                                                         # beak
        hw = max(0, int(r * 0.12) - k // 2)
        v.fill(cx - hw, cy - int(r * 0.1) - k, z + 2, cx + hw, cy - int(r * 0.1) - k, z + 2, "orange_concrete")
    tuft = int(r * 0.4)
    for sx in (-1, 1):                                                                       # ear tufts
        for k in range(tuft):
            hw = (tuft - k) // 2
            x0 = cx + sx * int(r * 0.65)
            v.fill(x0 - hw, cy + int(r * 0.75) + k, z, x0 + hw, cy + int(r * 0.75) + k, z + 1, "gray_concrete")


def _sun(v: Voxel, cx: int, cy: int, z: int, r: int) -> None:
    """Smiling sun face with alternating long / short rays.  Faces +z."""
    _vdisc(v, cx, cy, z, r, "yellow_concrete", depth=2)
    _vring(v, cx, cy, z + 1, r, "orange_concrete")
    for i, a in enumerate(range(0, 360, 15)):
        length = r * (0.6 if i % 2 else 0.3)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        v.line((round(cx + (r + 1) * ca), round(cy + (r + 1) * sa), z),
               (round(cx + (r + length) * ca), round(cy + (r + length) * sa), z), "orange_concrete")
    for sx in (-1, 1):
        ex = cx + sx * int(r * 0.4)
        v.fill(ex - 1, cy + int(r * 0.25), z + 1, ex + 1, cy + int(r * 0.25) + 2, z + 1, "black_concrete")
    _vring(v, cx, cy, z + 1, r * 0.5, "black_concrete", a1=200, a2=340)


def _flower(v: Voxel, x: int, z: int, h: int, r: float, petal: str, centre: str = "yellow_concrete",
            stem: str = "lime_concrete") -> None:
    """Meadow daisy: stem, a flat petal disc and a dark centre."""
    v.column(x, 1, z, h, stem)
    v.disc(x, h + 1, z, r, petal)
    v.disc(x, h + 1, z, r * 0.4, centre)
    v.set(x, h + 2, z, centre)


def _scaffold_wall(v: Voxel, x1: int, z: int, x2: int, h: int, step: int = 8) -> None:
    """A row of truss columns with a top beam: the backbone of a festival stage."""
    for x in range(x1, x2 + 1, step):
        _truss(v, x, z, h)
    v.fill(x1, h + 1, z, x2 + 1, h + 1, z + 1, TRUSS)


# ------------------------------------------------------------------ EDC LV

def kineticfield(v: Voxel) -> None:
    """kineticFIELD as it stood in 2024: the kineticCIRCLE revival of kineticCATHEDRAL - a cathedral
    facade with a giant circular LED rose window carrying the owl, organ-pipe spires along the roofline,
    two tall pylons, pyro towers, and the Ferris wheel and EDC sign in the distance."""
    _field(v, -110, -12, 110, 110)
    v.fill(-110, 0, -90, 110, 0, -13, "gray_concrete")                   # backstage asphalt
    # facade: wall, LED wings, circular window with the owl, organ pipes
    v.fill(-72, 1, -50, 72, 48, -47, "black_concrete")
    v.fill(-74, 1, -50, -72, 56, -47, "black_concrete"); v.fill(72, 1, -50, 74, 56, -47, "black_concrete")
    _led(v, -70, 4, -46, -26, 44, -46, LED, mode="y", band=3)
    _led(v, 26, 4, -46, 70, 44, -46, LED, mode="y", band=3)
    for x in (-48, 48):                                                    # gothic window tracery
        v.fill(x, 4, -45, x, 44, -45, "white_concrete")
        for y in range(8, 44, 9):
            v.fill(x - 22, y, -45, x + 22, y, -45, "white_concrete")
    _vdisc(v, 0, 27, -46, 23, "black_concrete", depth=1)
    _vring(v, 0, 27, -45, 22, "sea_lantern"); _vring(v, 0, 27, -45, 21, "magenta_stained_glass")
    _owl(v, 0, 27, -45, 18)
    for i, x in enumerate(range(-64, 65, 4)):                             # organ pipes
        h = 8 + int(22 * math.cos(math.radians(x * 1.3)))
        v.fill(x, 49, -49, x + 1, 48 + h, -48, "white_concrete" if i % 2 else "light_gray_concrete")
        _spire(v, x, 49 + h, -49, 5)
    for x in (-73, 73):
        _spire(v, x, 57, -49, 10)
    # the two pylons
    for x in (-96, 92):
        _truss(v, x, -52, 74, w=4)
        _led(v, x, 6, -48, x + 3, 70, -48, LED_COOL, mode="y", band=4)
        v.fill(x - 2, 75, -54, x + 5, 76, -47, "black_concrete")
        _spire(v, x + 1, 77, -50, 12); _spire(v, x + 2, 77, -51, 12)
    # stage deck, pyro and PA
    _deck(v, -44, -47, 44, -16, 4)
    for x in (-60, -40, -20, 20, 40, 60):
        _pyro(v, x, -12, 9)
    for x, z in ((-70, 20), (70, 20), (-70, 70), (70, 70), (0, 60)):
        _light_tower(v, x, z, 20)
    v.fill(-46, 1, -10, -52, 2, 30, "black_concrete"); v.fill(46, 1, -10, 52, 2, 30, "black_concrete")   # barricade
    # the Ferris wheel and the EDC sign in the distance behind the stage
    _ferris(v, 94, -82, 16)
    for x in (-104, -74):
        v.fill(x, 1, -84, x + 1, 24, -83, "white_concrete")
    v.fill(-105, 25, -85, -69, 25, -82, "black_concrete")
    _text(v, "EDC", -103, 27, -83, "glowstone", scale=2)
    _owl(v, -86, 50, -84, 8)
    _portaloos(v, -100, 106, 18); _portaloos(v, 64, 106, 18)


def cosmicmeadow(v: Voxel) -> None:
    """cosmicMEADOW in its 2023-2024 form: a 150-block-wide low LED wall under a truss canopy on the
    speedway infield grass, flanked by giant daisies and sunflowers in the meadow."""
    _field(v, -105, -10, 105, 110)
    v.fill(-105, 0, -70, 105, 0, -11, "gray_concrete")
    _scaffold_wall(v, -76, -48, 76, 30, step=8)
    v.fill(-76, 1, -48, 77, 2, -40, "black_concrete")
    _led(v, -74, 3, -46, 74, 28, -46, LED, mode="x", band=6)
    v.fill(-74, 15, -45, 74, 15, -45, "black_concrete")                   # horizontal split
    _led(v, -74, 29, -46, 74, 30, -46, ["sea_lantern"], mode="y")
    for z in range(-44, -20, 4):                                           # canopy over the deck
        v.fill(-78, 31, z, 78, 31, z, TRUSS)
    v.fill(-78, 31, -45, -78, 31, -22, TRUSS); v.fill(78, 31, -45, 78, 31, -22, TRUSS)
    for x in (-78, 78):
        _truss(v, x, -24, 30)
    _deck(v, -60, -40, 60, -14, 3)
    for x in (-50, -25, 0, 25, 50):
        _pyro(v, x, -11, 8)
    rng = random.Random(7)
    petals = ("white_concrete", "yellow_concrete", "pink_concrete", "orange_concrete", "magenta_concrete")
    for i in range(16):                                                    # the meadow art
        side = -1 if i % 2 else 1
        x = side * rng.randint(70, 100); z = -40 + i * 9
        _flower(v, x, z, rng.randint(8, 18), rng.randint(3, 6), rng.choice(petals),
                centre="black_concrete" if rng.random() < .4 else "yellow_concrete")
    for x, z in ((-85, 100), (85, 100), (0, 95)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -100, 106, 14); _portaloos(v, 74, 106, 14)


def circuitgrounds(v: Voxel) -> None:
    """circuitGROUNDS in its 2016-2024 panoramic form: a stage wall under a spine of five truss arches
    that span the whole dance floor like a spaceship frame, each hung with LED panels."""
    _field(v, -90, -50, 90, 100, ground="gray_concrete")
    _scaffold_wall(v, -62, -58, 62, 32, step=8)
    v.fill(-62, 1, -58, 63, 2, -50, "black_concrete")
    _led(v, -60, 3, -56, 60, 30, -56, LED, mode="y", band=2)
    _deck(v, -44, -50, 44, -24, 4)
    r = 60
    for k, z in enumerate((-42, -22, -2, 18, 38)):
        _vring(v, 0, 1, z, r, TRUSS, 0, 180); _vring(v, 0, 1, z + 1, r, TRUSS, 0, 180)
        _vring(v, 0, 1, z, r - 2, TRUSS, 0, 180)
        _vring(v, 0, 1, z + 1, r - 1, (LED_COOL if k % 2 else LED)[k % 5], 0, 180)
        for a in range(20, 161, 20):                                        # hanging LED panels
            px = round(r * math.cos(math.radians(a))); py = round(1 + r * math.sin(math.radians(a)))
            _led(v, px - 3, py - 8, z - 1, px + 3, py - 3, z - 1, LED, mode="y")
            v.fill(px, py - 2, z - 1, px, py - 1, z - 1, "iron_bars")
        for sx in (-1, 1):                                                   # footings
            v.fill(sx * r - 2, 1, z - 1, sx * r + 2, 4, z + 2, TRUSS)
    for a in (30, 60, 90, 120, 150):                                         # longitudinal spine
        px = round(r * math.cos(math.radians(a))); py = round(1 + r * math.sin(math.radians(a)))
        v.fill(px, py, -42, px, py, 39, TRUSS)
        v.fill(px, py + 1, -42, px, py + 1, 39, "sea_lantern")
    for x, z in ((-80, 60), (80, 60), (-80, -10), (80, -10)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -86, 96, 12); _portaloos(v, 62, 96, 12)


def neongarden(v: Voxel) -> None:
    """neonGARDEN in 2024, back under a megastructure for the first time since 2021: an enclosed
    truss hall with a white roof, LED side bands, the hanging light cube over the floor and CO2 smoke
    towers around the outside."""
    _field(v, -90, -90, 90, 90)
    x1, x2, z1, z2 = -46, 46, -72, 12
    v.fill(x1, 0, z1, x2, 0, z2, "gray_concrete")
    for x in range(x1, x2 + 1, 10):
        _truss(v, x, z1, 24); _truss(v, x, z2 - 1, 24)
    for z in range(z1, z2 + 1, 10):
        _truss(v, x1, z, 24); _truss(v, x2 - 1, z, 24)
    v.fill(x1, 25, z1, x2 + 1, 25, z2 + 1, TRUSS, hollow=True)
    v.fill(x1 - 1, 26, z1 - 1, x2 + 2, 26, z2 + 2, "white_concrete")
    for z in range(z1 + 2, z2, 12):                                        # roof ridges
        v.fill(x1 - 1, 27, z, x2 + 2, 27, z, "white_concrete")
    _led(v, x1, 18, z1 + 2, x1, 23, z2 - 2, LED, mode="y")                 # side LED bands
    _led(v, x2, 18, z1 + 2, x2, 23, z2 - 2, LED, mode="y")
    _led(v, x1 + 2, 18, z1, x2 - 2, 23, z1, LED, mode="y")
    v.fill(x1 + 2, 1, z1 - 2, x2 - 2, 4, z1 - 2, "black_concrete")
    _led(v, x1 + 4, 2, z1 + 1, x2 - 4, 16, z1 + 1, LED_COOL, mode="xy", band=3)
    _deck(v, x1 + 6, z1 + 2, x2 - 6, z1 + 16, 3)
    # the hanging cube
    cx, cy, cz = 0, 14, -30
    v.fill(cx - 5, cy - 5, cz - 5, cx + 5, cy + 5, cz + 5, "sea_lantern", hollow=True)
    v.fill(cx - 4, cy - 4, cz - 4, cx + 4, cy + 4, cz + 4, "cyan_stained_glass", hollow=True)
    for dx, dz in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
        v.fill(cx + dx, cy + 6, cz + dz, cx + dx, 25, cz + dz, "iron_bars")
    for x, z in ((-56, -70), (56, -70), (-56, -30), (56, -30), (-56, 10), (56, 10)):
        v.fill(x, 1, z, x + 1, 30, z + 1, "white_concrete")
        v.sphere(x, 33, z, 3, "white_wool", hollow=False)
    for x, z in ((-80, 50), (80, 50)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -86, 86, 12); _portaloos(v, 62, 86, 12)


def basspod(v: Voxel) -> None:
    """bassPOD in its 2022-2025 dome form: a geodesic half-dome of black truss open to the south, a
    dense LED front between bass stacks, and the skull-and-claw front piece above the booth."""
    _field(v, -90, -20, 90, 100)
    v.fill(-90, 0, -95, 90, 0, -21, "gray_concrete")
    r = 42
    v.sphere(0, 1, -40, r, TRUSS, hollow=True, y_min=1)
    _prune(v, lambda x, y, z: z > -40 and y > 0 and v.blocks.get((x, y, z)) == "minecraft:" + TRUSS
           and abs(x) <= r + 1 and abs(z + 40) <= r + 1)
    for y in (10, 20, 30, 38):                                               # geodesic lattice rings
        rr = math.sqrt(max(0.0, r * r - (y - 1) ** 2))
        v.disc(0, y, -40, rr, "white_concrete", hollow=True)
    _prune(v, lambda x, y, z: z > -40 and v.blocks.get((x, y, z)) == "minecraft:white_concrete" and y > 1
           and abs(x) <= r + 1 and abs(z + 40) <= r + 1)
    for a in range(0, 181, 30):
        v.line((round(r * math.cos(math.radians(a))), 1, -40), (0, 1 + r, -40), "white_concrete")
    _led(v, -34, 2, -41, 34, 26, -41, LED_WARM, mode="y", band=2)
    v.fill(-36, 1, -42, 36, 1, -41, "black_concrete")
    for sx in (-1, 1):                                                       # bass stacks
        for i in range(3):
            v.fill(sx * (38 + i * 4) - 1, 1, -44 + i * 3, sx * (38 + i * 4) + 1, 14 - i * 2, -40 + i * 3, "black_concrete")
            v.fill(sx * (38 + i * 4) - 1, 3, -39 + i * 3, sx * (38 + i * 4) + 1, 12 - i * 2, -39 + i * 3, "gray_concrete")
    _deck(v, -30, -40, 30, -22, 4)
    # the skull and the claws
    v.sphere(0, 36, -40, 8, "white_concrete", hollow=False)
    for sx in (-1, 1):
        v.fill(sx * 3 - 1, 36, -33, sx * 3 + 1, 38, -32, "black_concrete")
    v.fill(-3, 29, -34, 3, 32, -32, "white_concrete"); v.fill(-2, 31, -33, 2, 31, -32, "black_concrete")
    for sx in (-1, 1):
        for i, (dy, dz) in enumerate(((0, 0), (4, 2), (-4, 2))):
            p0 = (sx * 8, 34 + dy, -42 + dz)
            p1 = (sx * 26, 30 + dy, -36 + dz)
            p2 = (sx * 30, 14 + dy, -30 + dz)
            v.line(p0, p1, "bone_block"); v.line(p1, p2, "bone_block")
            v.line(p2, (sx * 24, 6 + dy, -30 + dz), "bone_block")
    for x in (-50, -40, 40, 50):
        _pyro(v, x, -18, 8)
    for x, z in ((-70, 40), (70, 40), (-70, 90), (70, 90)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -86, 96, 12); _portaloos(v, 62, 96, 12)


def wasteland(v: Voxel) -> None:
    """wasteLAND in its post-2019 junkyard form: a rusted truss LED wall, scrap towers with flames,
    a crashed semi-truck, barrels, tyres and chain-link around a dirt floor."""
    rng = random.Random(19)
    S.pad(v, -100, -70, 100, 100, "coarse_dirt")
    for _ in range(400):
        v.set(rng.randint(-100, 100), 0, rng.randint(-70, 100), rng.choice(("gravel", "dirt", "brown_terracotta")))
    v.walls(-100, 1, -70, 100, 1, 100, "iron_bars")
    for x in range(-6, 7):
        v.blocks.pop((x, 1, 100), None)
    rust = ("oxidized_copper", "weathered_copper", "exposed_copper", "iron_block", "brown_terracotta", "cut_copper")
    _scaffold_wall(v, -52, -50, 52, 26, step=8)
    for x in range(-52, 53, 8):                                               # rust the truss
        for y in range(1, 27, 3):
            v.fill(x, y, -50, x + 1, y, -49, rng.choice(rust))
    _led(v, -48, 3, -48, 48, 24, -48, LED_WARM, mode="xy", band=4)
    v.fill(-54, 1, -52, 54, 2, -40, "iron_block")
    _deck(v, -36, -40, 36, -18, 3)
    for x in (-82, -66, 66, 82):                                               # scrap towers
        y = 1
        while y < 30:
            w = rng.randint(2, 5); h = rng.randint(2, 5)
            ox, oz = rng.randint(-2, 2), rng.randint(-2, 2)
            v.fill(x + ox - w // 2, y, -58 + oz - w // 2, x + ox + w // 2, y + h - 1, -58 + oz + w // 2, rng.choice(rust))
            y += h
        v.set(x, y, -58, "netherrack"); v.set(x, y + 1, -58, "fire")
        v.fill(x + 3, y - 6, -58, x + 3, y + 2, -58, "chain")
    # the crashed semi
    v.fill(26, 1, 10, 32, 5, 16, "gray_concrete"); v.fill(27, 4, 11, 31, 4, 15, "black_stained_glass")
    for i in range(5):
        v.fill(33 + i * 4, 1 + i, 9, 36 + i * 4, 4 + i, 17, "light_gray_concrete")
    v.fill(26, 1, 9, 27, 2, 9, "black_concrete"); v.fill(31, 1, 9, 32, 2, 9, "black_concrete")
    v.fill(26, 1, 17, 27, 2, 17, "black_concrete"); v.fill(31, 1, 17, 32, 2, 17, "black_concrete")
    v.fill(28, 6, 12, 28, 9, 12, "black_concrete"); v.set(28, 10, 12, "fire")
    for _ in range(40):                                                        # barrels and tyres
        x, z = rng.randint(-95, 95), rng.randint(-30, 95)
        if abs(x) < 50 and z < 0:
            continue
        if rng.random() < .6:
            v.fill(x, 1, z, x, 2, z, rng.choice(("orange_concrete", "black_concrete", "red_concrete", "yellow_concrete")))
            if rng.random() < .3:
                v.set(x, 3, z, "netherrack"); v.set(x, 4, z, "fire")
        else:
            v.disc(x, 1, z, 1.5, "black_concrete", hollow=True)
    for x in (-40, 40):
        _truss(v, x, -8, 30, w=3, block="iron_block"); _spire(v, x + 1, 31, -7, 8)
    for x, z in ((-70, 50), (70, 50)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -90, 96, 10); _portaloos(v, 70, 96, 10)


def quantumvalley(v: Voxel) -> None:
    """quantumVALLEY, the Dreamstate trance stage, in its 2023-2024 form: an LED wall and booth
    under a giant mushroom canopy whose cap is banded like a mandala, with a ring of smaller
    glowing mushrooms along the edges of the field."""
    _field(v, -100, -20, 100, 110)
    v.fill(-100, 0, -70, 100, 0, -21, "gray_concrete")
    _scaffold_wall(v, -46, -56, 46, 26, step=8)
    _led(v, -44, 3, -54, 44, 24, -54, ["sea_lantern", "purple_stained_glass", "magenta_stained_glass",
                                        "glowstone", "cyan_stained_glass"], mode="y", band=2)
    v.fill(-48, 1, -58, 48, 2, -46, "black_concrete")
    _deck(v, -34, -46, 34, -24, 4)
    # the canopy
    v.cylinder(0, 1, -24, 6, 26, TRUSS, hollow=True)
    _led(v, -6, 3, -18, 6, 24, -18, LED, mode="y")
    cap = ("purple_stained_glass", "magenta_stained_glass", "sea_lantern", "cyan_stained_glass",
           "pink_stained_glass", "glowstone")
    layers = 11
    for i in range(layers):
        rr = 48 * math.sqrt(max(0.0, 1 - (i / layers) ** 2))
        v.disc(0, 27 + i, -24, rr, cap[i % len(cap)], hollow=i < layers - 1)
        if i < layers - 1:
            v.disc(0, 27 + i, -24, rr - 1, "black_concrete", hollow=True)
    v.disc(0, 27, -24, 47, "purple_stained_glass")                              # underside
    for a in range(0, 360, 15):                                                 # glowing gills
        v.line((round(8 * math.cos(math.radians(a))), 27, round(-24 + 8 * math.sin(math.radians(a)))),
               (round(46 * math.cos(math.radians(a))), 27, round(-24 + 46 * math.sin(math.radians(a)))), "sea_lantern")
    v.disc(0, 38, -24, 6, "sea_lantern"); _spire(v, 0, 39, -24, 10)
    rng = random.Random(23)
    for i in range(12):                                                         # small mushrooms
        side = -1 if i % 2 else 1
        x, z = side * rng.randint(62, 92), -40 + i * 12
        h = rng.randint(5, 10); rc = rng.randint(3, 5)
        v.column(x, 1, z, h, "white_concrete")
        v.disc(x, h + 1, z, rc, rng.choice(cap)); v.disc(x, h + 2, z, rc - 2, rng.choice(cap))
    for x, z in ((-85, 100), (85, 100)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -96, 106, 12); _portaloos(v, 72, 106, 12)


def bionicjungle(v: Voxel) -> None:
    """bionicJUNGLE, the house stage introduced in 2022: a giant tree whose trunk carries the LED
    wall, with buttress roots, hanging vines, butterflies in the canopy and glowing mushrooms."""
    _field(v, -90, -20, 90, 100, ground="moss_block")
    v.fill(-90, 0, -85, 90, 0, -21, "podzol")
    cx, cz = 0, -50
    v.cylinder(cx, 1, cz, 9, 32, "dark_oak_log")
    v.cylinder(cx, 33, cz, 5, 4, "dark_oak_log")
    for a in range(0, 360, 30):                                                 # buttress roots
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        v.line((round(cx + 8 * ca), 8, round(cz + 8 * sa)), (round(cx + 20 * ca), 1, round(cz + 20 * sa)), "dark_oak_log")
        v.line((round(cx + 9 * ca), 1, round(cz + 9 * sa)), (round(cx + 18 * ca), 1, round(cz + 18 * sa)), "dark_oak_log")
    for (dx, dy, dz, r) in ((0, 40, 0, 16), (-18, 36, -4, 11), (18, 36, -4, 11), (0, 36, 14, 11), (0, 36, -18, 11),
                            (-10, 44, 10, 8), (10, 44, 10, 8)):
        v.line((cx, 30, cz), (cx + dx, dy, cz + dz), "dark_oak_log")
        v.sphere(cx + dx, dy, cz + dz, r, LEAVES, hollow=True)
    rng = random.Random(31)
    for _ in range(24):                                                         # vines
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(12, 26)
        x, z = round(cx + rr * math.cos(a)), round(cz + rr * math.sin(a))
        v.fill(x, rng.randint(14, 24), z, x, 28, z, LEAVES)
    for _ in range(26):                                                         # butterflies
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(8, 20)
        x, z = round(cx + rr * math.cos(a)), round(cz + rr * math.sin(a)); y = rng.randint(50, 58)
        wing = rng.choice(("magenta_stained_glass", "cyan_stained_glass", "orange_stained_glass", "yellow_stained_glass"))
        v.set(x, y, z, "end_rod"); v.fill(x - 2, y, z, x - 1, y + 1, z, wing); v.fill(x + 1, y, z, x + 2, y + 1, z, wing)
    for _ in range(14):                                                         # mushrooms
        x, z = rng.randint(-80, 80), rng.randint(-80, 95)
        if abs(x) < 20 and z < -20:
            continue
        h = rng.randint(2, 5)
        v.column(x, 1, z, h, "mushroom_stem")
        v.sphere(x, h + 1, z, 2, rng.choice(("red_mushroom_block", "brown_mushroom_block")), hollow=False)
        v.set(x, h + 1, z, "glowstone")
    # the LED wall in the trunk and the booth
    v.fill(-14, 1, -44, 14, 22, -41, "dark_oak_log")
    _led(v, -12, 3, -40, 12, 20, -40, ["sea_lantern", "lime_stained_glass", "green_stained_glass", "glowstone",
                                        "cyan_stained_glass"], mode="y")
    _deck(v, -22, -40, 22, -24, 3)
    for x, z in ((-70, 60), (70, 60)):
        _light_tower(v, x, z, 14)
    _portaloos(v, -86, 96, 10); _portaloos(v, 66, 96, 10)


def stereobloom(v: Voxel) -> None:
    """stereoBLOOM in its 2021-2024 flower form: one giant bloom with a circular LED heart and eight
    radiating petals on a green stem over the booth, smaller blooms along the sides."""
    _field(v, -90, -20, 90, 100)
    v.fill(-90, 0, -70, 90, 0, -21, "gray_concrete")
    _scaffold_wall(v, -36, -50, 36, 20, step=8)
    _led(v, -34, 3, -48, 34, 18, -48, ["sea_lantern", "pink_stained_glass", "magenta_stained_glass",
                                        "glowstone", "orange_stained_glass"], mode="y")
    v.fill(-38, 1, -52, 38, 2, -40, "black_concrete")
    _deck(v, -26, -40, 26, -22, 3)

    def bloom(x: int, z: int, h: int, r: int, petal_r: int, petals=("pink_concrete", "magenta_concrete")) -> None:
        v.fill(x - 1, 1, z - 1, x + 1, h, z + 1, "lime_concrete")
        for ly in range(h // 3, h, h // 3):
            v.disc(x + 3, ly, z, 3, "lime_concrete", rz=1.5); v.disc(x - 3, ly + 2, z, 3, "lime_concrete", rz=1.5)
        for i, a in enumerate(range(0, 360, 45)):
            px = round(x + (r + petal_r - 1) * math.cos(math.radians(a)))
            py = round(h + r + (r + petal_r - 1) * math.sin(math.radians(a)))
            _vdisc(v, px, py, z - 1, petal_r, petals[i % len(petals)], depth=2)
        _vdisc(v, x, h + r, z, r, "black_concrete", depth=2)
        _vring(v, x, h + r, z + 2, r, "sea_lantern")
        _vdisc(v, x, h + r, z + 2, r * 0.75, "yellow_stained_glass", depth=1)
        _vdisc(v, x, h + r, z + 2, r * 0.35, "glowstone", depth=1)

    bloom(0, -55, 24, 11, 7)
    rng = random.Random(41)
    for i in range(8):
        side = -1 if i % 2 else 1
        bloom(side * rng.randint(55, 80), -45 + i * 14, rng.randint(6, 12), 3, 2,
              petals=(rng.choice(("white_concrete", "orange_concrete", "pink_concrete", "purple_concrete")),))
    for x, z in ((-70, 70), (70, 70)):
        _light_tower(v, x, z, 14)
    _portaloos(v, -86, 96, 10); _portaloos(v, 66, 96, 10)


def _mini_stage(v: Voxel, x: int, z: int, w: int, h: int, colors) -> None:
    """A stage marker on the grounds map: small truss frame, LED front, deck, facing south."""
    v.fill(x - w // 2 - 1, 1, z - 3, x + w // 2 + 1, h + 1, z - 2, TRUSS)
    _led(v, x - w // 2, 2, z - 1, x + w // 2, h, z - 1, colors, mode="y")
    v.fill(x - w // 2, 1, z, x + w // 2, 1, z + 4, "black_concrete")
    _spire(v, x - w // 2 - 1, h + 2, z - 3, 4); _spire(v, x + w // 2 + 1, h + 2, z - 3, 4)


def edc_grounds(v: Voxel) -> None:
    """The Las Vegas Motor Speedway grounds in miniature (2024 layout): the tri-oval, nine stages on the
    infield, the main entrance with the EDC sign, the Ferris wheel and carnival rides, and the
    Parliament, Boombox and Kalliope art cars parked on the infield roads."""
    S.pad(v, -150, -150, 150, 150, "grass_block")
    v.disc(0, 0, 0, 148, "gray_concrete", rz=138)
    v.disc(0, 0, 0, 138, "grass_block", rz=128)
    v.disc(0, 0, 0, 142, "white_concrete", rz=132, hollow=True)
    v.disc(0, 0, 0, 144, "light_gray_concrete", rz=134, hollow=True)
    for x in range(-120, 121, 2):                                              # the grandstand on the north straight
        v.fill(x, 1, -149, x, 1, -140, "gray_concrete")
    for t in range(5):
        v.fill(-120, 1 + t, -149 + t, 120, 1 + t, -149 + t, "light_gray_concrete")
    v.fill(-120, 7, -150, 120, 7, -142, "white_concrete")
    for x in range(-120, 121, 30):
        v.fill(x, 6, -150, x, 6, -150, "white_concrete")
    # the nine stages, roughly where they stood in 2024
    _mini_stage(v, 0, -95, 40, 14, LED)                                        # kineticFIELD
    _mini_stage(v, -95, -40, 28, 11, LED_COOL)                                 # circuitGROUNDS
    _mini_stage(v, 95, -40, 28, 10, ["sea_lantern", "lime_stained_glass", "yellow_stained_glass"])   # cosmicMEADOW
    _mini_stage(v, -60, 30, 18, 8, ["sea_lantern", "orange_stained_glass", "red_stained_glass"])    # wasteLAND
    _mini_stage(v, 60, 30, 18, 8, LED_WARM)                                    # bassPOD
    _mini_stage(v, -105, 70, 16, 8, ["sea_lantern", "purple_stained_glass", "magenta_stained_glass"])  # quantumVALLEY
    _mini_stage(v, 105, 70, 16, 8, ["sea_lantern", "cyan_stained_glass", "blue_stained_glass"])   # neonGARDEN
    _mini_stage(v, -30, 95, 14, 7, ["sea_lantern", "lime_stained_glass", "green_stained_glass"])   # bionicJUNGLE
    _mini_stage(v, 30, 95, 14, 7, ["sea_lantern", "pink_stained_glass", "magenta_stained_glass"])  # stereoBLOOM
    v.fill(-6, 0, -90, 6, 0, 125, "gray_concrete"); v.fill(-120, 0, 20, 120, 0, 24, "gray_concrete")   # infield roads
    # main entrance on the south straight with the EDC sign over the gate
    for x in (-24, 20):
        v.fill(x, 1, 136, x + 3, 22, 139, "white_concrete")
    v.fill(-25, 23, 135, 24, 24, 140, "black_concrete")
    _text(v, "EDC", -17, 26, 140, "glowstone", scale=2)
    _owl(v, 0, 50, 139, 9)
    for x in range(-60, 61, 6):                                                # the entry lanes
        v.fill(x, 1, 142, x, 1, 149, "iron_bars")
    # Ferris wheel and carnival rides on the east and west infield
    _ferris(v, 100, 110, 22)
    v.fill(-102, 1, 102, -97, 60, 107, "white_concrete")                      # drop tower
    v.fill(-105, 40, 99, -94, 42, 110, "red_concrete", hollow=True)
    v.set(-99, 61, 104, "glowstone")
    v.fill(-71, 1, 120, -69, 34, 122, "white_concrete")                        # swing ride
    v.disc(-70, 35, 121, 12, "yellow_concrete", hollow=True); v.disc(-70, 35, 121, 11, "red_concrete", hollow=True)
    for a in range(0, 360, 30):
        x, z = round(-70 + 11 * math.cos(math.radians(a))), round(121 + 11 * math.sin(math.radians(a)))
        v.fill(x, 28, z, x, 34, z, "chain"); v.set(x, 27, z, "blue_concrete")
    v.disc(70, 1, 125, 9, "oak_planks"); v.column(70, 1, 125, 9, "white_concrete")     # carousel
    v.cone(70, 9, 125, 11, 6, "red_concrete")
    for a in range(0, 360, 45):
        x, z = round(70 + 6 * math.cos(math.radians(a))), round(125 + 6 * math.sin(math.radians(a)))
        v.fill(x, 2, z, x, 8, z, "gold_block")
    # the art cars
    v.fill(-50, 1, 56, -35, 5, 61, "brown_terracotta")                         # Parliament: twisted-forest bus
    v.fill(-49, 3, 55, -36, 4, 55, "black_stained_glass")
    for i, x in enumerate(range(-48, -36, 3)):
        v.line((x, 6, 58), (x + (2 if i % 2 else -2), 12 + i, 58 + (1 if i % 2 else -1)), "dark_oak_log")
        v.set(x + (2 if i % 2 else -2), 13 + i, 58 + (1 if i % 2 else -1), "lantern")
    v.fill(-50, 0, 55, -35, 0, 62, "gray_concrete")
    v.fill(35, 1, 56, 50, 6, 61, "black_concrete")                             # Boombox
    _vdisc(v, 39, 4, 55, 2.5, "gray_concrete"); _vdisc(v, 46, 4, 55, 2.5, "gray_concrete")
    v.fill(41, 3, 55, 44, 5, 55, "sea_lantern"); v.fill(36, 7, 57, 49, 7, 60, "gray_concrete")
    v.fill(38, 8, 58, 47, 8, 59, "black_concrete")
    v.fill(-8, 1, 70, 8, 6, 80, "purple_concrete")                             # Kalliope: burlesque speakeasy on wheels
    v.fill(-7, 7, 71, 7, 10, 79, "red_concrete"); v.fill(-6, 11, 72, 6, 11, 78, "gold_block")
    v.cylinder(0, 12, 75, 3, 5, "gold_block", hollow=True); v.set(0, 17, 75, "glowstone")
    v.fill(-9, 2, 68, 9, 4, 69, "sea_lantern")
    for x in (-8, 8):
        v.fill(x, 0, 70, x, 0, 80, "black_concrete")
    for x, z in ((-130, 0), (130, 0), (0, -120), (-60, -120), (60, -120)):
        _light_tower(v, x, z, 20)
    _portaloos(v, -120, 128, 24); _portaloos(v, 60, 128, 20)


# --------------------------------------------------------- other venues

def nos_events_center(v: Voxel) -> None:
    """NOS Events Center, San Bernardino, dressed for Beyond Wonderland SoCal 2025: the Queen's Domain
    megastructure, Mad Hatter's Castle on the dirt speedway as a deck-of-cards castle, Damon Hall with
    its barrel-vault roof, and the grandstand along the oval."""
    S.pad(v, -110, -110, 110, 110, "grass_block")
    v.fill(-110, 0, -110, 110, 0, -104, "gray_concrete"); v.fill(-110, 0, -110, -104, 0, 110, "gray_concrete")
    # the Queen's Domain megastructure (largest in the world, per Insomniac)
    x1, x2, z1, z2 = -100, -14, -98, -26
    v.fill(x1, 0, z1, x2, 0, z2, "gray_concrete")
    for x in range(x1, x2 + 1, 12):
        _truss(v, x, z1, 26); _truss(v, x, z2 - 1, 26)
    for z in range(z1, z2 + 1, 12):
        _truss(v, x1, z, 26); _truss(v, x2 - 1, z, 26)
    v.fill(x1 - 1, 27, z1 - 1, x2 + 2, 27, z2 + 2, TRUSS, hollow=True)
    for z in range(z1 - 1, z2 + 3):
        y = 28 + int(10 * math.sin(math.pi * (z - z1 + 1) / (z2 - z1 + 3)))
        v.fill(x1 - 1, y, z, x2 + 2, y, z, "white_concrete")
        v.fill(x1 - 1, 28, z, x1 - 1, y, z, "white_concrete"); v.fill(x2 + 2, 28, z, x2 + 2, y, z, "white_concrete")
    _led(v, x1 + 2, 2, z1 + 1, x2 - 2, 24, z1 + 1, ["sea_lantern", "purple_stained_glass", "blue_stained_glass",
                                                  "glowstone", "magenta_stained_glass"], mode="xy", band=3)
    _led(v, x1, 20, z1 + 2, x1, 25, z2 - 2, LED, mode="y"); _led(v, x2, 20, z1 + 2, x2, 25, z2 - 2, LED, mode="y")
    _deck(v, x1 + 8, z1 + 2, x2 - 8, z1 + 18, 3)
    _vdisc(v, (x1 + x2) // 2, 40, z1 - 2, 8, "red_concrete", depth=2)                   # the Queen's heart crest
    _vdisc(v, (x1 + x2) // 2 - 4, 44, z1 - 2, 5, "red_concrete", depth=2); _vdisc(v, (x1 + x2) // 2 + 4, 44, z1 - 2, 5, "red_concrete", depth=2)
    # the dirt speedway oval, the grandstand and Mad Hatter's Castle at its north end
    ox, oz = 50, 20
    v.disc(ox, 0, oz, 56, "brown_terracotta", rz=76); v.disc(ox, 0, oz, 44, "coarse_dirt", rz=64)
    v.disc(ox, 0, oz, 36, "grass_block", rz=56)
    for t in range(6):                                                                   # grandstand, west side
        v.fill(-12 + t, 1 + t, -40, -11 + t, 1 + t, 80, "light_gray_concrete")
    v.fill(-14, 7, -40, -6, 7, 80, "white_concrete")
    cx, cz = ox, oz - 60
    v.fill(cx - 24, 1, cz - 6, cx + 24, 14, cz - 2, "white_concrete")
    v.fill(cx - 24, 1, cz - 6, cx + 24, 1, cz - 2, "black_concrete")
    v.crenellate(cx - 24, 15, cz - 6, cx + 24, cz - 2, "white_concrete", period=2)
    for sx in (-1, 1):
        v.cylinder(cx + sx * 26, 1, cz - 4, 4, 24, "white_concrete", hollow=True)
        v.cone(cx + sx * 26, 25, cz - 4, 5, 7, "red_concrete" if sx < 0 else "black_concrete")
        for y in (4, 10, 16):
            v.fill(cx + sx * 26 - 1, y, cz - 1, cx + sx * 26 + 1, y + 1, cz - 1, "red_concrete" if sx < 0 else "black_concrete")
    v.fill(cx - 10, 2, cz - 6, cx + 10, 12, cz - 2, "air")
    _led(v, cx - 10, 2, cz - 3, cx + 10, 12, cz - 3, LED_WARM, mode="y")
    for i, (dx, suit) in enumerate(((-20, "red_concrete"), (-14, "black_concrete"), (14, "red_concrete"), (20, "black_concrete"))):
        v.fill(cx + dx - 2, 3, cz - 1, cx + dx + 2, 12, cz - 1, "white_concrete")                  # the playing cards
        v.fill(cx + dx - 1, 5, cz, cx + dx + 1, 7, cz, suit); v.set(cx + dx, 8, cz, suit); v.set(cx + dx, 4, cz, suit)
    _deck(v, cx - 12, cz - 1, cx + 12, cz + 10, 2)
    # Damon Hall: the barrel-vaulted exhibition building by the south lawn
    hx1, hx2, hz1, hz2 = -100, -36, 30, 70
    v.fill(hx1, 1, hz1, hx2, 10, hz2, "white_concrete", hollow=True)
    v.fill(hx1, 1, hz1, hx2, 1, hz2, "polished_andesite")
    for z in range(hz1, hz2 + 1):
        y = 10 + int(9 * math.sin(math.pi * (z - hz1) / (hz2 - hz1)))
        v.fill(hx1 - 1, y, z, hx2 + 1, y, z, "light_gray_concrete")
    for x in range(hx1 + 4, hx2, 8):
        v.fill(x, 3, hz2, x + 1, 6, hz2, "glass_pane")
    v.fill(-70, 1, hz2, -66, 5, hz2, "air"); v.fill(-70, 1, hz1, -66, 5, hz1, "air")
    v.fill(-72, 6, hz2 + 1, -64, 6, hz2 + 3, "red_concrete")
    _text(v, "NOS", -88, 12, hz2 + 1, "red_concrete", scale=1)
    v.fill(-100, 0, 72, -36, 0, 100, "gray_concrete")                                     # parking
    for x in range(-98, -36, 6):
        v.fill(x, 0, 74, x, 0, 98, "white_concrete")
    for x, z in ((20, 100), (90, 100), (-30, -100)):
        _light_tower(v, x, z, 16)
    _portaloos(v, -30, 104, 14); _portaloos(v, 40, 104, 14)


def escape_psycho_circus(v: Voxel) -> None:
    """Escape: Psycho Circus 2018 at NOS: the Slaughterhouse main stage inside a giant clown's mouth
    under a striped big top with circus cages at its sides, and Ghouls' Graveyard, the haunted-house
    stage with its graveyard of headstones and dead trees."""
    rng = random.Random(13)
    S.pad(v, -110, -80, 110, 110, "podzol")
    for _ in range(600):
        v.set(rng.randint(-110, 110), 0, rng.randint(-80, 110), rng.choice(("coarse_dirt", "dirt", "podzol", "gravel")))
    v.walls(-110, 1, -80, 110, 1, 110, "iron_bars")
    for x in range(-6, 7):
        v.blocks.pop((x, 1, 110), None)
    # ---- Slaughterhouse (west)
    cx = -58
    v.fill(cx - 42, 1, -62, cx + 42, 34, -58, "black_concrete")
    _vdisc(v, cx, 20, -57, 20, "white_concrete", depth=2)                                      # the clown face
    for sx in (-1, 1):
        _vdisc(v, cx + sx * 8, 27, -55, 4, "glowstone", depth=1); _vdisc(v, cx + sx * 8, 27, -54, 1.5, "black_concrete", depth=1)
        _vring(v, cx + sx * 8, 27, -55, 5, "blue_concrete", 0, 180)
        v.sphere(cx + sx * 21, 30, -58, 5, "orange_concrete", hollow=False)                   # hair
    _vdisc(v, cx, 19, -55, 3, "red_concrete", depth=1)
    v.fill(cx - 13, 2, -62, cx + 13, 13, -55, "air")                                           # the mouth
    _vring(v, cx, 13, -55, 12, "red_concrete", 180, 360)
    v.fill(cx - 14, 13, -55, cx + 14, 14, -55, "red_concrete")
    for x in range(cx - 12, cx + 13, 4):                                                       # teeth
        v.fill(x, 11, -55, x + 1, 12, -55, "white_concrete")
    _led(v, cx - 12, 2, -61, cx + 12, 10, -61, LED_WARM, mode="y")
    _deck(v, cx - 12, -60, cx + 12, -50, 1)
    v.fill(cx - 46, 35, -66, cx + 46, 35, -40, "red_concrete")
    for k in range(16):                                                                          # striped big top
        rr = 46 * (1 - k / 16)
        for x in range(cx - int(rr) - 1, cx + int(rr) + 2):
            for z in range(-53 - int(rr) - 1, -53 + int(rr) + 2):
                if (x - cx) ** 2 + (z + 53) ** 2 <= (rr + 0.5) ** 2:
                    band = int((math.degrees(math.atan2(z + 53, x - cx)) + 360) // 22.5)
                    v.set(x, 36 + k, z, "red_concrete" if band % 2 else "white_concrete")
    v.fill(cx, 52, -53, cx, 58, -53, "yellow_concrete"); v.set(cx, 59, -53, "red_concrete")
    for sx in (-1, 1):                                                                           # circus cages
        x = cx + sx * 50
        v.fill(x - 4, 1, -60, x + 4, 8, -50, "iron_bars", hollow=True)
        v.fill(x - 4, 1, -60, x + 4, 1, -50, "black_concrete"); v.fill(x - 4, 9, -60, x + 4, 9, -50, "red_concrete")
        v.set(x, 4, -55, "lantern")
    # ---- Ghouls' Graveyard (east)
    gx = 60
    v.fill(gx - 36, 1, -62, gx + 36, 24, -40, "dark_oak_planks", hollow=True)
    v.fill(gx - 36, 1, -62, gx + 36, 1, -40, "spruce_planks")
    v.gable_roof(gx - 36, 25, -62, gx + 36, -40, "deepslate_tiles", ridge_axis="x", overhang=2)
    v.fill(gx + 20, 1, -66, gx + 32, 36, -54, "dark_oak_planks", hollow=True)                   # the tower
    v.cone(gx + 26, 37, -60, 8, 12, "deepslate_tiles")
    for y in (4, 10, 16, 22, 28, 34):
        for x in (gx + 22, gx + 30):
            v.fill(x, y, -54, x + 1, y + 2, -54, rng.choice(("purple_stained_glass", "black_stained_glass", "orange_stained_glass")))
    for x in range(gx - 32, gx + 16, 8):
        for y in (4, 12, 19):
            v.fill(x, y, -40, x + 2, y + 3, -40, rng.choice(("purple_stained_glass", "black_stained_glass", "orange_stained_glass", "air")))
    v.fill(gx - 13, 2, -40, gx + 13, 18, -40, "air")
    _led(v, gx - 12, 3, -41, gx + 12, 17, -41, ["sea_lantern", "purple_stained_glass", "orange_stained_glass", "glowstone",
                                                  "lime_stained_glass"], mode="y")
    v.fill(gx - 14, 2, -40, gx + 14, 2, -40, "dark_oak_log"); v.fill(gx - 14, 2, -40, gx - 14, 18, -40, "dark_oak_log")
    v.fill(gx + 14, 2, -40, gx + 14, 18, -40, "dark_oak_log"); v.fill(gx - 14, 18, -40, gx + 14, 18, -40, "dark_oak_log")
    _deck(v, gx - 12, -39, gx + 12, -30, 1)
    for _ in range(50):                                                                          # headstones
        x, z = gx + rng.randint(-40, 40), rng.randint(-24, 60)
        if abs(x - gx) < 16 and z < -10:
            continue
        v.fill(x, 1, z, x, 2, z, rng.choice(("cobblestone", "stone", "mossy_cobblestone")))
        v.set(x, 3, z, "stone_brick_slab")
    for _ in range(10):                                                                          # dead trees
        x, z = gx + rng.randint(-44, 44), rng.randint(-30, 70)
        h = rng.randint(6, 11)
        v.column(x, 1, z, h, "dark_oak_log")
        for a in range(0, 360, 90):
            v.line((x, h - 2, z), (x + round(4 * math.cos(math.radians(a + rng.randint(0, 60)))), h + 3,
                                   z + round(4 * math.sin(math.radians(a + rng.randint(0, 60))))), "dark_oak_log")
    for x in range(gx - 40, gx + 41, 4):
        v.set(x, 1, 70, "iron_bars"); v.set(x, 2, 70, "iron_bars")
    for x in range(gx - 40, gx + 41, 10):
        v.set(x, 1, -26, "jack_o_lantern[facing=south]")
    for x, z in ((-100, 60), (-20, 60), (20, 80), (100, 80)):
        _light_tower(v, x, z, 14)
    _portaloos(v, -100, 104, 12); _portaloos(v, 70, 104, 12)


def nocturnal_wonderland(v: Voxel) -> None:
    """Nocturnal Wonderland at Glen Helen Amphitheater, 2018-2019 layout: the main stage with its giant
    smiling sun face and radiating LED rays at the foot of the natural amphitheater slope, and the
    Labyrinth up the hill, angled to face the slope, ringed by the 2016 blacklight pillars and hedges."""
    _field(v, -110, -30, 110, 110)
    v.fill(-110, 0, -90, 110, 0, -31, "gray_concrete")
    for k in range(1, 11):                                                                     # the hill rises to the south
        v.fill(-110, k, 30 + k * 8, 110, k, 110, "grass_block")
    for k in range(1, 11):
        v.fill(-109, k + 1, 30 + k * 8, 109, k + 1, 30 + k * 8, "oak_fence")
    for x in range(-6, 7):
        for k in range(1, 11):
            v.blocks.pop((x, k + 1, 30 + k * 8), None)
    v.fill(-110, 11, 110, 110, 11, 110, "oak_fence")
    # the main stage and its sun
    _scaffold_wall(v, -52, -58, 52, 24, step=8)
    _led(v, -50, 3, -56, 50, 22, -56, ["sea_lantern", "yellow_stained_glass", "orange_stained_glass", "glowstone",
                                        "red_stained_glass"], mode="y", band=2)
    v.fill(-54, 1, -60, 54, 2, -46, "black_concrete")
    _sun(v, 0, 42, -58, 16)
    for sx in (-1, 1):
        for i, (dx, dy) in enumerate(((22, 30), (30, 24), (36, 16), (40, 8))):                  # LED rays either side
            _led(v, sx * dx - 3, dy, -57, sx * dx + 3, dy + 10, -57, LED_WARM, mode="y")
            v.fill(sx * dx - 3, dy + 11, -58, sx * dx + 3, dy + 11, -58, TRUSS)
            v.line((sx * dx, dy + 11, -58), (sx * 50, 25, -58), TRUSS)
    _deck(v, -36, -46, 36, -26, 4)
    for x in (-62, 62):
        _truss(v, x, -60, 44, w=3); _spire(v, x + 1, 45, -59, 8)
    for x in (-44, -22, 22, 44):
        _pyro(v, x, -22, 8)
    # the Labyrinth up the hill, facing the slope
    lx, lz, ly = 70, 60, 5
    v.fill(lx - 25, ly, lz - 25, lx + 25, ly, lz + 25, "grass_block")
    v.fill(lx - 25, ly + 1, lz - 25, lx + 25, ly + 8, lz + 25, "air")
    v.fill(lx - 18, ly + 1, lz - 24, lx + 18, ly + 2, lz - 18, "black_concrete")
    _led(v, lx - 16, ly + 3, lz - 23, lx + 16, ly + 12, lz - 23, ["sea_lantern", "lime_stained_glass", "magenta_stained_glass",
                                                               "cyan_stained_glass", "glowstone"], mode="x", band=4)
    v.fill(lx - 18, ly + 13, lz - 24, lx + 18, ly + 13, lz - 22, TRUSS)
    rng = random.Random(53)
    uv = ("lime_concrete", "magenta_concrete", "cyan_concrete", "glowstone", "purple_concrete")
    for x in range(lx - 24, lx + 25, 6):                                                        # blacklight pillars
        for z in range(lz - 14, lz + 25, 6):
            h = rng.randint(5, 9)
            for y in range(h):
                v.set(x, ly + 1 + y, z, uv[(y + x // 6) % len(uv)])
            v.set(x, ly + 1 + h, z, "end_rod")
    hedge = "dark_oak_leaves[persistent=true]"
    for z in range(lz - 10, lz + 25, 6):                                                        # hedge maze walls
        for x in range(lx - 24, lx + 25, 6):
            if rng.random() < .55:
                v.fill(x + 1, ly + 1, z, x + 5, ly + 3, z, hedge)
            else:
                v.fill(x, ly + 1, z + 1, x, ly + 3, z + 5, hedge)
    v.walls(lx - 25, ly + 1, lz - 25, lx + 25, ly + 3, lz + 25, hedge)
    v.fill(lx - 25, ly + 1, lz - 25, lx - 25, ly + 3, lz - 17, "air")
    for x, z in ((-90, 20), (90, 20), (-40, 70), (0, 70)):
        _light_tower(v, x, z, 14)
    for x in range(-100, -60, 10):                                                              # the hillside pavilion tents
        v.fill(x, 8, 96, x + 6, 8, 102, "white_concrete"); v.column(x + 3, 9, 99, 4, "white_concrete")
        v.cone(x + 3, 12, 99, 5, 4, "white_concrete")
    _portaloos(v, -106, 104, 12); _portaloos(v, 82, 104, 12)


WORLD = World(
    id="insomniac",
    name="Insomniac Events",
    game="EDC Las Vegas, Beyond Wonderland, Escape Halloween, Nocturnal Wonderland, Countdown NYE",
    era="1993-2026",
    description="Pasquale Rotella's festival stages, from the EDC Las Vegas speedway to the NOS Events Center.",
    franchise="Insomniac Events",
).build(Build("edc_kineticfield", "kineticFIELD", "The 2024 kineticCIRCLE main stage: a cathedral facade with the owl in a circular LED rose window, organ-pipe spires, twin pylons, pyro towers, and the Ferris wheel and EDC sign behind.", kineticfield, "1 block = 1 m")
).build(Build("edc_cosmicmeadow", "cosmicMEADOW", "The 2023-2024 wide LED wall under a truss canopy, with giant daisies and sunflowers along the meadow.", cosmicmeadow, "1 block = 1 m")
).build(Build("edc_circuitgrounds", "circuitGROUNDS", "The 2016-2024 panoramic design: five LED-hung truss arches spanning the crowd like a spaceship frame.", circuitgrounds, "1 block = 1 m")
).build(Build("edc_neongarden", "neonGARDEN", "The 2024 megastructure: enclosed truss hall, LED side bands, the hanging light cube and CO2 smoke towers.", neongarden, "1 block = 1 m")
).build(Build("edc_basspod", "bassPOD", "The 2022-2025 geodesic half-dome with its heavy LED front, bass stacks, and the skull and claws over the booth.", basspod, "1 block = 1 m")
).build(Build("edc_wasteland", "wasteLAND", "The post-2019 junkyard: rusted truss LED wall, scrap towers with flames, a crashed semi, barrels and tyres.", wasteland, "1 block = 1 m")
).build(Build("edc_quantumvalley", "quantumVALLEY", "The 2023-2024 Dreamstate trance stage under a giant banded mushroom canopy with glowing gills.", quantumvalley, "1 block = 1 m")
).build(Build("edc_bionicjungle", "bionicJUNGLE", "The 2022 house stage: a giant tree with the LED wall in its trunk, buttress roots, vines, butterflies and mushrooms.", bionicjungle, "1 block = 1 m")
).build(Build("edc_stereobloom", "stereoBLOOM", "The 2021-2024 flower stage: one giant bloom with a circular LED heart and eight petals, smaller blooms alongside.", stereobloom, "1 block = 1 m")
).build(Build("edc_grounds", "EDC Las Vegas grounds", "The Las Vegas Motor Speedway in miniature, 2024 layout: tri-oval, nine stages, entrance with the EDC sign, Ferris wheel, rides, and the Parliament, Boombox and Kalliope art cars.", edc_grounds, "1 block = 5 m")
).build(Build("nos_events_center", "NOS Events Center", "San Bernardino dressed for Beyond Wonderland SoCal 2025: the Queen's Domain megastructure, Mad Hatter's deck-of-cards castle on the dirt speedway, Damon Hall and the grandstand.", nos_events_center, "1 block = 2 m")
).build(Build("escape_psycho_circus", "Escape: Psycho Circus", "Escape 2018 at NOS: the Slaughterhouse stage in a giant clown's mouth under a striped big top with circus cages, and Ghouls' Graveyard's haunted house with headstones and dead trees.", escape_psycho_circus, "1 block = 1 m")
).build(Build("nocturnal_wonderland", "Nocturnal Wonderland", "Glen Helen Amphitheater, 2018-2019: the sun-face main stage at the foot of the slope and the Labyrinth up the hill with its blacklight pillars and hedge maze.", nocturnal_wonderland, "1 block = 1 m"))
