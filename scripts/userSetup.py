"""Deferred Maya menu registration."""

import maya.utils

from kairo_maya.maya_adapter import install_menu

maya.utils.executeDeferred(install_menu)
