from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from kairo_maya.publisher import publish_scene
from kairo_maya.scenedoctor import *
from kairo_pipeline.manifest import load_manifest


class MayaPublisherTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for directory in ("scenes", "assets", "sourceimages"):
            (self.root / directory).mkdir()
        (self.root / "scenes" / "hero.ma").write_bytes(b"maya scene")
        (self.root / "assets" / "rig.ma").write_bytes(b"rig")
        (self.root / "sourceimages" / "albedo.png").write_bytes(b"png")
        self.profile = SceneProfile(required_texture_color_spaces=("sRGB",))
        self.scene = SceneSnapshot(
            "scenes/hero.ma", True, "cm", "film", 1001, 1100,
            references=(ReferenceSnapshot("rigRN", "assets/rig.ma", "heroRig", True, True, True),),
            transforms=(TransformSnapshot("hero_GRP", (0,0,0), (0,0,0), (1,1,1)),),
            meshes=(MeshSnapshot("heroShape", 8, 1, 1),),
            textures=(TextureSnapshot("file1", "sourceimages/albedo.png", True, True, "sRGB"),),
        )

    def tearDown(self): self.temporary.cleanup()

    def test_dry_run_then_publish_scene_package(self):
        dry = publish_scene(self.root, self.scene, self.profile,
                            project_name="Demo", asset_name="hero", version=1, dry_run=True)
        self.assertTrue(dry.dry_run)
        self.assertFalse((self.root / "Published").exists())
        result = publish_scene(self.root, self.scene, self.profile,
                               project_name="Demo", asset_name="hero", version=1)
        self.assertEqual(result.files, 3)
        manifest = load_manifest(result.target / "publish.kairo.json")
        self.assertEqual(manifest.source_host, "maya")
        self.assertEqual({item.role for item in manifest.dependencies}, {"reference", "texture"})

    def test_broken_scene_cannot_publish(self):
        broken = SceneSnapshot("", False, "m", "film", 1001, 1100)
        with self.assertRaisesRegex(ValueError, "MAYA_SCENE_UNSAVED"):
            publish_scene(self.root, broken, self.profile,
                          project_name="Demo", asset_name="hero", version=1)
