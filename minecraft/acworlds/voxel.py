"""A tiny voxel canvas plus geometric primitives.

Coordinates follow Minecraft: x east, y up, z south.  A build is authored
with its ground level at y = 0 (the slab the player stands on) and is
later exported relative to the player's position with ``~`` coordinates.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, Optional, Tuple

Coord = Tuple[int, int, int]

AIR = "minecraft:air"


def _norm(block: str) -> str:
    """Make sure a block id carries the minecraft namespace."""
    if ":" in block.split("[", 1)[0]:
        return block
    return "minecraft:" + block


class Voxel:
    """Sparse block grid: ``{(x, y, z): block_id}``."""

    def __init__(self) -> None:
        self.blocks: Dict[Coord, str] = {}

    # ------------------------------------------------------------------ core
    def set(self, x: int, y: int, z: int, block: str) -> None:
        self.blocks[(int(x), int(y), int(z))] = _norm(block)

    def get(self, x: int, y: int, z: int) -> Optional[str]:
        return self.blocks.get((x, y, z))

    def clear(self, x: int, y: int, z: int) -> None:
        """Carve: explicitly place air (exported after solids)."""
        self.blocks[(int(x), int(y), int(z))] = AIR

    def merge(self, other: "Voxel", dx: int = 0, dy: int = 0, dz: int = 0) -> None:
        for (x, y, z), b in other.blocks.items():
            self.blocks[(x + dx, y + dy, z + dz)] = b

    def translated(self, dx: int, dy: int, dz: int) -> "Voxel":
        v = Voxel()
        v.merge(self, dx, dy, dz)
        return v

    def bounds(self) -> Tuple[int, int, int, int, int, int]:
        if not self.blocks:
            return (0, 0, 0, 0, 0, 0)
        xs = [c[0] for c in self.blocks]
        ys = [c[1] for c in self.blocks]
        zs = [c[2] for c in self.blocks]
        return (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))

    def size(self) -> Tuple[int, int, int]:
        x1, y1, z1, x2, y2, z2 = self.bounds()
        return (x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1)

    def __len__(self) -> int:
        return len(self.blocks)

    # ------------------------------------------------------------ primitives
    def fill(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
             block: str, hollow: bool = False) -> None:
        """Axis-aligned box (inclusive).  ``hollow`` keeps only the shell."""
        xa, xb = sorted((int(x1), int(x2)))
        ya, yb = sorted((int(y1), int(y2)))
        za, zb = sorted((int(z1), int(z2)))
        block = _norm(block)
        for x in range(xa, xb + 1):
            for y in range(ya, yb + 1):
                for z in range(za, zb + 1):
                    if hollow and not (x in (xa, xb) or y in (ya, yb) or z in (za, zb)):
                        continue
                    self.blocks[(x, y, z)] = block

    def walls(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
              block: str) -> None:
        """Four vertical walls only (no floor / ceiling)."""
        xa, xb = sorted((x1, x2))
        za, zb = sorted((z1, z2))
        self.fill(xa, y1, za, xb, y2, za, block)
        self.fill(xa, y1, zb, xb, y2, zb, block)
        self.fill(xa, y1, za, xa, y2, zb, block)
        self.fill(xb, y1, za, xb, y2, zb, block)

    def carve(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
        self.fill(x1, y1, z1, x2, y2, z2, AIR)

    def column(self, x: int, y1: int, z: int, height: int, block: str) -> None:
        self.fill(x, y1, z, x, y1 + height - 1, z, block)

    def line(self, p1: Coord, p2: Coord, block: str) -> None:
        """3D Bresenham-ish line using interpolation."""
        (x1, y1, z1), (x2, y2, z2) = p1, p2
        n = max(abs(x2 - x1), abs(y2 - y1), abs(z2 - z1), 1)
        for i in range(n + 1):
            t = i / n
            self.set(round(x1 + (x2 - x1) * t), round(y1 + (y2 - y1) * t),
                     round(z1 + (z2 - z1) * t), block)

    def disc(self, cx: int, y: int, cz: int, r: float, block: str,
             hollow: bool = False, rz: Optional[float] = None) -> None:
        """Horizontal filled circle / ellipse (``rz`` for the z radius)."""
        rz = r if rz is None else rz
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for z in range(int(cz - rz - 1), int(cz + rz + 2)):
                d = ((x - cx) / (r + 0.5)) ** 2 + ((z - cz) / (rz + 0.5)) ** 2
                if d <= 1.0:
                    if hollow:
                        d_in = ((x - cx) / (r - 0.5)) ** 2 + ((z - cz) / (rz - 0.5)) ** 2 if r > 0.5 else 2
                        if d_in <= 1.0:
                            continue
                    self.set(x, y, z, block)

    def cylinder(self, cx: int, y1: int, cz: int, r: float, height: int,
                 block: str, hollow: bool = False, rz: Optional[float] = None) -> None:
        for y in range(y1, y1 + height):
            self.disc(cx, y, cz, r, block, hollow=hollow, rz=rz)

    def cone(self, cx: int, y1: int, cz: int, r: float, height: int, block: str) -> None:
        for i in range(height):
            rr = r * (1 - i / height)
            self.disc(cx, y1 + i, cz, rr, block)

    def sphere(self, cx: int, cy: int, cz: int, r: float, block: str,
               hollow: bool = True, y_min: Optional[int] = None,
               y_max: Optional[int] = None) -> None:
        """Sphere shell (or solid).  Clip with y_min / y_max to make domes."""
        lo = int(cy - r - 1) if y_min is None else max(y_min, int(cy - r - 1))
        hi = int(cy + r + 1) if y_max is None else min(y_max, int(cy + r + 1))
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for y in range(lo, hi + 1):
                for z in range(int(cz - r - 1), int(cz + r + 2)):
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
                    if d <= r + 0.5 and (not hollow or d >= r - 0.5):
                        self.set(x, y, z, block)

    def dome(self, cx: int, y_base: int, cz: int, r: float, block: str,
             hollow: bool = True) -> None:
        """Hemispherical dome whose equator sits on ``y_base``."""
        self.sphere(cx, y_base, cz, r, block, hollow=hollow, y_min=y_base)

    def pyramid(self, cx: int, y1: int, cz: int, base: int, height: int,
                block: str, hollow: bool = False, top_cut: int = 0) -> None:
        """Square pyramid; ``top_cut`` truncates the apex (flat top)."""
        half = base / 2.0
        for k in range(height - top_cut):
            hw = half * (1 - k / height)
            r = int(round(hw))
            if r < 0:
                break
            y = y1 + k
            if hollow and k > 0:
                self.walls(cx - r, y, cz - r, cx + r, y, cz + r, block)
            else:
                self.fill(cx - r, y, cz - r, cx + r, y, cz + r, block)

    def step_pyramid(self, cx: int, y1: int, cz: int, base: int, tiers: int,
                     tier_height: int, block: str, shrink: Optional[int] = None) -> None:
        shrink = shrink or max(2, base // (tiers * 2))
        r = base // 2
        y = y1
        for _ in range(tiers):
            if r <= 0:
                break
            self.fill(cx - r, y, cz - r, cx + r, y + tier_height - 1, cz + r, block)
            r -= shrink
            y += tier_height

    def arch(self, x: int, y1: int, z: int, span: int, height: int, depth: int,
             block: str, axis: str = "x") -> None:
        """A solid wall segment ``span`` wide with a round-topped opening.

        ``axis`` is the direction the wall runs ('x' or 'z'); ``depth`` is
        the wall thickness.  The opening occupies the full span minus one
        block of pier on each side, its top is a semicircle.
        """
        r = (span - 2) / 2.0
        for i in range(span):
            for y in range(y1, y1 + height):
                for d in range(depth):
                    px, pz = (x + i, z + d) if axis == "x" else (x + d, z + i)
                    inner = 1 <= i <= span - 2
                    if inner:
                        # position relative to opening centre
                        cx_ = (i - 1) - r + 0.5
                        top = y1 + height - 1 - r
                        if y <= top or math.hypot(cx_, y - top) <= r + 0.5:
                            continue
                    self.set(px, y, pz, block)

    def ring_wall(self, cx: int, y1: int, cz: int, r: float, height: int,
                  block: str, rz: Optional[float] = None) -> None:
        self.cylinder(cx, y1, cz, r, height, block, hollow=True, rz=rz)

    def crenellate(self, x1: int, y: int, z1: int, x2: int, z2: int, block: str,
                   period: int = 2) -> None:
        """Place merlons along the top edge of a rectangular wall."""
        xa, xb = sorted((x1, x2))
        za, zb = sorted((z1, z2))
        for x in range(xa, xb + 1, period):
            self.set(x, y, za, block)
            self.set(x, y, zb, block)
        for z in range(za, zb + 1, period):
            self.set(xa, y, z, block)
            self.set(xb, y, z, block)

    def gable_roof(self, x1: int, y1: int, z1: int, x2: int, z2: int, block: str,
                   ridge_axis: str = "x", overhang: int = 1) -> int:
        """Stepped gable roof; returns the roof's top y."""
        xa, xb = sorted((x1, x2))
        za, zb = sorted((z1, z2))
        xa -= overhang; xb += overhang; za -= overhang; zb += overhang
        y = y1
        if ridge_axis == "x":
            while za <= zb:
                self.fill(xa, y, za, xb, y, zb, block)
                za += 1; zb -= 1; y += 1
        else:
            while xa <= xb:
                self.fill(xa, y, za, xb, y, zb, block)
                xa += 1; xb -= 1; y += 1
        return y - 1

    def hip_roof(self, x1: int, y1: int, z1: int, x2: int, z2: int, block: str,
                 overhang: int = 1) -> int:
        xa, xb = sorted((x1, x2))
        za, zb = sorted((z1, z2))
        xa -= overhang; xb += overhang; za -= overhang; zb += overhang
        y = y1
        while xa <= xb and za <= zb:
            self.fill(xa, y, za, xb, y, zb, block)
            xa += 1; xb -= 1; za += 1; zb -= 1; y += 1
        return y - 1

    def pagoda_roof(self, cx: int, y: int, cz: int, half: int, block: str,
                    edge: str) -> None:
        """Flared eave: one wide layer with an upturned edge then a narrower layer."""
        self.fill(cx - half, y, cz - half, cx + half, y, cz + half, block)
        self.walls(cx - half, y + 1, cz - half, cx + half, y + 1, cz + half, edge)
        self.fill(cx - half + 2, y + 1, cz - half + 2, cx + half - 2, y + 1, cz + half - 2, block)

    def windows(self, x1: int, y: int, z1: int, x2: int, z2: int, block: str,
                period: int = 3, offset: int = 1) -> None:
        """Punch windows into an existing rectangular wall ring at height ``y``."""
        xa, xb = sorted((x1, x2))
        za, zb = sorted((z1, z2))
        for x in range(xa + offset, xb, period):
            self.set(x, y, za, block)
            self.set(x, y, zb, block)
        for z in range(za + offset, zb, period):
            self.set(xa, y, z, block)
            self.set(xb, y, z, block)

    def tree(self, x: int, y: int, z: int, log: str = "oak_log",
             leaves: str = "oak_leaves[persistent=true]", height: int = 5,
             canopy: int = 2) -> None:
        self.column(x, y, z, height, log)
        self.sphere(x, y + height - 1, z, canopy, leaves, hollow=False)
        self.set(x, y + height - 1, z, log)

    def palm(self, x: int, y: int, z: int, height: int = 7) -> None:
        self.column(x, y, z, height, "jungle_log")
        top = y + height
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            self.set(x + dx, top, z + dz, "jungle_leaves[persistent=true]")
            self.set(x + 2 * dx, top, z + 2 * dz, "jungle_leaves[persistent=true]")
            self.set(x + 3 * dx, top - 1, z + 3 * dz, "jungle_leaves[persistent=true]")
        self.set(x, top, z, "jungle_leaves[persistent=true]")


def iter_rect(x1: int, z1: int, x2: int, z2: int) -> Iterable[Tuple[int, int]]:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for z in range(min(z1, z2), max(z1, z2) + 1):
            yield x, z
