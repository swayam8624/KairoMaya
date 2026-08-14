# Contributing

Keep changes focused and run:

```bash
PYTHONPATH=../KairoPipelineCore/src:python \
  python3 -m unittest discover -s tests -v
python3 -m compileall -q python scripts tests
```

Changes to `maya_adapter.py`, `userSetup.py`, or the module descriptor require
a native Maya smoke. Include the Maya version and license type used.
