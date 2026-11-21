# KairoMaya — teaching source reading order

Start with the [README](../README.md), then follow this **workflow-oriented** path. These repositories integrate with [KairoPipelineCore](https://github.com/swayam8624/KairoPipelineCore), the host-neutral Python contracts. The order below describes how a user action reaches validated, publishable data—not the import/build order.

1. [scripts/userSetup.py](../scripts/userSetup.py) — read API inputs, output contracts, errors and downstream caller.
2. [python/kairo_maya/__init__.py](../python/kairo_maya/__init__.py) — read API inputs, output contracts, errors and downstream caller.
3. [python/kairo_maya/maya_adapter.py](../python/kairo_maya/maya_adapter.py) — read API inputs, output contracts, errors and downstream caller.
4. [python/kairo_maya/scenedoctor.py](../python/kairo_maya/scenedoctor.py) — read API inputs, output contracts, errors and downstream caller.
5. [python/kairo_maya/publisher.py](../python/kairo_maya/publisher.py) — read API inputs, output contracts, errors and downstream caller.
6. [modules/KairoMaya.mod](../modules/KairoMaya.mod) — read API inputs, output contracts, errors and downstream caller.
7. [tests/test_maya_adapter.py](../tests/test_maya_adapter.py) — read API inputs, output contracts, errors and downstream caller.
8. [tests/test_scenedoctor.py](../tests/test_scenedoctor.py) — read API inputs, output contracts, errors and downstream caller.
9. [tests/test_publisher.py](../tests/test_publisher.py) — read API inputs, output contracts, errors and downstream caller.

## Data flow

Maya startup/UI → guarded maya.cmds/OpenMaya 2.0 host adapter snapshots references, units, meshes, textures, scene paths → immutable SceneSnapshot and SceneProfile checks in scenedoctor.py → navigable structured diagnostics → publisher validates references and SHA-256 → KairoPipelineCore atomic manifest publication. The pure validation code never imports maya.

## Boundary of the tests

Python tests do not prove native Maya mesh API behavior or docked UI startup. Preserve the explicit native release checklist and avoid claiming scene repair that the adapter does not perform.

## Teaching exercises

1. Trace one host action or command into a pure validation function and its structured diagnostic.
2. Identify where filesystem paths are normalized and hashed before publishing.
3. Feed malformed/missing files to the host-neutral path and locate the specific failure/diagnostic.
4. Run the portable tests; then read the native verification checklist before claiming host support.
5. Explain why a dry-run plan, a completed atomic publish, and a native host import are three different events.

## Licensing

Preserve the repository's existing [LICENSE](../LICENSE). The original source and documentation permit learning and development according to that file; external DCC SDKs, plugins, images and example assets retain their own terms.
