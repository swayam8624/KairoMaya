"""Host-neutral Maya scene validation rules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kairo_pipeline.diagnostics import Diagnostic, DiagnosticBag, DiagnosticLocation, Severity


@dataclass(frozen=True, slots=True)
class ReferenceSnapshot:
    node: str
    path: str
    namespace: str
    loaded: bool
    exists: bool
    inside_project: bool


@dataclass(frozen=True, slots=True)
class TransformSnapshot:
    name: str
    translation: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class MeshSnapshot:
    name: str
    vertices: int
    uv_sets: int
    assigned_materials: int
    nonmanifold_edges: int = 0
    lamina_faces: int = 0


@dataclass(frozen=True, slots=True)
class TextureSnapshot:
    node: str
    path: str
    exists: bool
    inside_project: bool
    color_space: str


@dataclass(frozen=True, slots=True)
class SceneSnapshot:
    scene_path: str
    saved: bool
    linear_unit: str
    time_unit: str
    first_frame: float
    last_frame: float
    unknown_plugins: tuple[str, ...] = ()
    references: tuple[ReferenceSnapshot, ...] = ()
    transforms: tuple[TransformSnapshot, ...] = ()
    meshes: tuple[MeshSnapshot, ...] = ()
    textures: tuple[TextureSnapshot, ...] = ()


@dataclass(frozen=True, slots=True)
class SceneProfile:
    linear_unit: str = "cm"
    time_unit: str = "film"
    first_frame: float = 1001.0
    last_frame: float = 1100.0
    required_texture_color_spaces: tuple[str, ...] = ()
    require_frozen_root_transforms: bool = True

    def __post_init__(self) -> None:
        if self.first_frame > self.last_frame:
            raise ValueError("profile first frame must not exceed last frame")


def validate_scene(snapshot: SceneSnapshot, profile: SceneProfile) -> DiagnosticBag:
    bag = DiagnosticBag()
    if not snapshot.saved:
        _add(bag, "MAYA_SCENE_UNSAVED", Severity.ERROR, "Scene has not been saved.",
             "Save it inside the project before publishing.")
    if snapshot.linear_unit != profile.linear_unit:
        _add(bag, "MAYA_LINEAR_UNIT", Severity.ERROR,
             f"Linear unit is {snapshot.linear_unit}, expected {profile.linear_unit}.",
             "Change units with conversion enabled and review scale.")
    if snapshot.time_unit != profile.time_unit:
        _add(bag, "MAYA_TIME_UNIT", Severity.ERROR,
             f"Time unit is {snapshot.time_unit}, expected {profile.time_unit}.",
             "Set the show frame rate before animation or caching.")
    if (snapshot.first_frame, snapshot.last_frame) != (profile.first_frame, profile.last_frame):
        _add(bag, "MAYA_TIMELINE_RANGE", Severity.ERROR,
             "Playback range does not match the project profile.",
             "Apply the approved shot frame range.")
    for plugin in snapshot.unknown_plugins:
        _add(bag, "MAYA_UNKNOWN_PLUGIN", Severity.WARNING,
             f"Unknown plugin metadata remains: {plugin}.",
             "Confirm it is safe, then remove unknown plugin data.", plugin)
    _validate_references(snapshot.references, bag)
    _validate_transforms(snapshot.transforms, profile, bag)
    _validate_meshes(snapshot.meshes, bag)
    _validate_textures(snapshot.textures, profile, bag)
    return bag


def _validate_references(references: tuple[ReferenceSnapshot, ...], bag: DiagnosticBag) -> None:
    namespaces: set[str] = set()
    for ref in references:
        if not ref.exists:
            _add(bag, "MAYA_REFERENCE_MISSING", Severity.ERROR,
                 f"Reference file is missing: {ref.path}", "Restore or repath the reference.", ref.node, "file")
        if not ref.loaded:
            _add(bag, "MAYA_REFERENCE_UNLOADED", Severity.WARNING,
                 "Reference is unloaded.", "Load it for final validation.", ref.node)
        if not ref.inside_project:
            _add(bag, "MAYA_REFERENCE_EXTERNAL", Severity.ERROR,
                 f"Reference is outside the project: {ref.path}",
                 "Publish and reference a project-relative asset.", ref.node, "file")
        if not ref.namespace or ref.namespace in {":", "UI", "shared"}:
            _add(bag, "MAYA_NAMESPACE_INVALID", Severity.ERROR,
                 "Reference namespace is empty or reserved.", "Assign a unique asset namespace.", ref.node)
        elif ref.namespace in namespaces:
            _add(bag, "MAYA_NAMESPACE_DUPLICATE", Severity.ERROR,
                 f"Reference namespace is duplicated: {ref.namespace}",
                 "Assign a unique namespace per reference.", ref.node)
        namespaces.add(ref.namespace)


def _validate_transforms(transforms: tuple[TransformSnapshot, ...], profile: SceneProfile, bag: DiagnosticBag) -> None:
    if not profile.require_frozen_root_transforms:
        return
    for transform in transforms:
        if any(abs(value) > 1e-6 for value in (*transform.translation, *transform.rotation)) or any(
            abs(value - 1.0) > 1e-6 for value in transform.scale
        ):
            _add(bag, "MAYA_ROOT_TRANSFORM_DIRTY", Severity.WARNING,
                 "Export root has non-identity transforms.",
                 "Review pivots, then freeze transforms when production-safe.", transform.name)
        if any(value <= 0.0 for value in transform.scale):
            _add(bag, "MAYA_ROOT_SCALE_NONPOSITIVE", Severity.ERROR,
                 "Export root has zero or negative scale.",
                 "Remove mirrored or degenerate scale before export.", transform.name, "scale")


def _validate_meshes(meshes: tuple[MeshSnapshot, ...], bag: DiagnosticBag) -> None:
    for mesh in meshes:
        if mesh.vertices == 0:
            _add(bag, "MAYA_MESH_EMPTY", Severity.ERROR, "Mesh has no vertices.", "Remove or rebuild it.", mesh.name)
        if mesh.uv_sets == 0:
            _add(bag, "MAYA_MESH_UVS_MISSING", Severity.ERROR, "Mesh has no UV set.", "Create production UVs.", mesh.name)
        if mesh.assigned_materials == 0:
            _add(bag, "MAYA_MESH_MATERIAL_MISSING", Severity.ERROR, "Mesh has no assigned material.", "Assign an approved material.", mesh.name)
        if mesh.nonmanifold_edges:
            _add(bag, "MAYA_MESH_NONMANIFOLD", Severity.ERROR,
                 f"Mesh has {mesh.nonmanifold_edges} nonmanifold edge(s).", "Repair topology.", mesh.name)
        if mesh.lamina_faces:
            _add(bag, "MAYA_MESH_LAMINA", Severity.ERROR,
                 f"Mesh has {mesh.lamina_faces} lamina face(s).", "Remove overlapping faces.", mesh.name)


def _validate_textures(textures: tuple[TextureSnapshot, ...], profile: SceneProfile, bag: DiagnosticBag) -> None:
    for texture in textures:
        if not texture.exists:
            _add(bag, "MAYA_TEXTURE_MISSING", Severity.ERROR,
                 f"Texture is missing: {texture.path}", "Restore or repath it.", texture.node, "fileTextureName")
        if not texture.inside_project:
            _add(bag, "MAYA_TEXTURE_EXTERNAL", Severity.ERROR,
                 f"Texture is outside the project: {texture.path}",
                 "Publish it into the project texture library.", texture.node, "fileTextureName")
        if profile.required_texture_color_spaces and texture.color_space not in profile.required_texture_color_spaces:
            _add(bag, "MAYA_TEXTURE_COLORSPACE", Severity.ERROR,
                 f"Texture colorspace '{texture.color_space}' is not approved.",
                 "Choose a colorspace from the project profile.", texture.node, "colorSpace")


def _add(bag: DiagnosticBag, code: str, severity: Severity, message: str,
         suggestion: str, object_path: str = "scene", property_name: str = "") -> None:
    bag.add(Diagnostic(code=code, severity=severity, message=message,
                       location=DiagnosticLocation(host="maya", object_path=object_path,
                                                   property_name=property_name),
                       suggestion=suggestion))
