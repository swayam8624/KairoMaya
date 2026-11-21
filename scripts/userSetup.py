# TEACHING MAP — scripts/userSetup.py
# Maya plugin bootstrapping/registration entrypoint executed by Maya's Python environment.
# Keep startup side effects explicit and do not run scene changes on import.
# Follow READING_ORDER.md for native-host and portable publish API boundaries.

"""Deferred Maya menu registration."""

import maya.utils

from kairo_maya.maya_adapter import install_menu

maya.utils.executeDeferred(install_menu)
