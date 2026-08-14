"""Validated immutable Maya scene publication."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kairo_pipeline.fingerprint import fingerprint_file
from kairo_pipeline.manifest import PublishFile, PublishKind, PublishManifest
from kairo_pipeline.paths import resolve_project_path
from kairo_pipeline.publish import plan_publish, publish_bundle

from .scenedoctor import SceneProfile, SceneSnapshot, validate_scene


@dataclass(frozen=True, slots=True)
class ScenePublishResult:
    target: Path
    files: int
    bytes: int
    manifest_sha256: str
    dry_run: bool


def publish_scene(project_root: Path, snapshot: SceneSnapshot, profile: SceneProfile,
                  *, project_name: str, asset_name: str, version: int,
                  dry_run: bool = False, replace: bool = False) -> ScenePublishResult:
    """Preflight and atomically publish a Maya scene with declared dependencies."""

    diagnostics = validate_scene(snapshot, profile)
    if diagnostics.blocks_publish:
        codes = ", ".join(item.code for item in diagnostics if item.blocks_publish)
        raise ValueError(f"Maya scene publish is blocked by: {codes}")
    root = Path(project_root).resolve(strict=True)
    scene = resolve_project_path(root, snapshot.scene_path)
    scene_fingerprint = fingerprint_file(scene)
    dependencies: dict[str, PublishFile] = {}
    for reference in snapshot.references:
        if reference.exists and reference.inside_project:
            dependencies.setdefault(reference.path, PublishFile(
                reference.path, "reference", fingerprint_file(resolve_project_path(root, reference.path)),
                "application/vnd.autodesk.maya",
            ))
    for texture in snapshot.textures:
        if texture.exists and texture.inside_project:
            dependencies.setdefault(texture.path, PublishFile(
                texture.path, "texture", fingerprint_file(resolve_project_path(root, texture.path)),
                _texture_media_type(texture.path),
            ))
    manifest = PublishManifest(
        kind=PublishKind.ASSET, project=project_name, name=asset_name, version=version,
        source_host="maya", source_path=snapshot.scene_path,
        source_fingerprint=scene_fingerprint,
        outputs=(PublishFile(snapshot.scene_path, "maya-scene", scene_fingerprint,
                             "application/vnd.autodesk.maya"),),
        dependencies=tuple(dependencies.values()),
        metadata={
            "linear_unit": snapshot.linear_unit,
            "time_unit": snapshot.time_unit,
            "frame_first": str(snapshot.first_frame),
            "frame_last": str(snapshot.last_frame),
        },
    )
    library = root / "Published"
    result = (plan_publish(root, library, manifest, replace=replace) if dry_run
              else publish_bundle(root, library, manifest, replace=replace))
    if dry_run:
        return ScenePublishResult(result.target, len(result.files),
                                  sum(item.fingerprint.size for item in result.files),
                                  result.manifest_fingerprint.sha256, True)
    return ScenePublishResult(result.target, result.copied_files, result.copied_bytes,
                              result.manifest_fingerprint.sha256, False)


def _texture_media_type(path: str) -> str:
    suffix = Path(path).suffix.casefold()
    return {
        ".exr": "image/x-exr", ".png": "image/png", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".tif": "image/tiff", ".tiff": "image/tiff",
    }.get(suffix, "application/octet-stream")
