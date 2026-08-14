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

__version__ = "0.1.0"

__all__ = [
    "MeshSnapshot", "ReferenceSnapshot", "SceneProfile", "SceneSnapshot",
    "TextureSnapshot", "TransformSnapshot", "validate_scene", "__version__",
    "inspect_scene", "install_menu", "select_location", "show_panel",
]
