"""Guarded Maya API 2.0 adapter for SceneDoctor."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .scenedoctor import (
    MeshSnapshot, ReferenceSnapshot, SceneProfile, SceneSnapshot,
    TextureSnapshot, TransformSnapshot, validate_scene,
)

try:
    import maya.cmds as _cmds  # type: ignore[import-not-found]
    import maya.api.OpenMaya as _om  # type: ignore[import-not-found]
except ImportError:
    _cmds = None
    _om = None


def require_maya() -> tuple[Any, Any]:
    if _cmds is None or _om is None:
        raise RuntimeError("KairoMaya host operations require Maya's Python runtime")
    return _cmds, _om


def inspect_scene(profile: SceneProfile | None = None):
    """Snapshot the open Maya scene and return deterministic diagnostics."""

    cmds, om = require_maya()
    project = Path(cmds.workspace(query=True, rootDirectory=True)).resolve(strict=True)
    scene_path = str(cmds.file(query=True, sceneName=True) or "")
    selected_profile = profile or SceneProfile(
        linear_unit=os.environ.get("KAIRO_MAYA_LINEAR_UNIT", "cm"),
        time_unit=os.environ.get("KAIRO_MAYA_TIME_UNIT", "film"),
        first_frame=float(os.environ.get("KAIRO_MAYA_FIRST_FRAME", "1001")),
        last_frame=float(os.environ.get("KAIRO_MAYA_LAST_FRAME", "1100")),
        required_texture_color_spaces=tuple(
            value.strip() for value in os.environ.get(
                "KAIRO_MAYA_TEXTURE_COLORSPACES", ""
            ).split(",") if value.strip()
        ),
    )
    snapshot = SceneSnapshot(
        scene_path=_portable_path(project, scene_path),
        saved=bool(scene_path),
        linear_unit=str(cmds.currentUnit(query=True, linear=True)),
        time_unit=str(cmds.currentUnit(query=True, time=True)),
        first_frame=float(cmds.playbackOptions(query=True, minTime=True)),
        last_frame=float(cmds.playbackOptions(query=True, maxTime=True)),
        unknown_plugins=tuple(cmds.unknownPlugin(query=True, list=True) or ()),
        references=_references(cmds, project),
        transforms=_export_roots(cmds),
        meshes=_meshes(cmds, om),
        textures=_textures(cmds, project),
    )
    return validate_scene(snapshot, selected_profile)


def select_location(object_path: str) -> None:
    cmds, _ = require_maya()
    if not cmds.objExists(object_path):
        raise ValueError(f"Maya object no longer exists: {object_path}")
    cmds.select(object_path, replace=True)


def install_menu() -> None:
    cmds, _ = require_maya()
    if cmds.menu("KairoProductionMenu", exists=True):
        cmds.deleteUI("KairoProductionMenu")
    menu = cmds.menu("KairoProductionMenu", label="Kairo", parent="MayaWindow", tearOff=True)
    cmds.menuItem(label="Open SceneDoctor", parent=menu,
                  command=lambda *_: show_panel())


def _references(cmds: Any, project: Path) -> tuple[ReferenceSnapshot, ...]:
    result = []
    for path in cmds.file(query=True, reference=True) or ():
        try:
            node = str(cmds.referenceQuery(path, referenceNode=True))
            namespace = str(cmds.referenceQuery(node, namespace=True)).lstrip(":")
            loaded = bool(cmds.referenceQuery(node, isLoaded=True))
        except RuntimeError:
            node, namespace, loaded = str(path), "", False
        source = Path(path).resolve(strict=False)
        result.append(ReferenceSnapshot(
            node=node, path=_portable_path(project, str(source)), namespace=namespace,
            loaded=loaded, exists=source.is_file(), inside_project=_inside(project, source),
        ))
    return tuple(result)


def _export_roots(cmds: Any) -> tuple[TransformSnapshot, ...]:
    roots: set[str] = set()
    for shape in cmds.ls(type="mesh", long=True) or ():
        parents = cmds.listRelatives(shape, parent=True, fullPath=True) or ()
        if not parents:
            continue
        current = parents[0]
        while True:
            parent = cmds.listRelatives(current, parent=True, fullPath=True) or ()
            if not parent:
                break
            current = parent[0]
        roots.add(current)
    return tuple(TransformSnapshot(
        name=node,
        translation=tuple(float(v) for v in cmds.getAttr(f"{node}.translate")[0]),
        rotation=tuple(float(v) for v in cmds.getAttr(f"{node}.rotate")[0]),
        scale=tuple(float(v) for v in cmds.getAttr(f"{node}.scale")[0]),
    ) for node in sorted(roots))


def _meshes(cmds: Any, om: Any) -> tuple[MeshSnapshot, ...]:
    result = []
    for name in cmds.ls(type="mesh", long=True, noIntermediate=True) or ():
        selection = om.MSelectionList()
        selection.add(name)
        function = om.MFnMesh(selection.getDagPath(0))
        shaders, _ = function.getConnectedShaders(0)
        nonmanifold = cmds.polyInfo(name, nonManifoldEdges=True) or ()
        lamina = cmds.polyInfo(name, laminaFaces=True) or ()
        result.append(MeshSnapshot(
            name=name, vertices=function.numVertices,
            uv_sets=len(function.getUVSetNames()), assigned_materials=len(shaders),
            nonmanifold_edges=len(nonmanifold), lamina_faces=len(lamina),
        ))
    return tuple(result)


def _textures(cmds: Any, project: Path) -> tuple[TextureSnapshot, ...]:
    result = []
    for node in cmds.ls(type="file") or ():
        raw = str(cmds.getAttr(f"{node}.fileTextureName") or "")
        source = Path(os.path.expandvars(raw)).expanduser().resolve(strict=False)
        result.append(TextureSnapshot(
            node=node, path=_portable_path(project, str(source)), exists=source.is_file(),
            inside_project=_inside(project, source),
            color_space=str(cmds.getAttr(f"{node}.colorSpace") or ""),
        ))
    return tuple(result)


def _inside(project: Path, source: Path) -> bool:
    try:
        source.relative_to(project)
        return True
    except ValueError:
        return False


def _portable_path(project: Path, raw: str) -> str:
    if not raw:
        return ""
    source = Path(raw).resolve(strict=False)
    try:
        return source.relative_to(project).as_posix()
    except ValueError:
        return source.as_posix()


_window = None


def show_panel() -> None:
    """Open a dockable SceneDoctor results panel in Maya."""

    require_maya()
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
    try:
        from PySide6 import QtCore, QtWidgets
    except ImportError:
        from PySide2 import QtCore, QtWidgets  # type: ignore[no-redef,import-not-found]

    class SceneDoctorWindow(MayaQWidgetDockableMixin, QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.setObjectName("KairoSceneDoctorWindow")
            self.setWindowTitle("Kairo SceneDoctor")
            layout = QtWidgets.QVBoxLayout(self)
            self.summary = QtWidgets.QLabel("Run a production scene preflight.")
            self.results = QtWidgets.QListWidget()
            run_button = QtWidgets.QPushButton("Validate Scene")
            layout.addWidget(self.summary)
            layout.addWidget(self.results)
            layout.addWidget(run_button)
            run_button.clicked.connect(self.refresh)
            self.results.itemDoubleClicked.connect(self.navigate)
            self.refresh()

        def refresh(self):
            self.results.clear()
            try:
                diagnostics = inspect_scene()
            except Exception as error:
                self.summary.setText(f"SceneDoctor could not run: {error}")
                return
            items = tuple(diagnostics)
            state = "BLOCKED" if diagnostics.blocks_publish else "READY"
            self.summary.setText(f"{state} · {len(items)} diagnostic(s)")
            for diagnostic in items:
                item = QtWidgets.QListWidgetItem(
                    f"{diagnostic.severity.value.upper()} · {diagnostic.code}\n"
                    f"{diagnostic.message}\n{diagnostic.suggestion}"
                )
                location = diagnostic.location.object_path if diagnostic.location else ""
                item.setData(QtCore.Qt.UserRole, location)
                self.results.addItem(item)

        def navigate(self, item):
            location = item.data(QtCore.Qt.UserRole)
            if location and location != "scene":
                select_location(location)

    global _window
    if _window is not None:
        _window.close()
    _window = SceneDoctorWindow()
    _window.show(dockable=True, area="right", floating=False)
