# Kairo Maya SceneDoctor

SceneDoctor is a Maya scene preflight for references, namespaces, transforms,
units, timelines, mesh topology, UVs, materials, textures, and unknown plugins.
It presents deterministic diagnostics in a dockable artist panel and keeps the
rules testable outside Maya.

```bash
PYTHONPATH=../KairoPipelineCore/src:python \
  python3 -m unittest discover -s tests -v
```

The real `maya.cmds` and API 2.0 adapter is guarded. Native Maya verification
is a separate release gate and is never inferred from mocks.

## Production behavior

- API 2.0 mesh snapshots plus Maya command-layer scene/reference inspection;
- dockable results with navigation back to the failing production node;
- bounded diagnostics: SceneDoctor never silently freezes transforms, repairs
  topology, strips unknown plugins, or rewrites reference namespaces;
- dry-run and atomic asset publication with SHA-256 verified dependencies.

See [the artist workflow](docs/artist-workflow.md) for installation and the
native release checklist.


## Source learning pathway

Follow [the linked reading order](docs/SOURCE_READING_ORDER.md) to trace module ownership, public interfaces, implementation, tests and cross-repository interaction. This path is designed for learners who want to understand both the algorithms and the API boundaries rather than just execute a sample.

## Open-source learning and extension

Original contributions may be learned from, modified and further developed under the applicable [LICENSE](LICENSE). Preserve required notices; external libraries, application-host SDKs, source adaptations, datasets and media retain their own terms. Check [STATUS.md](STATUS.md) and native-host evidence before treating a feature as verified.
