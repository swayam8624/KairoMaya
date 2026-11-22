# Teaching source map — KairoMaya
**Worked source walkthrough:** [Maya references/transforms → SceneDoctor → shared publish](https://github.com/swayam8624/KairoPipelineCore/blob/docs/teaching-walkthrough-20261121/docs/CROSS_DCC_PUBLICATION_WALKTHROUGH.md).

Maya scene inspection and versioned export/publication.

Read these source links in order, identify the caller and callee for each public API, then check the error/ownership contract and its tests.

## Reading order

1. [`README.md`](../README.md)
2. [`pyproject.toml`](../pyproject.toml)
3. [`modules`](../modules)
4. [`python`](../python)
5. [`scripts`](../scripts)
6. [`tests`](../tests)
7. [`docs`](../docs)

## Repository integration and API contracts

Maya API adapters inspect scene content, run preflight and publish to PipelineCore. Consumer-side checks occur in KairoAssets; automated unit tests do not prove native Maya GUI execution.

## Teaching standards

- Comments explain invariants, decision reasons, lifetime, prerequisites and cross-file effects; they do not narrate obvious statements.
- Follow upstream interfaces before implementation details; distinguish implemented, host-verified and planned features.
- Run available tests at a pinned commit and consult [STATUS.md](../STATUS.md) / [STATUS.yaml](../STATUS.yaml) before declaring completion.
- Reuse original contributions under [LICENSE](../LICENSE), subject to third-party code and asset terms.


## Complete source-file inventory

After the curated teaching path, follow this deterministic inventory of first-party source, scripts, shaders, and tests. Grouping is a suggested learning order, not an indication that every function is already annotated. Vendored dependencies, ROMs, binaries, data, media, and generated evidence are excluded.

### Implementation and other source (4)

1. [`python/kairo_maya/__init__.py`](../python/kairo_maya/__init__.py)
2. [`python/kairo_maya/maya_adapter.py`](../python/kairo_maya/maya_adapter.py)
3. [`python/kairo_maya/publisher.py`](../python/kairo_maya/publisher.py)
4. [`python/kairo_maya/scenedoctor.py`](../python/kairo_maya/scenedoctor.py)

### Automation and tooling (1)

1. [`scripts/userSetup.py`](../scripts/userSetup.py)

### Verification and tests (3)

1. [`tests/test_maya_adapter.py`](../tests/test_maya_adapter.py)
2. [`tests/test_publisher.py`](../tests/test_publisher.py)
3. [`tests/test_scenedoctor.py`](../tests/test_scenedoctor.py)

Snapshot totals: 8 first-party source/build/test files, 21 tracked files overall. Re-audit when files are renamed or added.
