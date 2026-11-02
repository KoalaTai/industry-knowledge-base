"""Run with:  python -m unittest discover -s minecraft/tests  (from the repo root)."""

import json
import os
import re
import sys
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from acworlds import Voxel, all_worlds  # noqa: E402
from acworlds.export import FILL_LIMIT, mesh, to_commands  # noqa: E402
from acworlds.structure import (TILE, blocks_from_template, build_plan, dumps, loads,  # noqa: E402
                                parse_state, template_nbt)
from acworlds.technology import MODELS  # noqa: E402

CMD = re.compile(r"^(fill|setblock)( ~-?\d*){3}(( ~-?\d*){3})? minecraft:[a-z_]+(\[[a-z_=0-9,]+\])?$")
PLACE = re.compile(r"^place template ac:[a-z_0-9/]+/[sl]\d+_\d+_\d+( ~-?\d*){3}$")
FILL = re.compile(r"^fill ~(-?\d*) ~(-?\d*) ~(-?\d*) ~(-?\d*) ~(-?\d*) ~(-?\d*) (minecraft:\S+)$")


def _expand(boxes):
    out = {}
    for x1, y1, z1, x2, y2, z2, b in boxes:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    out[(x, y, z)] = b
    return out


def _rel(s):
    return int(s) if s else 0


def _expand_plan(plan):
    """Apply a Plan on an empty canvas and return the resulting blocks."""
    out = {}
    for cmd in plan.fills + plan.late_fills:
        m = FILL.match(cmd)
        assert m, cmd
        x1, y1, z1, x2, y2, z2 = (_rel(g) for g in m.groups()[:6])
        out.update(_expand([(x1, y1, z1, x2, y2, z2, m.group(7))]))
    for t in plan.templates:
        nbt = loads(dumps(t.nbt))           # byte-level round trip
        out.update(blocks_from_template(nbt, t.origin))
    return out


def _sample():
    v = Voxel()
    v.fill(-10, 0, -10, 60, 3, 60, "stone")       # big slab -> stays /fill
    v.fill(2, 1, 2, 8, 2, 8, "air")               # carved room
    v.dome(5, 4, 5, 4, "sandstone")
    v.set(5, 20, 5, "gold_block")
    v.set(3, 4, 3, "wall_torch[facing=north]")    # needs support -> late template
    v.tree(50, 4, 50)                             # leaves carry [persistent=true]
    return v


class MeshTests(unittest.TestCase):
    def test_mesh_round_trips_exactly(self):
        v = Voxel()
        v.fill(0, 0, 0, 10, 3, 10, "stone")
        v.fill(2, 1, 2, 8, 2, 8, "air")
        v.dome(5, 4, 5, 4, "sandstone")
        v.set(5, 20, 5, "gold_block")
        boxes = mesh(v)
        self.assertEqual(_expand(boxes), v.blocks)
        self.assertLess(len(boxes), len(v.blocks) // 4)

    def test_air_is_emitted_last(self):
        v = Voxel()
        v.fill(0, 0, 0, 4, 4, 4, "stone")
        v.carve(1, 1, 1, 3, 3, 3)
        cmds = to_commands(v)
        self.assertTrue(cmds[-1].endswith("minecraft:air"))

    def test_large_boxes_are_split(self):
        v = Voxel()
        v.fill(0, 0, 0, 199, 0, 199, "sand")        # 40,000 > 32,768
        for x1, y1, z1, x2, y2, z2, _ in mesh(v):
            self.assertLessEqual((x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1), FILL_LIMIT)


class TemplateTests(unittest.TestCase):
    def test_nbt_round_trip(self):
        nbt = {"DataVersion": 5023, "size": [1, 2, 3], "palette": [{"Name": "minecraft:stone"},
               {"Name": "minecraft:oak_leaves", "Properties": {"persistent": "true"}}],
               "blocks": [{"pos": [0, 1, 2], "state": 1}], "entities": []}
        self.assertEqual(loads(dumps(nbt)), nbt)

    def test_parse_state(self):
        self.assertEqual(parse_state("minecraft:stone"), ("minecraft:stone", {}))
        self.assertEqual(parse_state("minecraft:wall_torch[facing=north,lit=true]"),
                         ("minecraft:wall_torch", {"facing": "north", "lit": "true"}))

    def test_plan_reproduces_voxel_exactly(self):
        v = _sample()
        self.assertEqual(_expand_plan(build_plan(v)), v.blocks)
        self.assertEqual(_expand_plan(build_plan(v, fill_threshold=10 ** 9)), v.blocks)   # templates only

    def test_tiles_respect_the_48_block_cap(self):
        v = Voxel()
        v.fill(-70, 0, -70, 130, 60, 130, "stone", hollow=True)   # 201 x 61 x 201 shell
        plan = build_plan(v, fill_threshold=10 ** 9)
        self.assertEqual(len(plan.templates), 5 * 2 * 5)      # ceil(201/48) x ceil(61/48) x ceil(201/48)
        for t in plan.templates:
            self.assertLessEqual(max(t.nbt["size"]), TILE)
            for e in t.nbt["blocks"]:
                self.assertTrue(all(0 <= p < TILE for p in e["pos"]), e)
        with self.assertRaises(ValueError):
            template_nbt({(0, 0, 0): "minecraft:stone", (TILE, 0, 0): "minecraft:stone"}, (0, 0, 0))

    def test_late_blocks_are_placed_after_solids(self):
        plan = build_plan(_sample())
        kinds = [t.name[0] for t in plan.templates]
        self.assertIn("l", kinds)
        cmds = plan.commands("ac:test/sample")
        first_late = next(i for i, c in enumerate(cmds) if "/l" in c)
        self.assertTrue(all("/s" in c or c.startswith("fill") for c in cmds[:first_late]))
        for c in cmds:
            self.assertTrue(PLACE.match(c) or CMD.match(c), c)


class BuildTests(unittest.TestCase):
    def _builders(self):
        builders = [(w.id, b.id, b.builder) for w in all_worlds() for b in w.builds]
        builders += [("tech", k, fn) for k, fn in MODELS.items()]
        self.assertGreater(len(builders), 80)
        return builders

    def test_every_build_generates_valid_commands(self):
        for wid, bid, fn in self._builders():
            with self.subTest(build=f"{wid}/{bid}"):
                v = Voxel()
                fn(v)
                self.assertGreater(len(v), 100)
                cmds = to_commands(v)
                self.assertLess(len(cmds), 60000, "would exceed max_command_sequence_length")
                for c in cmds:
                    self.assertRegex(c, CMD)

    def test_template_plans_are_small_and_valid(self):
        total = 0
        for wid, bid, fn in self._builders():
            with self.subTest(build=f"{wid}/{bid}"):
                v = Voxel()
                fn(v)
                plan = build_plan(v)
                n = plan.command_count
                total += n
                self.assertLess(n, len(to_commands(v)) + 1)
                for c in plan.commands(f"ac:{wid}/{bid}"):
                    self.assertTrue(PLACE.match(c) or CMD.match(c), c)
                for t in plan.templates:
                    self.assertLessEqual(max(t.nbt["size"]), TILE)
        self.assertLess(total, 6000, "the whole pack should need only a few thousand placement commands")

    def test_unique_ids(self):
        ids = [f"{w.id}/{b.id}" for w in all_worlds() for b in w.builds]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len({w.id for w in all_worlds()}), len(all_worlds()))


class PackagingTests(unittest.TestCase):
    """The shipped zip must be loadable by Minecraft as-is."""

    ZIP = os.path.join(os.path.dirname(HERE), "datapack", "ac_worlds.zip")

    def test_zip_has_pack_mcmeta_at_root(self):
        # Minecraft silently ignores a zip whose pack.mcmeta is inside a subfolder.
        with zipfile.ZipFile(self.ZIP) as zf:
            names = zf.namelist()
            self.assertIn("pack.mcmeta", names)
            self.assertIn("data/minecraft/tags/function/load.json", names)
            self.assertIn("data/minecraft/tags/function/tick.json", names)
            self.assertIn("data/ac/function/load.mcfunction", names)
            self.assertFalse(any(n.startswith("ac_worlds/") for n in names))
            meta = json.loads(zf.read("pack.mcmeta"))
            self.assertGreaterEqual(meta["pack"]["pack_format"], 48)
            self.assertEqual(meta["pack"]["min_format"], 48)         # 1.21.9+ / 26.x field
            self.assertIn("max_format", meta["pack"])

    def test_zip_ships_structure_templates(self):
        with zipfile.ZipFile(self.ZIP) as zf:
            names = zf.namelist()
            nbts = [n for n in names if n.startswith("data/ac/structure/") and n.endswith(".nbt")]
            self.assertGreater(len(nbts), 100)
            raw = zf.read("data/ac/function/raw/egypt/giza.mcfunction").decode().splitlines()
            places = [c for c in raw if c.startswith("place template ac:egypt/giza/")]
            self.assertTrue(places)
            for c in places:
                tid = c.split()[2].split(":", 1)[1]
                self.assertIn(f"data/ac/structure/{tid}.nbt", names)
            self.assertNotIn("gamerule", zf.read("data/ac/function/load.mcfunction").decode())

    def test_zip_ships_travel_functions(self):
        with zipfile.ZipFile(self.ZIP) as zf:
            names = zf.namelist()
            for fn in ("fly", "spirit", "overview", "_overview", "goto/egypt", "_goto/egypt", "goto/tech"):
                self.assertIn(f"data/ac/function/{fn}.mcfunction", names)
            self.assertIn("gamemode spectator @s", zf.read("data/ac/function/spirit.mcfunction").decode())
            goto = zf.read("data/ac/function/_goto/egypt.mcfunction").decode().splitlines()[0]
            self.assertRegex(goto, r"^\$execute positioned \$\(x\) \$\(y\) \$\(z\) run tp @s ~-?\d* ~-?\d* ~-?\d* -?\d+ -?\d+$")
            hub = zf.read("data/ac/function/hub.mcfunction").decode()
            self.assertIn("data modify storage ac:hub x set from storage ac:seq x", hub)
            # goto/overview adopt a running hub's origin; the guard must be on the key copied last
            entry = zf.read("data/ac/function/goto/egypt.mcfunction").decode().splitlines()
            adopt = [c for c in entry if "set from storage ac:seq" in c]
            self.assertEqual(len(adopt), 3)
            self.assertTrue(all(c.startswith("execute unless data storage ac:hub z ") for c in adopt), adopt)
            self.assertTrue(adopt[-1].endswith("ac:hub z set from storage ac:seq z"))


if __name__ == "__main__":
    unittest.main()
