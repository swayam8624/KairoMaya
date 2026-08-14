import unittest

from kairo_maya.scenedoctor import *


class SceneDoctorTests(unittest.TestCase):
    def profile(self):
        return SceneProfile(required_texture_color_spaces=("Raw", "sRGB"))

    def valid(self):
        return SceneSnapshot(
            "scenes/asset.ma", True, "cm", "film", 1001, 1100,
            references=(ReferenceSnapshot("refRN", "assets/rig.ma", "hero", True, True, True),),
            transforms=(TransformSnapshot("hero_GRP", (0,0,0), (0,0,0), (1,1,1)),),
            meshes=(MeshSnapshot("heroShape", 100, 1, 1),),
            textures=(TextureSnapshot("file1", "sourceimages/albedo.png", True, True, "sRGB"),),
        )

    def codes(self, scene):
        return {item.code for item in validate_scene(scene, self.profile())}

    def test_valid_scene_passes(self):
        self.assertEqual(self.codes(self.valid()), set())

    def test_scene_profile_errors_block(self):
        scene = SceneSnapshot("", False, "m", "ntsc", 1, 24, ("oldPlugin",))
        self.assertEqual(self.codes(scene), {
            "MAYA_SCENE_UNSAVED", "MAYA_LINEAR_UNIT", "MAYA_TIME_UNIT",
            "MAYA_TIMELINE_RANGE", "MAYA_UNKNOWN_PLUGIN",
        })

    def test_reference_contracts(self):
        scene = self.valid()
        broken = ReferenceSnapshot("badRN", "/tmp/missing.ma", "hero", False, False, False)
        changed = SceneSnapshot(scene.scene_path, True, "cm", "film", 1001, 1100,
                                references=scene.references + (broken,))
        self.assertEqual(self.codes(changed), {
            "MAYA_REFERENCE_MISSING", "MAYA_REFERENCE_UNLOADED",
            "MAYA_REFERENCE_EXTERNAL", "MAYA_NAMESPACE_DUPLICATE",
        })

    def test_mesh_transform_and_texture_contracts(self):
        scene = SceneSnapshot(
            "scenes/asset.ma", True, "cm", "film", 1001, 1100,
            transforms=(TransformSnapshot("root", (1,0,0), (0,0,0), (-1,1,1)),),
            meshes=(MeshSnapshot("badShape", 0, 0, 0, 2, 1),),
            textures=(TextureSnapshot("file1", "/tmp/a.png", False, False, "Utility - Raw"),),
        )
        self.assertEqual(self.codes(scene), {
            "MAYA_ROOT_TRANSFORM_DIRTY", "MAYA_ROOT_SCALE_NONPOSITIVE", "MAYA_MESH_EMPTY",
            "MAYA_MESH_UVS_MISSING", "MAYA_MESH_MATERIAL_MISSING", "MAYA_MESH_NONMANIFOLD",
            "MAYA_MESH_LAMINA", "MAYA_TEXTURE_MISSING", "MAYA_TEXTURE_EXTERNAL",
            "MAYA_TEXTURE_COLORSPACE",
        })
