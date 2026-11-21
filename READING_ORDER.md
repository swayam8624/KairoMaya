# KairoMaya: linked source-reading order

Begin with scene/reference diagnostics and a pure publisher, then Maya API 2.0 adapter, userSetup entry point and tests. Native Maya state and Qt windows belong to the adapter, while KairoPipelineCore handles portable publish format and hashes.

## APIs and boundaries

SceneDoctor inspects authored nodes/links, publisher validates output/provenance, maya_adapter maps these to native Maya APIs. Explicit fixes and previews must not silently alter artist work; native host tests differ from pure Python tests.

## Read these files (8)

1. [`python/kairo_maya/scenedoctor.py`](python/kairo_maya/scenedoctor.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
2. [`python/kairo_maya/publisher.py`](python/kairo_maya/publisher.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
3. [`python/kairo_maya/maya_adapter.py`](python/kairo_maya/maya_adapter.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
4. [`scripts/userSetup.py`](scripts/userSetup.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
5. [`tests/test_scenedoctor.py`](tests/test_scenedoctor.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
6. [`tests/test_maya_adapter.py`](tests/test_maya_adapter.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
7. [`python/kairo_maya/__init__.py`](python/kairo_maya/__init__.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
8. [`tests/test_publisher.py`](tests/test_publisher.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.

## License and verification

This repository preserves its existing [LICENSE](LICENSE) for original work; external artist tools, SDKs, output media and third-party assets keep their own terms. Educational reuse and further development are encouraged within those licenses. Use [README](README.md) for actual host configuration. A source guide or passing pure-Python unit tests do not imply a successful native-host integration run.
