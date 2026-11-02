"""Run with:  python3 -m unittest minecraft.rcon_bridge.test_bridge  (from the repo root)."""

import os
import sys
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import server  # noqa: E402


class FakeClient:
    """Stands in for mctools.RCONClient: records commands, answers with canned text."""

    def __init__(self, *a, **k):
        self.sent = []

    def login(self, pw):
        return pw == "pw"

    def command(self, cmd):
        self.sent.append(cmd)
        if cmd == "list":
            return "§aThere are 1 of a max of 5 players online: wari"
        if cmd.startswith("execute if block"):
            return "Test passed"
        return ""


class BridgeTests(unittest.TestCase):
    def setUp(self):
        server._rcon = server.Rcon("127.0.0.1", 25575, "pw")
        self.fake = FakeClient()
        patcher = mock.patch.object(server.Rcon, "_connect", return_value=self.fake)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_colour_codes_are_stripped_and_slash_dropped(self):
        self.assertEqual(server.run_command("/list"), "There are 1 of a max of 5 players online: wari")
        self.assertEqual(self.fake.sent, ["list"])

    def test_silent_commands_say_so(self):
        self.assertEqual(server.run_command("fill 0 0 0 1 1 1 stone"), "(no output)")

    def test_probe_block(self):
        self.assertTrue(server.probe_block(1, 2, 3, "stone").startswith("yes"))
        self.assertEqual(self.fake.sent[-1], "execute if block 1 2 3 minecraft:stone")

    def test_place_build_forceloads_then_runs_then_releases(self):
        with mock.patch.object(server.time, "sleep"):
            server.place_build("ac:egypt/giza", 10, -60, 20)
        adds = [c for c in self.fake.sent if c.startswith("forceload add")]
        removes = [c for c in self.fake.sent if c.startswith("forceload remove")]
        self.assertEqual(len(adds), 4)
        self.assertEqual(len(removes), 4)
        self.assertIn("execute positioned 10 -60 20 run function ac:raw/egypt/giza", self.fake.sent)
        self.assertLess(self.fake.sent.index(adds[-1]), self.fake.sent.index("execute positioned 10 -60 20 run function ac:raw/egypt/giza"))

    def test_oversized_command_is_refused(self):
        with self.assertRaises(ValueError):
            server.run_command("say " + "x" * 2000)

    def test_env_file_parsing(self):
        with mock.patch.object(server, "ENV_FILE") as env:
            env.exists.return_value = True
            env.read_text.return_value = "# comment\nRCON_PASSWORD = secret\nRCON_PORT=25580\n"
            with mock.patch.dict(os.environ, {}, clear=False):
                os.environ.pop("RCON_PASSWORD", None)
                cfg = server.load_env()
        self.assertEqual(cfg["RCON_PASSWORD"], "secret")
        self.assertEqual(cfg["RCON_PORT"], "25580")


if __name__ == "__main__":
    unittest.main()
