# Artist workflow

1. Add the repository's `modules` directory to `MAYA_MODULE_PATH`.
2. Start Maya. `userSetup.py` registers **Kairo > Open SceneDoctor** after the
   host UI is ready.
3. Open the dockable panel and run **Validate Scene**.
4. Double-click a diagnostic to select its reference, transform, mesh, or
   texture node.
5. Resolve blocking units, timeline, missing dependency, namespace, topology,
   UV, material, texture, and scale issues.
6. Publish only after preflight succeeds. The publisher stages and verifies the
   Maya scene, references, and textures before atomically exposing a version.

Profile defaults can be overridden with `KAIRO_MAYA_LINEAR_UNIT`,
`KAIRO_MAYA_TIME_UNIT`, `KAIRO_MAYA_FIRST_FRAME`,
`KAIRO_MAYA_LAST_FRAME`, and `KAIRO_MAYA_TEXTURE_COLORSPACES`.

## Native release gate

- module loads and Kairo menu appears exactly once;
- panel docks, refreshes, and navigates to reported nodes;
- API 2.0 mesh inspection handles intermediate shapes and material slots;
- unloaded and broken references produce controlled diagnostics;
- a valid scene dry-runs and publishes a reloadable manifest.
