"""Victorian London - Assassin's Creed Syndicate (2015), 1868."""

from .. import structures as S
from ..palettes import LONDON
from ..registry import Build, World
from ..voxel import Voxel

P = LONDON


def westminster(v: Voxel) -> None:
    """The Palace of Westminster with the clock tower (Big Ben, 1859) on the Thames."""
    S.pad(v, -90, -40, 90, 60, "stone")
    v.fill(-90, -3, 30, 90, 0, 60, "water")
    v.fill(-90, 0, 28, 90, 0, 29, "smooth_stone")
    # long river front in Gothic Revival
    v.fill(-80, 1, 0, 80, 16, 26, P["wall"])
    v.fill(-79, 1, 1, 79, 15, 25, "air")
    v.fill(-79, 1, 1, 79, 1, 25, P["floor"])
    for y in range(3, 15, 3):
        v.windows(-80, y, 0, 80, 26, P["window"], period=3, offset=2)
    for x in range(-80, 81, 8):
        v.column(x, 1, 26, 18, P["trim"])
        v.set(x, 19, 26, P["trim"])
    v.crenellate(-80, 17, 0, 80, 26, P["trim"], period=2)
    S.tower(v, -40, 10, 8, 30, P, top="flat", square=True, wall=P["wall"])         # Victoria Tower
    v.crenellate(-48, 31, 2, -32, 18, P["trim"])
    # Elizabeth Tower: 96 m, 4 clock faces
    cx, cz = 70, 10
    v.fill(cx - 5, 1, cz - 5, cx + 5, 44, cz + 5, P["wall"])
    v.fill(cx - 4, 1, cz - 4, cx + 4, 44, cz + 4, "air")
    for y in range(34, 42):                                                              # four clock faces
        for x in range(cx - 4, cx + 5):
            d = ((x - cx) ** 2 + (y - 38) ** 2) ** 0.5
            if d <= 4.2:
                blk = "black_concrete" if d > 3.4 else "white_concrete"
                v.set(x, y, cz - 5, blk); v.set(x, y, cz + 5, blk)
                v.set(cx - 5, y, cz - 5 + (x - cx) + 5, blk); v.set(cx + 5, y, cz - 5 + (x - cx) + 5, blk)
    v.fill(cx - 4, 36, cz - 5, cx, 36, cz - 5, "black_concrete")                      # hands
    v.fill(cx, 36, cz - 5, cx, 39, cz - 5, "black_concrete")
    v.fill(cx - 6, 45, cz - 6, cx + 6, 45, cz + 6, P["trim"])
    v.fill(cx - 4, 46, cz - 4, cx + 4, 50, cz + 4, P["wall"])                           # belfry
    v.fill(cx - 3, 46, cz - 3, cx + 3, 50, cz + 3, "air")
    v.windows(cx - 4, 48, cz - 4, cx + 4, cz + 4, "air", period=2, offset=1)
    v.set(cx, 49, cz, "bell")
    v.pyramid(cx, 51, cz, 11, 10, "deepslate_tiles")
    v.set(cx, 61, cz, "gold_block")
    S.arched_bridge(v, 30, 30, 30, 11, P, arches=5, axis="z", deck_y=3)              # Westminster Bridge
    v.fill(30, 4, 30, 30, 5, 60, "iron_bars"); v.fill(40, 4, 30, 40, 5, 60, "iron_bars")


def st_pauls(v: Voxel) -> None:
    """Wren's St Paul's (1710): dome on a colonnaded drum, twin west towers, over the City."""
    S.pad(v, -70, -70, 70, 70, "stone")
    S.basilica(v, 0, -50, P, length=90, width=35, h=22)
    cx, cz = 0, 0
    v.cylinder(cx, 23, cz, 15, 10, P["wall"], hollow=True)
    import math
    for a in range(0, 360, 12):
        v.column(round(cx + 17 * math.cos(math.radians(a))), 23, round(cz + 17 * math.sin(math.radians(a))), 10, "quartz_pillar")
    v.disc(cx, 33, cz, 17, P["trim"])
    v.disc(cx, 23, cz, 14, "air")
    v.cylinder(cx, 34, cz, 13, 3, P["wall"], hollow=True)
    v.dome(cx, 37, cz, 14, "gray_concrete")
    v.cylinder(cx, 52, cz, 3, 6, "white_concrete", hollow=True)
    v.cone(cx, 58, cz, 3, 4, "white_concrete")
    v.set(cx, 62, cz, "gold_block")
    for tx in (-20, 20):
        S.tower(v, tx, -52, 3, 32, P, top="dome", square=True, wall=P["wall"])
    S.city_block(v, -68, 20, P, cols=4, rows=2, lot=9, street=3, floors=(3, 4), roof="hip", seed=80)
    S.city_block(v, 12, 20, P, cols=4, rows=2, lot=9, street=3, floors=(3, 4), roof="hip", seed=81)


def tower_of_london(v: Voxel) -> None:
    """The White Tower (1078) inside its two curtain walls and moat, with Traitors' Gate on the river."""
    S.pad(v, -70, -60, 70, 60, "grass_block")
    v.fill(-70, -3, 40, 70, 0, 60, "water")
    v.fill(-60, -3, -50, 60, 0, 38, "water")
    v.fill(-54, 0, -44, 54, 0, 34, "grass_block")
    S.curtain_wall(v, -52, -42, 52, 32, 7, {**P, "wall": "stone_bricks"}, gate="south", tower_r=4)
    S.curtain_wall(v, -38, -30, 38, 20, 10, {**P, "wall": "stone_bricks"}, gate="south", tower_r=4)
    S.keep(v, 0, -5, 12, 24, {**P, "wall": "white_concrete", "roof": "deepslate_tiles"})
    v.arch(-6, 1, 32, 13, 7, 3, "stone_bricks", axis="x")                              # Traitors' Gate
    v.fill(-5, 0, 34, 5, 0, 40, "water")
    S.house(v, -34, 0, 14, 10, P, floors=2, roof="gable", wall="bricks")                # Queen's House
    for i in range(6):
        v.set(-30 + i * 10, 1, -40, "black_wool")                                      # the ravens


def thames_rail(v: Voxel) -> None:
    """Industrial London: a railway viaduct and steam locomotive, warehouses, Thames barges, a factory chimney."""
    S.pad(v, -80, -50, 80, 60, "stone")
    v.fill(-80, -3, 20, 80, 0, 60, "water")
    S.aqueduct(v, -80, -10, 160, {**P, "wall": "bricks"}, span=8, tiers=1, tier_h=10, thickness=5)
    v.fill(-80, 11, -9, 80, 11, -7, "gravel")
    v.fill(-80, 12, -8, 80, 12, -8, "rail")
    # locomotive and two carriages on the viaduct
    lx, ly, lz = -20, 13, -8
    v.fill(lx, ly, lz - 1, lx + 12, ly + 1, lz + 1, "black_concrete")
    v.fill(lx + 1, ly + 2, lz - 1, lx + 9, ly + 2, lz + 1, "black_concrete")           # boiler
    v.fill(lx + 10, ly + 2, lz - 1, lx + 12, ly + 4, lz + 1, "red_terracotta")            # cab
    v.column(lx + 2, ly + 3, lz, 3, "black_concrete")                                     # funnel
    v.set(lx + 2, ly + 6, lz, "white_wool"); v.set(lx + 1, ly + 7, lz, "white_wool")
    for c in range(2):
        cx0 = lx + 14 + c * 11
        v.fill(cx0, ly, lz - 1, cx0 + 9, ly + 3, lz + 1, "brown_terracotta")
        v.fill(cx0 + 1, ly + 1, lz - 1, cx0 + 8, ly + 2, lz + 1, "air")
        v.windows(cx0, ly + 2, lz - 1, cx0 + 9, lz + 1, "glass_pane", period=2, offset=1)
    # warehouses and a chimney
    for i in range(3):
        S.house(v, -70 + i * 40, 0, 30, 14, P, floors=3, roof="gable", wall="bricks")
    v.cylinder(60, 1, 8, 2, 40, "bricks", hollow=True)
    v.set(60, 41, 8, "campfire")
    for i in range(3):                                                                     # Thames barges
        bx = -60 + i * 40
        v.fill(bx, 0, 30, bx + 16, 0, 34, "dark_oak_planks")
        v.fill(bx + 2, 1, 31, bx + 14, 1, 33, "brown_wool")
        v.column(bx + 8, 1, 32, 10, "stripped_oak_log")
        v.fill(bx + 8, 4, 33, bx + 8, 10, 37, "brown_wool")


def london_streets(v: Voxel) -> None:
    """Terraced brick streets, a gin palace, a market and a Rooks hideout."""
    S.pad(v, -60, -60, 60, 60, "cobblestone")
    S.city_block(v, -58, -58, {**P, "wall": "bricks", "wall2": "light_gray_terracotta"}, cols=4, rows=2, lot=9, street=4, floors=(3, 3), roof="gable", seed=82)
    S.city_block(v, -58, 10, {**P, "wall": "bricks", "wall2": "light_gray_terracotta"}, cols=4, rows=2, lot=9, street=4, floors=(3, 3), roof="gable", seed=83)
    S.house(v, 10, -50, 30, 20, P, floors=2, roof="hip", wall="light_gray_terracotta")     # covered market
    v.fill(11, 1, -49, 39, 8, -31, "air")
    for x in range(14, 38, 6):
        v.fill(x, 1, -46, x + 2, 1, -34, "barrel")
    S.house(v, 10, 10, 20, 14, P, floors=2, roof="flat", wall="bricks")                    # gin palace
    for x in range(12, 30, 3):
        v.set(x, 3, 24, "lantern")
    for x in range(-58, 60, 12):
        v.column(x, 1, 2, 4, "iron_bars"); v.set(x, 5, 2, "lantern")                       # gas lamps


WORLD = World(
    id="london",
    name="Victorian London",
    game="Assassin's Creed Syndicate (2015)",
    era="1868",
    description="The Frye twins' London: Westminster, St Paul's, the Tower, the railway and the East End.",
).build(Build("westminster", "Westminster", "The Palace of Westminster river front, Victoria Tower, the clock tower with Big Ben and Westminster Bridge.", westminster)
).build(Build("st_pauls", "St Paul's Cathedral", "Wren's dome on its colonnaded drum with twin west towers, over City streets.", st_pauls)
).build(Build("tower_of_london", "Tower of London", "The White Tower inside two curtain walls and the moat, with Traitors' Gate on the Thames.", tower_of_london)
).build(Build("thames_rail", "The Thames and the Railway", "A brick railway viaduct with a steam locomotive and carriages, warehouses, chimney and barges.", thames_rail)
).build(Build("london_streets", "East End Streets", "Brick terraces, a covered market, a gin palace and gas lamps.", london_streets))
