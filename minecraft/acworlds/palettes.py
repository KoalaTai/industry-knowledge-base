"""Block palettes, one per architectural tradition.

A palette is a plain dict so builders can do ``p["wall"]``.  Keys:
ground, wall, wall2 (accent), trim, roof, floor, column, light, window,
water, path.
"""

from __future__ import annotations

from typing import Dict

Palette = Dict[str, str]


def _p(**kw: str) -> Palette:
    base = dict(
        ground="stone", wall="stone_bricks", wall2="cobblestone", trim="smooth_stone",
        roof="dark_oak_planks", floor="smooth_stone", column="stone_bricks",
        light="lantern", window="glass_pane", water="water", path="gravel",
        leaves="oak_leaves[persistent=true]", log="oak_log",
    )
    base.update(kw)
    return base


EGYPT = _p(ground="sand", wall="sandstone", wall2="smooth_sandstone", trim="chiseled_sandstone",
           roof="sandstone_slab", floor="cut_sandstone", column="sandstone", path="sand",
           leaves="jungle_leaves[persistent=true]", log="jungle_log")
PYRAMID_CASING = "smooth_sandstone"
PYRAMID_CORE = "sandstone"

LEVANT = _p(ground="terracotta", wall="sandstone", wall2="smooth_sandstone", trim="cut_sandstone",
            roof="sandstone", floor="smooth_sandstone", column="smooth_sandstone", path="dirt_path")
CRUSADER = _p(ground="stone", wall="stone_bricks", wall2="mossy_stone_bricks", trim="stone_brick_slab",
              roof="cobblestone", floor="stone", column="stone_bricks", path="cobblestone")
TUSCANY = _p(ground="grass_block", wall="smooth_sandstone", wall2="white_terracotta", trim="smooth_quartz",
             roof="terracotta", floor="polished_andesite", column="smooth_quartz", path="cobblestone",
             window="glass_pane", leaves="dark_oak_leaves[persistent=true]", log="dark_oak_log")
VENICE = _p(ground="stone", wall="white_terracotta", wall2="pink_terracotta", trim="quartz_block",
            roof="terracotta", floor="polished_diorite", column="quartz_pillar", path="stone_bricks")
ROME = _p(ground="grass_block", wall="smooth_stone", wall2="stone_bricks", trim="quartz_block",
          roof="terracotta", floor="polished_andesite", column="quartz_pillar", path="cobblestone")
OTTOMAN = _p(ground="grass_block", wall="light_gray_terracotta", wall2="stone_bricks", trim="quartz_block",
             roof="light_blue_terracotta", floor="polished_diorite", column="quartz_pillar", path="stone_bricks")
COLONIAL = _p(ground="grass_block", wall="bricks", wall2="white_concrete", trim="smooth_stone",
              roof="dark_oak_planks", floor="oak_planks", column="white_concrete", path="cobblestone",
              leaves="spruce_leaves[persistent=true]", log="spruce_log")
CARIBBEAN = _p(ground="sand", wall="smooth_sandstone", wall2="white_terracotta", trim="cut_sandstone",
               roof="orange_terracotta", floor="oak_planks", column="smooth_sandstone", path="sand",
               leaves="jungle_leaves[persistent=true]", log="jungle_log")
PARIS = _p(ground="stone", wall="polished_diorite", wall2="light_gray_concrete", trim="smooth_quartz",
           roof="deepslate_tiles", floor="polished_andesite", column="quartz_pillar", path="cobblestone")
LONDON = _p(ground="stone", wall="light_gray_terracotta", wall2="bricks", trim="smooth_quartz",
            roof="deepslate_tiles", floor="smooth_stone", column="quartz_pillar", path="cobblestone")
GREECE = _p(ground="grass_block", wall="quartz_block", wall2="smooth_quartz", trim="chiseled_quartz_block",
            roof="terracotta", floor="smooth_quartz", column="quartz_pillar", path="cobblestone",
            leaves="dark_oak_leaves[persistent=true]", log="dark_oak_log")
VIKING = _p(ground="grass_block", wall="spruce_planks", wall2="spruce_log", trim="stripped_spruce_log",
            roof="dark_oak_planks", floor="spruce_planks", column="spruce_log", path="dirt_path",
            leaves="spruce_leaves[persistent=true]", log="spruce_log")
SAXON = _p(ground="grass_block", wall="cobblestone", wall2="mossy_cobblestone", trim="stone_bricks",
           roof="hay_block", floor="stone", column="cobblestone", path="dirt_path")
ABBASID = _p(ground="sand", wall="mud_bricks", wall2="packed_mud", trim="cut_sandstone",
             roof="light_blue_terracotta", floor="smooth_sandstone", column="smooth_sandstone", path="sand",
             leaves="jungle_leaves[persistent=true]", log="jungle_log")
JAPAN = _p(ground="grass_block", wall="white_concrete", wall2="dark_oak_planks", trim="dark_oak_log",
           roof="deepslate_tiles", floor="dark_oak_planks", column="dark_oak_log", path="gravel",
           leaves="cherry_leaves[persistent=true]", log="cherry_log")
CHINA = _p(ground="grass_block", wall="stone_bricks", wall2="gray_terracotta", trim="smooth_stone",
           roof="gray_terracotta", floor="smooth_stone", column="red_terracotta", path="stone_bricks")
INDIA = _p(ground="grass_block", wall="red_sandstone", wall2="smooth_red_sandstone", trim="cut_red_sandstone",
           roof="white_concrete", floor="polished_diorite", column="smooth_red_sandstone", path="red_sand")
RUSSIA = _p(ground="snow_block", wall="bricks", wall2="red_terracotta", trim="white_concrete",
            roof="lime_terracotta", floor="smooth_stone", column="white_concrete", path="stone_bricks")
GERMAN = _p(ground="grass_block", wall="white_concrete", wall2="dark_oak_planks", trim="dark_oak_log",
            roof="red_terracotta", floor="oak_planks", column="dark_oak_log", path="cobblestone")
MESOPOTAMIA = _p(ground="terracotta", wall="mud_bricks", wall2="packed_mud", trim="blue_terracotta",
                 roof="mud_bricks", floor="packed_mud", column="mud_bricks", path="terracotta")
INCA = _p(ground="grass_block", wall="polished_andesite", wall2="andesite", trim="smooth_stone",
          roof="hay_block", floor="andesite", column="polished_andesite", path="andesite")
