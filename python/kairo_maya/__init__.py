# TEACHING MAP — python/kairo_maya/__init__.py
# Package API for portable scene diagnostics and publishing. Native Maya API access belongs
# to maya_adapter.py, keeping SceneDoctor logic independently testable.
# Follow READING_ORDER.md for native-host and portable publish API boundaries.

"""Kairo Maya SceneDoctor public API."""

from .scenedoctor import (
    MeshSnapshot,
    ReferenceSnapshot,
    SceneProfile,
    SceneSnapshot,
    TextureSnapshot,
    TransformSnapshot,
    validate_scene,
)
from .maya_adapter import inspect_scene, install_menu, select_location, show_panel
from .publisher import ScenePublishResult, publish_scene

__version__ = "0.1.0"

__all__ = [
    "MeshSnapshot", "ReferenceSnapshot", "SceneProfile", "SceneSnapshot",
    "TextureSnapshot", "TransformSnapshot", "validate_scene", "__version__",
    "inspect_scene", "install_menu", "select_location", "show_panel",
    "ScenePublishResult", "publish_scene",
]
