"""Buildable models of premodern technology (``/function ac:tech/<id>``).

Each builder here is referenced by ``tech_model`` in
knowledge/premodern_technology.json.  They are small (20-80 blocks a side)
cut-away or working-principle models, not full landmarks.
"""

from __future__ import annotations

import math
from typing import Callable, Dict

from . import structures as S
from .palettes import ABBASID, CRUSADER, EGYPT, GREECE, INCA, MESOPOTAMIA, ROME, TUSCANY, VIKING
from .voxel import Voxel

Model = Callable[[Voxel], None]
MODELS: Dict[str, Model] = {}


def model(fn: Model) -> Model:
    MODELS[fn.__name__] = fn
    return fn


# ------------------------------------------------------------------ Egypt

@model
def pyramid_ramp(v: Voxel) -> None:
    """Half-built pyramid with a straight haul ramp, a sledge and a lever gang."""
    S.pad(v, -40, -30, 40, 50, "sand")
    v.pyramid(0, 1, 0, 41, 26, "sandstone", top_cut=12)                   # unfinished: flat top
    # the ramp of mud brick and rubble up the south face
    for k in range(14):
        v.fill(-4, 1 + k, 20 + 2 * (13 - k) + 2, 4, 1 + k, 20 + 2 * (13 - k) + 3, "packed_mud")
    v.fill(-4, 1, 46, 4, 1, 48, "packed_mud")
    # sledge with a block, on wetted sand, hauled by a rope
    v.fill(-1, 2, 42, 1, 2, 44, "dark_oak_slab")
    v.fill(-1, 3, 42, 1, 4, 44, "smooth_sandstone")
    v.line((0, 3, 41), (0, 7, 34), "chain")
    v.set(0, 1, 45, "water")
    # a lever gang prising a casing block at the top
    v.fill(-3, 15, -3, 3, 15, 3, "smooth_sandstone")
    v.line((5, 15, 0), (9, 18, 0), "stripped_oak_log")
    v.set(5, 14, 0, "stone")
    # survey trench half full of water: the levelling method
    v.fill(-30, 0, -25, 30, 0, -25, "water")


@model
def shaduf(v: Voxel) -> None:
    """Three shadufs in series lifting water from a canal to a garden terrace."""
    S.pad(v, -14, -10, 14, 20, "grass_block")
    v.fill(-14, 0, -10, 14, 0, -6, "water")
    for i, z in enumerate((-4, 6, 16)):
        y = i * 3
        v.fill(-14, y, z - 2, 14, y, z + 2, "coarse_dirt")
        v.column(-1, y + 1, z, 5, "stripped_oak_log")
        v.column(1, y + 1, z, 5, "stripped_oak_log")
        v.fill(-1, y + 6, z, 1, y + 6, z, "stripped_oak_log")
        v.line((0, y + 6, z + 5), (0, y + 6, z - 6), "oak_fence")
        v.fill(-1, y + 5, z + 5, 1, y + 6, z + 6, "clay")                   # counterweight
        v.line((0, y + 6, z - 6), (0, y + 2 - (3 if i == 0 else 0), z - 6), "chain")
        v.set(0, y + 1 - (3 if i == 0 else 0) + (0 if i == 0 else 0), z - 6, "water_cauldron[level=3]")
        v.fill(-10, y + 1, z - 4, 10, y + 1, z - 4, "water")               # the lifted water channel
    v.fill(-12, 7, 10, 12, 7, 18, "farmland[moisture=7]")
    for x in range(-12, 13, 2):
        v.set(x, 8, 12, "wheat[age=7]"); v.set(x, 8, 16, "melon_stem[age=7]")


@model
def obelisk_quarry(v: Voxel) -> None:
    """The Unfinished Obelisk in its trench, a finished one being tipped upright into a sand pit."""
    S.pad(v, -30, -20, 50, 30, "polished_granite")
    v.fill(-24, 1, -10, 24, 4, 10, "granite")
    v.fill(-22, 1, -3, 22, 4, 3, "air")                                     # trench around the shaft
    v.fill(-20, 1, -1, 20, 3, 1, "polished_granite")                        # the obelisk, still attached
    v.fill(-20, 1, -1, 20, 1, 1, "granite")
    for x in range(-22, 23, 4):
        v.set(x, 5, -4, "stone"); v.set(x, 5, 4, "stone")                   # dolerite pounders
    # raising: an embankment with a sand-filled pit, obelisk sliding in tip first
    v.fill(28, 1, -8, 48, 8, 8, "packed_mud")
    v.fill(38, 1, -3, 46, 8, 3, "sand")
    v.fill(38, 5, -3, 46, 8, 3, "air")
    v.line((30, 9, 0), (42, 2, 0), "polished_granite")
    v.line((30, 10, 0), (42, 3, 0), "polished_granite")
    v.set(44, 1, 0, "polished_granite")                                     # the base block
    v.fill(44, 0, -1, 46, 0, 1, "polished_granite")


# ------------------------------------------------------- Mesopotamia / Persia

@model
def ziggurat(v: Voxel) -> None:
    """Three-tier ziggurat of Ur with fired-brick casing and the triple stair."""
    S.pad(v, -30, -30, 30, 36, "terracotta")
    S.ziggurat(v, 0, 0, MESOPOTAMIA, base=44, tiers=3, tier_h=7)
    v.walls(-22, 1, -22, 22, 7, 22, "bricks")                                # fired brick skin
    for y in range(2, 7, 2):
        v.windows(-22, y, -22, 22, 22, "mud_bricks", period=6, offset=3)   # weep holes


@model
def chariot(v: Voxel) -> None:
    """Solid-wheel ox cart beside a spoked-wheel Egyptian chariot, with a potter's wheel."""
    S.pad(v, -20, -10, 20, 10, "dirt_path")
    # ox cart with solid disc wheels
    v.fill(-16, 2, -3, -8, 2, 3, "oak_planks")
    for z in (-4, 4):
        v.disc(-12, 0, z, 0, "air")
        for a in range(0, 360, 20):
            v.set(round(-12 + 2.5 * math.cos(math.radians(a))), round(2.5 + 2.5 * math.sin(math.radians(a))), z, "oak_planks")
        v.fill(-13, 1, z, -11, 4, z, "oak_planks")
    v.fill(-12, 2, -3, -12, 2, 3, "stripped_oak_log")
    v.line((-8, 2, 0), (-2, 2, 0), "oak_fence")
    # chariot with spoked wheels and a pole
    v.fill(4, 3, -1, 7, 3, 1, "oak_planks")
    v.fill(4, 4, -1, 4, 5, 1, "oak_fence")
    for z in (-2, 2):
        for a in range(0, 360, 30):
            v.set(round(5.5 + 2 * math.cos(math.radians(a))), round(2.5 + 2 * math.sin(math.radians(a))), z, "stripped_birch_log")
        for a in range(0, 360, 60):
            v.set(round(5.5 + 1 * math.cos(math.radians(a))), round(2.5 + 1 * math.sin(math.radians(a))), z, "birch_fence")
    v.line((7, 3, 0), (14, 3, 0), "birch_fence")
    v.fill(14, 1, -2, 16, 4, -1, "brown_wool"); v.fill(14, 1, 1, 16, 4, 2, "brown_wool")   # horses
    # potter's wheel
    v.disc(0, 1, 7, 2, "stone")
    v.column(0, 2, 7, 2, "stripped_oak_log")
    v.disc(0, 4, 7, 1.2, "stone")
    v.set(0, 5, 7, "flower_pot")


@model
def qanat(v: Voxel) -> None:
    """Cut-away hillside: mother well, line of shafts, sloping tunnel, outlet to fields."""
    S.pad(v, -10, -60, 10, 20, "sand")
    for k in range(12):                                                      # the alluvial fan rising to -z
        v.fill(-10, 1 + k, -60, 10, 1 + k, -60 + (12 - k) * 4, "terracotta" if k % 3 else "sand")
    v.fill(-10, -8, -60, 10, -8, 20, "clay")
    v.fill(-10, -7, -60, 10, -7, -40, "water")                               # the aquifer
    # tunnel on a gentle gradient
    for z in range(-58, 16):
        y = -6 + (z + 58) // 12
        v.fill(-1, y, z, 1, y + 1, z, "air")
        if (z + 58) % 12 == 0:
            v.set(0, y, z, "water")
    for z in range(-58, 16, 10):                                             # vertical shafts with spoil rings
        y_top = 12 if z < -30 else max(1, 12 - (z + 30) // 4)
        v.fill(0, -6 + (z + 58) // 12, z, 0, y_top + 1, z, "air")
        v.disc(0, y_top + 1, z, 2, "coarse_dirt", hollow=True)
    v.fill(-1, 0, 16, 1, 0, 20, "water")                                     # the outlet
    v.fill(-9, 0, 17, -2, 0, 20, "farmland[moisture=7]"); v.fill(2, 0, 17, 9, 0, 20, "farmland[moisture=7]")
    v.fill(10, -8, -60, 10, 13, 20, "air")                                   # cut-away face


@model
def panemone(v: Voxel) -> None:
    """Sistan vertical-axis windmill: walled chamber with a slot, reed-mat sails on an upright shaft."""
    S.pad(v, -10, -10, 10, 10, "sand")
    v.fill(-6, 1, -6, 6, 12, 6, "mud_bricks")
    v.fill(-5, 1, -5, 5, 12, 5, "air")
    v.fill(-6, 4, -2, -6, 12, 2, "air")                                      # wind inlet slot
    v.fill(6, 4, 1, 6, 12, 5, "air")                                          # outlet
    v.column(0, 1, 0, 12, "stripped_oak_log")
    for a in range(0, 360, 60):
        dx, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        for r in range(1, 5):
            v.fill(round(r * dx), 5, round(r * dz), round(r * dx), 11, round(r * dz), "hay_block")
    v.disc(0, 2, 0, 2, "stone")                                               # the millstone under the shaft
    v.disc(0, 3, 0, 2, "smooth_stone")
    v.fill(-6, 13, -6, 6, 13, 6, "mud_bricks")


# ------------------------------------------------------------- Greece

@model
def archimedes_screw(v: Voxel) -> None:
    """Inclined screw in a half-open casing lifting water from a pool to a channel."""
    S.pad(v, -6, -14, 26, 10, "grass_block")
    v.fill(-4, -2, -10, 4, 0, -2, "water")
    v.fill(-5, -3, -11, 5, -3, -1, "stone")
    length = 24
    for i in range(length):
        x = i
        y = int(i * 0.55)
        a = i * 0.9
        v.set(x, y, -6, "stripped_oak_log")                                   # axle
        v.set(x, y + round(2 * math.sin(a)), -6 + round(2 * math.cos(a)), "oak_planks")   # helical blade
        v.set(x, y + round(2 * math.sin(a + math.pi)), -6 + round(2 * math.cos(a + math.pi)), "oak_planks")
        if i % 4 == 0:
            v.set(x, y + round(2 * math.sin(a)) - 1, -6 + round(2 * math.cos(a)), "water")
        v.fill(x, y - 3, -9, x, y - 3, -3, "spruce_planks")                  # casing floor
        v.set(x, y - 2, -9, "spruce_planks"); v.set(x, y - 2, -3, "spruce_planks")
    v.fill(22, 11, -9, 26, 11, 8, "smooth_stone")
    v.fill(23, 12, -8, 25, 12, 8, "water")


@model
def antikythera(v: Voxel) -> None:
    """A 12x scale 'exploded' relief of the mechanism: front zodiac dial, crank, gear train, back spiral dials."""
    S.pad(v, -20, -8, 20, 8, "polished_andesite")
    # front dial plate with zodiac ring
    v.disc(-10, 1, 0, 8, "copper_block")
    v.disc(-10, 2, 0, 8, "oxidized_copper", hollow=True)
    v.disc(-10, 2, 0, 6, "weathered_copper", hollow=True)
    for a in range(0, 360, 30):
        v.set(round(-10 + 7 * math.cos(math.radians(a))), 3, round(7 * math.sin(math.radians(a))), "gold_block")
    v.line((-10, 3, 0), (-10, 3, 5), "iron_block")                           # pointer
    v.set(-10, 3, 0, "gold_block")
    # gear train (concentric gears as toothed discs)
    for (x, z, r, b) in ((0, 0, 5, "copper_block"), (6, 3, 3, "exposed_copper"), (6, -3, 2, "exposed_copper"),
                         (10, 0, 4, "weathered_copper")):
        v.disc(x, 1, z, r, b)
        for a in range(0, 360, max(10, int(360 / (r * 6)))):
            v.set(round(x + (r + 1) * math.cos(math.radians(a))), 1, round(z + (r + 1) * math.sin(math.radians(a))), b)
        v.set(x, 2, z, "iron_block")
    v.line((14, 1, 0), (18, 1, 0), "iron_block")                             # crank
    v.set(18, 2, 0, "iron_block"); v.set(18, 3, 0, "oak_fence")
    # back dial: Metonic spiral
    for t in range(0, 720, 6):
        r = 2 + t / 120
        v.set(round(-10 + r * math.cos(math.radians(t))), 1, round(r * math.sin(math.radians(t))), "copper_block")
    v.fill(-20, 0, -8, 20, 0, 8, "polished_andesite")
    v.set(0, 4, -7, "lectern")


@model
def catapult(v: Voxel) -> None:
    """A torsion ballista (bolt thrower) and a one-armed onager side by side."""
    S.pad(v, -14, -8, 14, 8, "grass_block")
    S.catapult(v, 7, 0)
    # ballista: two vertical skeins (frames), arms, slider
    wood = "stripped_oak_log"
    v.fill(-12, 1, -3, -4, 1, 3, wood)
    for z in (-3, 3):
        v.fill(-9, 2, z, -7, 5, z, wood)
        v.fill(-8, 2, z, -8, 5, z, "white_wool")                            # sinew skein
        v.line((-8, 4, z), (-8 - (2 if z < 0 else 2), 4, z + (-5 if z < 0 else 5)), wood)   # arms
    v.line((-10, 4, -8), (-10, 4, 8), "chain")                              # bowstring
    v.line((-13, 3, 0), (-3, 4, 0), wood)                                   # slider / stock
    v.set(-13, 4, 0, "iron_block")                                           # bolt tip


@model
def aeolipile(v: Voxel) -> None:
    """Hero's steam sphere over a cauldron fire, plus his automatic temple doors."""
    S.pad(v, -14, -8, 14, 8, "polished_andesite")
    v.fill(-2, 1, -2, 2, 1, 2, "netherrack"); v.fill(-2, 2, -2, 2, 2, 2, "fire")
    v.fill(-3, 3, -3, 3, 5, 3, "copper_block"); v.fill(-2, 3, -2, 2, 5, 2, "water")
    v.fill(-3, 6, -3, 3, 6, 3, "copper_block")
    v.column(-2, 7, 0, 3, "copper_block"); v.column(2, 7, 0, 3, "copper_block")      # steam pipes
    v.sphere(0, 10, 0, 2, "exposed_copper", hollow=True)
    v.set(0, 10, -3, "copper_block"); v.set(1, 10, -3, "copper_block")       # bent nozzles
    v.set(0, 10, 3, "copper_block"); v.set(-1, 10, 3, "copper_block")
    v.set(0, 12, 0, "white_stained_glass")
    # temple doors: altar fire heats air in a vessel, forcing water into a bucket that pulls the door ropes
    v.fill(8, 1, -4, 13, 6, 4, "quartz_block"); v.fill(9, 1, -3, 12, 5, 3, "air")
    v.fill(10, 1, 4, 11, 4, 4, "air")
    v.set(10, 1, -6, "campfire")
    v.set(10, 0, -5, "copper_block"); v.set(10, -1, -5, "copper_block")
    v.set(10, -2, -3, "water_cauldron[level=3]")
    v.fill(8, -3, -5, 13, -3, 5, "stone")
    v.fill(14, -3, -5, 14, 6, 5, "air")                                      # cut-away


# --------------------------------------------------------------- Rome

@model
def aqueduct(v: Voxel) -> None:
    """A two-tier arcade carrying its channel across a valley into a castellum (distribution tank)."""
    S.pad(v, -4, -8, 80, 12, "grass_block")
    S.aqueduct(v, 0, 0, 56, ROME, span=7, tiers=2, tier_h=9, thickness=3)
    v.fill(56, 1, -2, 66, 20, 6, "stone_bricks")                              # castellum
    v.fill(57, 15, -1, 65, 19, 5, "air")
    v.fill(57, 15, -1, 65, 15, 5, "water")
    for z in (0, 2, 4):
        v.fill(66, 14, z, 76, 14, z, "exposed_copper")                      # three lead mains: baths, fountains, houses
    v.set(2, 22, 1, "oak_fence")                                             # a surveyor's chorobates on the channel
    v.fill(2, 23, 0, 2, 23, 2, "oak_slab")


@model
def arch(v: Voxel) -> None:
    """Arch on its timber centering beside a finished arch, a barrel vault and a groin vault."""
    S.pad(v, -4, -4, 48, 20, "grass_block")
    # under construction: centering with voussoirs half placed
    for i in range(1, 12):
        y = 1 + round(6 * math.sin(math.pi * i / 12))
        v.set(i, y, 0, "oak_planks")
        v.set(i, y - 1, 0, "oak_planks")
    v.fill(0, 1, 0, 0, 6, 0, "stone_bricks"); v.fill(12, 1, 0, 12, 6, 0, "stone_bricks")
    for i in (1, 2, 3, 9, 10, 11):
        y = 1 + round(6 * math.sin(math.pi * i / 12))
        v.set(i, y + 1, 0, "smooth_stone")
    v.set(6, 9, 0, "chiseled_stone_bricks")                                  # the keystone waiting
    v.set(6, 10, 0, "chain"); v.set(6, 11, 0, "oak_fence")
    # finished arch
    v.arch(16, 1, 0, 13, 9, 2, "stone_bricks", axis="x")
    # barrel vault
    for z in range(4, 12):
        v.arch(32, 1, z, 13, 9, 1, "stone_bricks", axis="x")
    # groin vault: two barrel vaults crossing
    for z in range(13, 20):
        v.arch(32, 1, z, 9, 7, 1, "mossy_stone_bricks", axis="x")
    for x in range(32, 41):
        v.arch(x, 1, 12, 9, 7, 1, "mossy_stone_bricks", axis="z")


@model
def roman_road(v: Voxel) -> None:
    """Cut-away road section showing the four layers, with milestone, groma and a bridge."""
    S.pad(v, -4, -8, 60, 8, "grass_block")
    S.roman_road(v, 0, 0, 40, width=7)
    v.fill(0, -4, -6, 12, 0, -4, "air")                                      # cut-away: statumen, rudus, nucleus, pavimentum
    v.fill(13, -4, -5, 13, 0, -5, "air")
    v.fill(0, -3, -5, 12, -3, -5, "cobblestone")
    v.fill(0, -2, -5, 12, -2, -5, "gravel")
    v.fill(0, -1, -5, 12, -1, -5, "andesite")
    v.column(20, 1, 6, 4, "oak_fence"); v.fill(19, 5, 5, 21, 5, 7, "oak_fence")   # the groma
    v.fill(40, 0, -5, 52, 0, 5, "water"); v.fill(40, -3, -5, 52, -1, 5, "water")
    S.arched_bridge(v, 40, -3, 12, 7, ROME, arches=2, axis="x", deck_y=0)
    v.fill(53, 0, -3, 60, 0, 3, "polished_andesite")


@model
def hypocaust(v: Voxel) -> None:
    """Bath-house cut-away: furnace, pilae under the floor, box-tile walls, caldarium pool."""
    S.pad(v, -4, -4, 26, 16, "stone")
    v.fill(0, -3, 0, 22, -3, 12, "stone")
    for x in range(1, 22, 2):                                                 # pilae (brick piers)
        for z in range(1, 12, 2):
            v.fill(x, -2, z, x, 0, z, "bricks")
    v.fill(0, 1, 0, 22, 1, 12, "smooth_stone")                                # suspended floor
    v.fill(0, 2, 0, 22, 6, 12, "terracotta"); v.fill(1, 2, 1, 21, 6, 11, "air")
    v.fill(0, 2, 0, 0, 6, 12, "orange_terracotta")                            # box-tile wall
    v.fill(22, 2, 0, 22, 6, 12, "orange_terracotta")
    v.fill(-4, -2, 5, -1, 0, 7, "air"); v.fill(-4, -3, 5, -1, -3, 7, "netherrack"); v.fill(-4, -2, 5, -1, -2, 7, "fire")
    v.fill(-1, -2, 5, 0, 0, 7, "air")
    v.fill(2, 2, 2, 8, 2, 10, "water")                                        # hot plunge
    v.fill(0, 7, 0, 22, 7, 12, "terracotta")
    v.set(0, 8, 2, "campfire"); v.set(22, 8, 10, "campfire")                  # roof flues
    v.fill(0, -3, 13, 22, 7, 16, "air")                                       # cut-away face


@model
def treadwheel_crane(v: Voxel) -> None:
    """Treadwheel crane with a jib, compound pulley and a block hanging from a lewis."""
    S.pad(v, -10, -10, 14, 10, "grass_block")
    wood = "stripped_oak_log"
    v.fill(-4, 1, -4, 4, 1, 4, wood)
    for a in range(0, 360, 12):                                               # treadwheel
        v.set(-2, 5 + round(4.5 * math.sin(math.radians(a))), round(4.5 * math.cos(math.radians(a))), wood)
        v.set(-3, 5 + round(4.5 * math.sin(math.radians(a))), round(4.5 * math.cos(math.radians(a))), wood)
    v.fill(-4, 5, 0, 4, 5, 0, "iron_block")                                    # axle
    v.line((0, 1, 0), (0, 16, 0), wood)                                        # mast
    v.line((0, 16, 0), (12, 10, 0), wood)                                      # jib
    v.line((12, 10, 0), (12, 4, 0), "chain")
    v.fill(11, 9, 0, 13, 9, 0, "iron_block")                                   # pulley block
    v.fill(11, 2, -1, 13, 3, 1, "smooth_stone")                                # the lifted block
    v.set(12, 4, 0, "iron_bars")                                               # lewis iron
    v.line((0, 10, 0), (8, 1, 0), "oak_fence")                                 # guy


@model
def watermill_cascade(v: Voxel) -> None:
    """Three overshot wheels in a Barbegal-style cascade, each turning a millstone."""
    S.pad(v, -8, -10, 40, 10, "grass_block")
    for i in range(3):
        x = i * 12
        base = 20 - i * 7
        v.fill(x - 6, base + 6, -2, x + 6, base + 6, -1, "smooth_stone")      # head race
        v.fill(x - 6, base + 7, -2, x + 6, base + 7, -1, "water")
        for a in range(0, 360, 20):                                             # the wheel
            v.set(x + 4, base + 2 + round(4 * math.sin(math.radians(a))), round(4 * math.cos(math.radians(a))), "stripped_spruce_log")
        v.fill(x + 3, base + 2, 0, x + 5, base + 2, 0, "iron_block")
        v.fill(x - 6, base - 1, 1, x + 2, base + 5, 6, "stone_bricks")           # mill room
        v.fill(x - 5, base, 2, x + 1, base + 4, 5, "air")
        v.disc(x - 2, base, 3, 1.5, "smooth_stone")
        v.fill(x - 6, base + 6, 1, x + 2, base + 6, 6, "dark_oak_planks")
        v.fill(x - 6, base - 1, -2, x + 6, base - 1, -1, "water")               # tail race to the next wheel
    v.fill(-8, 0, -4, 40, 0, 4, "water")


@model
def siege_tower(v: Voxel) -> None:
    """Siege tower on its ramp at a curtain wall, with a ram under a testudo shed."""
    S.pad(v, -20, -12, 24, 12, "grass_block")
    v.fill(10, 1, -12, 14, 12, 12, "stone_bricks")
    v.crenellate(10, 13, -12, 14, 12, "stone_bricks")
    for k in range(8):
        v.fill(-10 + k * 2, 1 + k, -5, -9 + k * 2, 1 + k, 5, "coarse_dirt")   # ramp
    S.siege_tower(v, 2, -3)
    v.fill(-18, 1, 6, -6, 4, 10, "spruce_planks"); v.fill(-17, 1, 7, -7, 3, 9, "air")
    v.fill(-19, 1, 8, -5, 2, 8, "stripped_dark_oak_log")                        # the ram
    v.set(-5, 2, 8, "iron_block")


# ------------------------------------------------------------------ China

@model
def blast_furnace(v: Voxel) -> None:
    """Han water-powered blast furnace: waterwheel, bellows, tall shaft furnace, pig mould."""
    S.pad(v, -12, -8, 14, 10, "stone")
    v.fill(-12, -2, -8, -6, 0, 8, "water")
    for a in range(0, 360, 20):
        v.set(-9, 1 + round(3.5 * math.sin(math.radians(a))), round(3.5 * math.cos(math.radians(a))), "stripped_spruce_log")
    v.fill(-10, 1, 0, -2, 1, 0, "iron_block")                                   # shaft to the bellows cam
    v.fill(-4, 1, -3, -1, 3, 3, "brown_wool")                                    # leather bellows
    v.fill(-1, 2, 0, 2, 2, 0, "exposed_copper")                                   # tuyere
    for k in range(9):                                                            # tapering clay furnace
        r = 4 - k // 3
        v.fill(3 - r, 1 + k, -r, 3 + r, 1 + k, r, "terracotta")
        v.fill(3 - r + 1, 1 + k, -r + 1, 3 + r - 1, 1 + k, r - 1, "lava" if k < 3 else ("coal_block" if k % 2 else "raw_iron_block"))
    v.set(3, 10, 0, "fire")
    v.fill(7, 1, -1, 7, 1, 1, "air"); v.fill(6, 1, 0, 12, 1, 0, "lava")           # tap hole and runner
    v.fill(8, 0, -3, 12, 0, 3, "stone"); v.fill(9, 1, -2, 11, 1, 2, "lava")        # pig / mould bed
    v.set(7, 2, 3, "anvil")


@model
def pound_lock(v: Voxel) -> None:
    """Canal pound lock between two levels with a barge in the chamber."""
    S.pad(v, -8, -20, 8, 24, "grass_block")
    v.fill(-4, -3, -20, 4, 0, -6, "water")                                       # lower pound
    v.fill(-5, -4, -20, 5, -4, 24, "stone")
    v.fill(-5, -3, -20, -5, 2, 24, "stone_bricks"); v.fill(5, -3, -20, 5, 2, 24, "stone_bricks")
    v.fill(-4, -3, -5, 4, 2, -5, "dark_oak_planks")                               # lower gate (closed)
    v.fill(-4, -3, -4, 4, 1, 9, "water")                                          # chamber, filled
    v.fill(-4, -3, 10, 4, 3, 10, "dark_oak_planks")                               # upper gate
    v.fill(-1, 1, 10, 1, 2, 10, "air")                                            # paddle sluice open
    v.fill(-4, 0, 11, 4, 1, 24, "water")                                          # upper pound
    v.fill(-4, 1, 10, 4, 1, 10, "dark_oak_planks")
    v.fill(-3, 1, -2, 3, 2, 6, "spruce_planks"); v.fill(-2, 2, -1, 2, 2, 5, "air")   # barge
    v.column(-6, 3, -5, 2, "oak_fence"); v.fill(-7, 5, -5, -5, 5, -5, "oak_fence")   # balance beams
    v.column(6, 3, 10, 2, "oak_fence"); v.fill(5, 5, 10, 7, 5, 10, "oak_fence")


# ------------------------------------------------------------------ India

@model
def iron_pillar(v: Voxel) -> None:
    """The Delhi pillar at 1:1 (7.2 m = 7 blocks) in a courtyard, with a bloomery beside it."""
    S.pad(v, -10, -10, 10, 10, "red_sandstone")
    v.fill(-1, 1, -1, 1, 1, 1, "smooth_stone")
    v.column(0, 2, 0, 6, "iron_block")
    v.set(0, 8, 0, "chain"); v.set(0, 9, 0, "iron_block")                        # bell capital
    v.walls(-6, 1, -6, 6, 1, 6, "red_sandstone")                                     # courtyard kerb
    v.cone(7, 1, 7, 2, 4, "terracotta"); v.set(7, 1, 7, "lava"); v.set(7, 5, 7, "fire")   # bloomery
    v.set(5, 1, 9, "anvil")


@model
def stepwell(v: Voxel) -> None:
    S.pad(v, -20, -20, 20, 24, "red_sandstone")
    from .palettes import INDIA
    S.stepwell(v, 0, 0, INDIA, half=14, depth=12)


# ------------------------------------------------------- Islamic world

@model
def astrolabe(v: Voxel) -> None:
    """A giant astrolabe laid flat: mater, plate with almucantars, rete with star pointers, alidade."""
    S.pad(v, -16, -16, 16, 16, "smooth_sandstone")
    v.disc(0, 1, 0, 14, "copper_block")
    v.disc(0, 2, 0, 14, "oxidized_copper", hollow=True)                            # the limb with hour scale
    for a in range(0, 360, 15):
        v.set(round(13 * math.cos(math.radians(a))), 2, round(13 * math.sin(math.radians(a))), "gold_block")
    for r in (3, 6, 9, 12):                                                         # almucantars (altitude circles), offset for latitude
        v.disc(0, 2, 2, r, "weathered_copper", hollow=True)
    v.disc(0, 2, 0, 10, "exposed_copper", hollow=True)                              # ecliptic ring of the rete
    for (x, z) in ((3, -8), (-6, 4), (7, 5), (-2, -3), (9, -2), (-8, -7)):          # star pointers
        v.set(x, 3, z, "gold_block"); v.set(x, 2, z, "gold_block")
    v.fill(-12, 4, 0, 12, 4, 0, "iron_block")                                       # alidade
    v.set(0, 5, 0, "iron_block")
    v.set(0, 3, -15, "chain"); v.set(0, 4, -15, "chain")                            # suspension ring


@model
def elephant_clock(v: Voxel) -> None:
    """Al-Jazari's elephant water clock: elephant, howdah tower, dragons, phoenix and the water tank inside."""
    S.pad(v, -10, -10, 10, 10, "polished_diorite")
    v.fill(-5, 2, -3, 5, 6, 3, "gray_wool")                                          # elephant body
    for px in (-4, 4):
        for pz in (-2, 2):
            v.fill(px, 1, pz, px, 1, pz, "gray_wool")
    v.fill(6, 3, -2, 8, 6, 2, "gray_wool"); v.line((9, 4, 0), (11, 1, 0), "gray_wool")   # head and trunk
    v.fill(-2, 1, -2, 2, 6, 2, "water")                                              # the tank inside
    v.set(0, 5, 0, "copper_block")                                                   # the perforated float bowl
    v.fill(-3, 7, -3, 3, 7, 3, "red_wool")                                            # carpet
    v.fill(-3, 8, -3, 3, 13, 3, "white_concrete"); v.fill(-2, 8, -2, 2, 13, 2, "air")   # howdah tower
    v.set(0, 9, 0, "lectern")                                                        # the scribe
    v.fill(-4, 14, -4, 4, 14, 4, "red_terracotta")
    v.pyramid(0, 15, 0, 7, 4, "red_terracotta")
    v.set(0, 19, 0, "gold_block")                                                    # the phoenix
    for side in (-1, 1):
        v.line((side * 4, 14, 0), (side * 6, 10, 0), "lime_concrete")                 # the dragons
        v.set(side * 6, 9, 0, "lime_concrete")
    v.set(-5, 12, -4, "bell")                                                        # the cymbal
    v.set(7, 5, 3, "iron_block")                                                     # the mahout's hammer


@model
def noria(v: Voxel) -> None:
    """River-driven noria pouring into an aqueduct, with an ox-driven saqiya beside it."""
    S.pad(v, -16, -12, 20, 12, "grass_block")
    v.fill(-16, -3, -4, 20, 0, 4, "water")
    for a in range(0, 360, 12):
        v.set(0, 1 + round(8 * math.sin(math.radians(a))), round(8 * math.cos(math.radians(a))), "stripped_jungle_log")
        if a % 36 == 0:
            v.set(0, 1 + round(8 * math.sin(math.radians(a))), round(8 * math.cos(math.radians(a))), "decorated_pot")
    v.fill(-1, 1, 0, 1, 1, 0, "iron_block")
    v.fill(-2, 9, -10, 2, 9, -8, "smooth_sandstone"); v.fill(-16, 9, -10, 2, 9, -10, "smooth_sandstone")
    v.fill(-16, 10, -10, 2, 10, -10, "water")
    # saqiya: ox walks a circle turning a lantern gear that drives a pot wheel over a well
    v.disc(14, 0, 8, 5, "dirt_path")
    v.column(14, 1, 8, 4, "stripped_oak_log")
    v.disc(14, 3, 8, 3, "oak_fence", hollow=True)                                    # horizontal lantern gear
    v.line((14, 2, 8), (14, 2, 13), "oak_fence")                                     # the sweep
    v.fill(13, 1, 13, 15, 3, 14, "brown_wool")                                       # the ox
    for a in range(0, 360, 30):
        v.set(10, 2 + round(2.5 * math.sin(math.radians(a))), 8 + round(2.5 * math.cos(math.radians(a))), "jungle_fence")
    v.fill(9, -3, 7, 9, 0, 9, "air"); v.fill(9, -4, 7, 9, -4, 9, "water")            # the well


# ------------------------------------------------------- Medieval Europe

@model
def trebuchet(v: Voxel) -> None:
    S.pad(v, -24, -8, 12, 8, "grass_block")
    S.trebuchet(v, 0, 0)
    v.fill(-24, 1, -8, -20, 8, 8, "stone_bricks")                                    # the target wall
    v.fill(-22, 3, -2, -20, 6, 2, "air"); v.fill(-23, 1, -1, -21, 1, 1, "cobblestone")   # the breach


@model
def three_field(v: Voxel) -> None:
    """Three open fields (winter wheat, spring oats, fallow with sheep), a heavy plough and horse."""
    S.pad(v, -30, -12, 30, 12, "grass_block")
    v.fill(-30, 0, -12, -11, 0, 12, "farmland[moisture=7]")
    for x in range(-29, -11, 2):
        for z in range(-11, 12, 2):
            v.set(x, 1, z, "wheat[age=7]")
    v.fill(-9, 0, -12, 10, 0, 12, "farmland[moisture=7]")
    for x in range(-8, 10, 2):
        for z in range(-11, 12, 2):
            v.set(x, 1, z, "wheat[age=3]")
    for (x, z) in ((14, -6), (20, 2), (26, -8), (17, 8), (25, 6)):
        v.fill(x, 1, z, x + 1, 1, z, "white_wool")                                   # sheep on the fallow
    for z in range(-12, 13, 4):                                                       # furrows in the plough strip
        v.fill(-9, 0, z, 10, 0, z, "coarse_dirt")
    # heavy plough: wheels, coulter, share, mouldboard; horse in a collar
    v.fill(-4, 1, 0, 1, 1, 0, "stripped_oak_log")
    v.set(-4, 1, -1, "oak_planks"); v.set(-4, 1, 1, "oak_planks")
    v.set(0, 1, 0, "iron_block"); v.set(1, 0, 0, "iron_block"); v.set(1, 1, 1, "stone_bricks")
    v.fill(-9, 1, -1, -6, 3, 1, "brown_wool")                                        # the horse
    v.set(-5, 2, 0, "stripped_oak_log")                                              # collar
    v.line((-3, 4, 0), (3, 4, 0), "oak_fence")                                       # ploughman's handles


@model
def post_mill(v: Voxel) -> None:
    S.pad(v, -14, -10, 14, 12, "grass_block")
    S.windmill(v, -7, 0, VIKING, style="post")
    S.windmill(v, 7, 0, TUSCANY, style="tower")


@model
def clock_tower(v: Voxel) -> None:
    """Belfry with weight-driven clock: drum, crown wheel, verge-and-foliot escapement, bell and dial."""
    S.pad(v, -8, -8, 8, 8, "cobblestone")
    v.fill(-4, 1, -4, 4, 20, 4, "stone_bricks"); v.fill(-3, 1, -3, 3, 19, 3, "air")
    v.fill(-4, 21, -4, 4, 21, 4, "stone_bricks")
    v.pyramid(0, 22, 0, 9, 5, "deepslate_tiles")
    v.fill(-3, 16, -3, 3, 16, 3, "air"); v.set(0, 18, 0, "bell")
    v.windows(-4, 17, -4, 4, 4, "air", period=2, offset=1)
    # the movement, visible through a cut-away in the south wall
    v.fill(-2, 6, 4, 2, 13, 4, "air")
    v.fill(-1, 8, 0, 1, 8, 0, "stripped_oak_log")                                    # the barrel (drum)
    v.line((0, 7, 0), (0, 2, 0), "chain"); v.set(0, 1, 0, "iron_block")                # the driving weight
    for a in range(0, 360, 30):                                                        # crown wheel
        v.set(round(2 * math.cos(math.radians(a))), 10 + round(2 * math.sin(math.radians(a))), 1, "copper_block")
    v.fill(0, 9, 2, 0, 13, 2, "iron_bars")                                             # the verge
    v.fill(-2, 13, 2, 2, 13, 2, "stripped_oak_log")                                    # the foliot with weights
    v.set(-2, 14, 2, "iron_block"); v.set(2, 14, 2, "iron_block")
    v.disc(0, 15, -4, 2.5, "white_concrete")                                           # dial on the north face
    for y in range(13, 18):
        for x in range(-2, 3):
            if math.hypot(x, y - 15) <= 2.5:
                v.set(x, y, -4, "white_concrete")
    v.set(0, 15, -4, "black_concrete"); v.set(0, 16, -4, "black_concrete"); v.set(1, 15, -4, "black_concrete")


@model
def flying_buttress(v: Voxel) -> None:
    """One bay of a Gothic nave in section: pointed arch, rib vault, clerestory glass, flying buttress and pinnacle."""
    S.pad(v, -16, -6, 16, 6, "stone")
    for side in (-1, 1):
        px = side * 6
        v.fill(px, 1, -4, px, 14, 4, "stone_bricks")                                    # nave pier / wall
        v.fill(px, 8, -3, px, 13, 3, "blue_stained_glass_pane")                         # clerestory
        v.fill(px, 8, -4, px, 13, -4, "stone_bricks"); v.fill(px, 8, 4, px, 13, 4, "stone_bricks")
        bx = side * 13
        v.fill(bx, 1, -1, bx, 20, 1, "stone_bricks")                                    # outer buttress pier
        v.cone(bx, 21, 0, 1.5, 4, "stone_bricks")                                        # pinnacle
        for k in range(7):                                                               # the flyer (a quarter arch)
            x = bx - side * k
            y = 16 - int(4 * (1 - math.cos(math.radians(k * 13))))
            v.set(x, y, 0, "stone_bricks"); v.set(x, y - 1, 0, "stone_bricks")
        v.fill(min(px, bx) + 1 if side < 0 else px + 1, 1, -3, max(px, bx) - 1 if side < 0 else bx - 1, 7, 3,
               "air")
        v.fill(min(px, bx), 8, -3, max(px, bx), 8, 3, "deepslate_tiles")               # aisle roof
    for i in range(-6, 7):                                                               # pointed arch rib
        y = 15 + int(6 * (1 - (abs(i) / 6) ** 1.6))
        v.set(i, y, 0, "chiseled_stone_bricks"); v.set(i, y - 1, 0, "stone_bricks")
        v.fill(i, y + 1, -4, i, y + 1, 4, "cobblestone")                                 # vault web
    v.fill(-7, 22, -5, 7, 22, 5, "deepslate_tiles")                                      # nave roof line
    v.fill(-16, 1, -6, 16, 0, -6, "air")


@model
def printing_press(v: Voxel) -> None:
    """Gutenberg's shop: screw press, type cases, composing stone, drying lines, a scribe's desk for contrast."""
    S.pad(v, -10, -8, 10, 8, "oak_planks")
    v.walls(-10, 1, -8, 10, 6, 8, "white_concrete"); v.fill(-10, 7, -8, 10, 7, 8, "dark_oak_planks")
    v.fill(-2, 1, 8, 2, 4, 8, "air")
    v.fill(-2, 1, -2, 2, 1, 2, "dark_oak_planks")                                        # press bed
    v.column(-3, 1, 0, 6, "stripped_dark_oak_log"); v.column(3, 1, 0, 6, "stripped_dark_oak_log")
    v.fill(-3, 7, 0, 3, 7, 0, "stripped_dark_oak_log")
    v.fill(0, 3, 0, 0, 6, 0, "iron_bars")                                                 # the screw
    v.fill(-1, 2, -1, 1, 2, 1, "smooth_stone")                                           # platen
    v.line((0, 5, 0), (0, 5, 4), "oak_fence")                                             # the bar
    v.fill(-9, 1, -7, -5, 1, -3, "chiseled_bookshelf"); v.set(-7, 2, -5, "iron_block")      # type cases
    v.fill(5, 1, -7, 9, 1, -3, "smooth_stone")
    v.fill(-8, 5, 2, 8, 5, 2, "chain")                                                    # drying line
    for x in range(-7, 8, 3):
        v.set(x, 4, 2, "white_wool")
    v.set(7, 1, 5, "lectern"); v.set(7, 2, 5, "candle")                                   # the scribe's desk
    v.fill(-8, 1, 4, -5, 1, 6, "bookshelf")


@model
def motte_and_bailey(v: Voxel) -> None:
    """Norman motte with timber tower, palisaded bailey, ditch and bridge."""
    S.pad(v, -36, -30, 36, 30, "grass_block")
    for k in range(10):
        v.disc(-14, 1 + k, 0, 14 - k * 1.2, "coarse_dirt" if k % 2 else "grass_block")
    v.disc(-14, 0, 0, 16, "water", hollow=True); v.disc(-14, 0, 0, 17, "water", hollow=True)   # ditch
    v.fill(-18, 11, -4, -10, 18, 4, "spruce_planks"); v.fill(-17, 11, -3, -11, 17, 3, "air")
    v.fill(-18, 19, -4, -10, 19, 4, "dark_oak_planks")
    for a in range(0, 360, 20):
        v.column(round(-14 + 13 * math.cos(math.radians(a))), 11, round(13 * math.sin(math.radians(a))), 3, "spruce_fence")
    for x in range(2, 33, 2):                                                               # bailey palisade
        v.column(x, 1, -18, 4, "spruce_fence"); v.column(x, 1, 18, 4, "spruce_fence")
    for z in range(-18, 19, 2):
        v.column(32, 1, z, 4, "spruce_fence"); v.column(2, 1, z, 4, "spruce_fence")
    v.fill(2, 1, -2, 2, 4, 2, "air")
    v.walls(2, 0, -18, 32, 0, 18, "water")
    S.house(v, 8, -14, 10, 7, CRUSADER, floors=1, roof="gable", wall="oak_planks")           # hall
    S.house(v, 20, 6, 8, 6, CRUSADER, floors=1, roof="gable", wall="cobblestone")             # chapel
    v.fill(10, 1, 8, 14, 1, 12, "hay_block")
    for k in range(10):                                                                     # bridge up the motte
        v.fill(2 - k, 1 + k, -1, 3 - k, 1 + k, 1, "oak_planks")


# ------------------------------------------------------------ Americas

@model
def inca_bridge(v: Voxel) -> None:
    """Grass-rope suspension bridge across a gorge, with stone anchors and a stretch of Inca road."""
    S.pad(v, -30, -10, 30, 10, "grass_block")
    v.fill(-12, -30, -10, 12, 0, 10, "air")
    v.fill(-12, -31, -10, 12, -31, 10, "water")
    v.fill(-14, -30, -10, -13, 0, 10, "stone"); v.fill(13, -30, -10, 14, 0, 10, "stone")
    v.fill(-16, 1, -3, -13, 3, 3, "polished_andesite"); v.fill(13, 1, -3, 16, 3, 3, "polished_andesite")   # anchors
    for i in range(-13, 14):
        sag = int(5 * (1 - (i / 13) ** 2))
        v.fill(i, 1 - sag, -1, i, 1 - sag, 1, "hay_block")                                 # the woven deck
        v.set(i, 3 - sag, -2, "oak_fence"); v.set(i, 3 - sag, 2, "oak_fence")               # handrail cables
        v.set(i, 2 - sag, -2, "chain"); v.set(i, 2 - sag, 2, "chain")
    v.fill(-30, 0, -2, -14, 0, 2, "andesite"); v.fill(14, 0, -2, 30, 0, 2, "andesite")      # Qhapaq Nan
    for x in range(-28, -14, 4):
        v.set(x, 1, 3, "polished_andesite")
    S.house(v, 18, -9, 8, 5, INCA, floors=1, roof="gable", wall="polished_andesite")        # tambo / qollqa


@model
def andean_terraces(v: Voxel) -> None:
    """Moray-style concentric terraced bowl with stone steps and an irrigation channel."""
    S.pad(v, -30, -30, 30, 30, "grass_block")
    for k in range(8):
        r = 28 - k * 3.4
        v.disc(0, -k, 0, r, "grass_block")
        v.disc(0, -k, 0, r, "polished_andesite", hollow=True)
        v.disc(0, -k - 1, 0, r, "polished_andesite", hollow=True)
        for a in range(10, 360, 90):
            v.set(round((r - 1) * math.cos(math.radians(a))), -k, round((r - 1) * math.sin(math.radians(a))), "stone")
        if k % 2:
            for a in range(0, 360, 20):
                v.set(round((r - 2) * math.cos(math.radians(a))), -k + 1, round((r - 2) * math.sin(math.radians(a))), "wheat[age=7]")
                v.set(round((r - 2) * math.cos(math.radians(a))), -k, round((r - 2) * math.sin(math.radians(a))), "farmland[moisture=7]")
    v.fill(0, 0, -30, 0, 0, -28, "water")
    for k in range(8):
        v.set(0, -k, -28 + k * 3, "water")


@model
def chinampa(v: Voxel) -> None:
    """Raised fields in the lake: wattle fences, willow anchors, canals and a canoe."""
    S.pad(v, -30, -20, 30, 20, "water")
    v.fill(-30, -3, -20, 30, -1, 20, "water")
    for i in range(4):
        x = -28 + i * 15
        v.fill(x, -2, -16, x + 8, 0, 16, "mud")
        v.fill(x, 1, -16, x + 8, 1, 16, "moss_block")
        v.walls(x, 0, -16, x + 8, 1, 16, "oak_fence")
        for z in range(-14, 17, 4):
            v.set(x + 2, 2, z, "wheat[age=7]"); v.set(x + 5, 2, z + 1, "melon_stem[age=7]")
            v.set(x + 4, 2, z + 2, "sweet_berry_bush[age=3]")
        v.tree(x, 2, -16, "oak_log", "oak_leaves[persistent=true]", height=4, canopy=2)
        v.tree(x + 8, 2, 16, "oak_log", "oak_leaves[persistent=true]", height=4, canopy=2)
    v.fill(-10, 0, -19, -4, 0, -19, "dark_oak_planks"); v.set(-11, 1, -19, "dark_oak_planks")   # canoe


@model
def mesoamerican_pyramid(v: Voxel) -> None:
    """Nine-tier stepped pyramid with four stairways and a temple on top (El Castillo type)."""
    S.pad(v, -30, -30, 30, 30, "grass_block")
    S.ziggurat(v, 0, 0, {**MESOPOTAMIA, "wall": "smooth_stone", "trim": "stone"}, base=48, tiers=9, tier_h=3)
    for a in (0, 90, 180, 270):
        for k in range(27):
            r = 24 - k * 0.85
            x = round(r * math.cos(math.radians(a))); z = round(r * math.sin(math.radians(a)))
            w = 2
            v.fill(x - (w if a % 180 else 0), 1 + k, z - (0 if a % 180 else w), x + (w if a % 180 else 0), 1 + k, z + (0 if a % 180 else w), "stone")
    v.set(0, 1, 26, "lime_terracotta"); v.set(0, 1, -26, "lime_terracotta")             # serpent heads
    v.fill(-1, 28, -1, 1, 30, 1, "chiseled_sandstone")


@model
def great_zimbabwe(v: Voxel) -> None:
    """The Great Enclosure's dry-stone elliptical wall, parallel passage and conical tower."""
    S.pad(v, -40, -30, 40, 30, "grass_block")
    v.cylinder(0, 1, 0, 34, 10, "stone", hollow=True, rz=24)
    v.cylinder(0, 1, 0, 33, 10, "stone", hollow=True, rz=23)
    v.cylinder(0, 1, 0, 32, 6, "stone", hollow=True, rz=22)
    for a in range(0, 360, 4):                                                                # chevron pattern course
        v.set(round(34 * math.cos(math.radians(a))), 9 if a % 8 else 10, round(24 * math.sin(math.radians(a))), "andesite")
    v.cylinder(0, 1, 0, 30, 6, "stone", hollow=True, rz=20)
    for a in range(300, 420, 2):                                                               # parallel passage
        px, pz = round(31 * math.cos(math.radians(a))), round(21 * math.sin(math.radians(a)))
        v.fill(px, 1, pz, px, 6, pz, "air")
    v.fill(-3, 1, 20, 3, 10, 26, "air")                                                          # the entrance
    v.cone(18, 1, 8, 5, 12, "stone")                                                             # conical tower
    v.cylinder(18, 1, 8, 5, 4, "stone")
    for i in range(5):
        v.cylinder(-20 + i * 9, 1, -8, 2.5, 3, "packed_mud", hollow=True)                          # daga huts
        v.cone(-20 + i * 9, 4, -8, 3.5, 3, "hay_block")


TECH_BUILD_NOTES = {
    "pyramid_ramp": "Half-built pyramid with haul ramp, sledge on wetted sand, lever gang and the water-levelling trench.",
    "shaduf": "Three shadufs lifting water in series from a canal to a terrace garden.",
    "obelisk_quarry": "The Unfinished Obelisk in its trench with dolerite pounders, and one being tipped into a sand pit.",
    "ziggurat": "Ur-type ziggurat: fired-brick skin, weep holes, triple stair and shrine.",
    "chariot": "Solid-wheel ox cart, spoked chariot with horses, and a potter's wheel.",
    "qanat": "Cut-away hillside showing mother well, shafts, graded tunnel and outlet fields.",
    "panemone": "Sistan vertical-axis windmill with inlet slot and reed sails over a millstone.",
    "archimedes_screw": "Inclined screw in a casing lifting water from a pool to a channel.",
    "antikythera": "Exploded relief: zodiac dial, gear train, crank and pointer.",
    "catapult": "Torsion ballista and onager.",
    "aeolipile": "Hero's steam sphere over a fire, and his automatic temple doors in cut-away.",
    "aqueduct": "Two-tier arcade into a castellum with three lead mains.",
    "arch": "Arch on centering, finished arch, barrel vault and groin vault.",
    "roman_road": "Four-layer road in cut-away, groma, milestone and a bridge.",
    "hypocaust": "Bath cut-away: furnace, pilae, box-tile walls, plunge, roof flues.",
    "treadwheel_crane": "Treadwheel, jib, pulley block and lewis holding a stone.",
    "watermill_cascade": "Three overshot wheels in cascade, each driving a millstone.",
    "siege_tower": "Siege tower on a ramp at a wall, with a ram under its shed.",
    "blast_furnace": "Han furnace with waterwheel-driven bellows, tap hole and pig bed.",
    "pound_lock": "Lock chamber between two levels with a barge inside.",
    "iron_pillar": "The Delhi pillar at 1:1 with a bloomery beside it.",
    "stepwell": "Chand Baori type stepwell, 12 storeys down to the water.",
    "astrolabe": "Giant astrolabe: limb, almucantars, rete, star pointers, alidade.",
    "elephant_clock": "Al-Jazari's elephant clock with tank, float, scribe, dragons and phoenix.",
    "noria": "River noria filling an aqueduct, and an ox-driven saqiya over a well.",
    "trebuchet": "Counterweight trebuchet and a breached wall.",
    "three_field": "Three open fields in rotation with a heavy plough and collared horse.",
    "post_mill": "A post mill beside a tower mill.",
    "clock_tower": "Belfry with weight, drum, crown wheel, verge and foliot, bell and dial.",
    "flying_buttress": "One nave bay in section: pointed rib vault, clerestory, flyers, pinnacles.",
    "printing_press": "Screw press, type cases, composing stone, drying lines and a scribe's desk.",
    "motte_and_bailey": "Motte with timber tower, ditch, palisaded bailey with hall and chapel.",
    "inca_bridge": "Grass-rope suspension bridge over a gorge on the Inca road.",
    "andean_terraces": "Moray-style concentric terraced bowl with irrigation channel.",
    "chinampa": "Raised lake fields with wattle fences, willows, canals and a canoe.",
    "mesoamerican_pyramid": "Nine-tier pyramid with four stairways and serpent heads.",
    "great_zimbabwe": "Elliptical dry-stone Great Enclosure with conical tower and daga huts.",
}
