import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "codex-remote-hub.py"


def load_hub():
    spec = importlib.util.spec_from_file_location("codex_remote_hub_test", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ServerHelperTests(unittest.TestCase):
    def setUp(self):
        self.hub = load_hub()
        self.hub._port_assignments.clear()

    def test_normalize_session_name(self):
        self.assertEqual(self.hub.normalize_session_name(" My Project!! "), "my-project")
        self.assertEqual(self.hub.normalize_session_name("A_B.c-1"), "a_b.c-1")
        with self.assertRaises(ValueError):
            self.hub.normalize_session_name("!!!")

    def test_validate_session_name_rejects_unsafe_values(self):
        self.assertEqual(self.hub.validate_session_name("safe-name_1"), "safe-name_1")
        for value in ("../bad", "bad/slash", "", "-starts-with-dash", "x" * 65):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.hub.validate_session_name(value)

    def test_resolve_project_directory_stays_inside_dev_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp) / "Projects"
            child = base / "app"
            sibling = pathlib.Path(tmp) / "Projects2"
            child.mkdir(parents=True)
            sibling.mkdir()

            self.hub.DEV_ROOT = str(base)

            self.assertEqual(self.hub.resolve_project_directory(str(child)), str(child.resolve()))
            with self.assertRaises(ValueError):
                self.hub.resolve_project_directory(str(sibling))

    def test_get_folders_resets_traversal_to_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp) / "Projects"
            child = base / "app"
            outside = pathlib.Path(tmp) / "outside"
            child.mkdir(parents=True)
            outside.mkdir()

            self.hub.DEV_ROOT = str(base)
            data = self.hub.get_folders("../outside")

            self.assertEqual(data["absolute"], str(base.resolve()))
            self.assertEqual(data["folders"], ["app"])

    def test_port_for_name_resolves_hash_collisions(self):
        buckets = {}
        pair = None
        for i in range(5000):
            name = f"s{i}"
            preferred = self.hub.BASE_PORT + (
                int(self.hub.hashlib.md5(name.encode()).hexdigest(), 16) % self.hub.PORT_COUNT
            )
            if preferred in buckets:
                pair = (buckets[preferred], name)
                break
            buckets[preferred] = name

        self.assertIsNotNone(pair)
        first, second = pair
        self.assertNotEqual(self.hub.port_for_name(first), self.hub.port_for_name(second))

    def test_rendering_escapes_session_values(self):
        self.hub.get_sessions = lambda: [{
            "name": "bad\"><script",
            "port": 7800,
            "time": "10:00",
            "attached": False,
            "has_ttyd": False,
        }]

        rendered = self.hub.render_hub("localhost")

        self.assertNotIn('bad"><script', rendered)
        self.assertIn("bad&quot;&gt;&lt;script", rendered)

    def test_terminal_uses_http_without_certificates(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hub.INSTALL_DIR = tmp
            rendered = self.hub.render_terminal("safe", 7800, "example.test:7690")

        self.assertIn('"http://example.test:7800"', rendered)
        self.assertIn("<title>safe", rendered)


if __name__ == "__main__":
    unittest.main()
