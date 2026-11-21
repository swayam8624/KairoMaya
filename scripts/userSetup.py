# SOURCE STUDY NOTE:
# Maya startup hook exposing Kairo SceneDoctor through native Maya Python. It should not run scene
# edits automatically at application startup.
# See docs/SOURCE_READING_ORDER.md for host → preflight → publish flow.

"""Deferred Maya menu registration."""

import maya.utils

from kairo_maya.maya_adapter import install_menu

maya.utils.executeDeferred(install_menu)
