"""Run with:  python -m unittest discover -s minecraft/tests  (from the repo root)."""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from acworlds import Voxel, all_worlds  # noqa: E402
from acworlds.export import FILL_LIMIT, mesh, to_commands  # noqa: E402
from acworlds.technology import MODELS  # noqa: E402

CMD = re.compile(r"^(fill|setblock)( ~-?\d*){3}(( ~-?\d*){3})? minecraft:[a-z_]+(\[[a-z_=0-9,]+\])?$")


def _expand(boxes):
    out = {}
    for x1, y1, z1, x2, y2, z2, b in boxes:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    out[(x, y, z)] = b
    return out


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


class BuildTests(unittest.TestCase):
    def test_every_build_generates_valid_commands(self):
        builders = [(w.id, b.id, b.builder) for w in all_worlds() for b in w.builds]
        builders += [("tech", k, fn) for k, fn in MODELS.items()]
        self.assertGreater(len(builders), 80)
        for wid, bid, fn in builders:
            with self.subTest(build=f"{wid}/{bid}"):
                v = Voxel()
                fn(v)
                self.assertGreater(len(v), 100)
                cmds = to_commands(v)
                self.assertLess(len(cmds), 60000, "would exceed maxCommandChainLength")
                for c in cmds:
                    self.assertRegex(c, CMD)

    def test_unique_ids(self):
        ids = [f"{w.id}/{b.id}" for w in all_worlds() for b in w.builds]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len({w.id for w in all_worlds()}), len(all_worlds()))


if __name__ == "__main__":
    unittest.main()
