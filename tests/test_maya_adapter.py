import unittest

from kairo_maya.maya_adapter import _inside, _portable_path, require_maya
from pathlib import Path
from tempfile import TemporaryDirectory


class MayaAdapterTests(unittest.TestCase):
    def test_project_paths_are_portable(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "sourceimages" / "albedo.png"
            self.assertTrue(_inside(root, source))
            self.assertEqual(_portable_path(root, str(source)), "sourceimages/albedo.png")

    def test_host_operation_fails_explicitly_without_maya(self):
        with self.assertRaisesRegex(RuntimeError, "require Maya"):
            require_maya()
