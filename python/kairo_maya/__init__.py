# SOURCE STUDY NOTE:
# Package surface separating host Maya API access from pure SceneSnapshot/SceneProfile validation.
# See docs/SOURCE_READING_ORDER.md for host → preflight → publish flow.

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
