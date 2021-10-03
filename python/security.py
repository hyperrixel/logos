"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: security
"""


from enum import Enum

from datamodel import LogosSerializable


class LogosPermissionTypes(Enum):
    """
    Provide constants to handle permissions
    =======================================
    """

    NO_PERMISSION = 0
    READ = 1
    WRITE = 2
    ADMINISTRATE = 4


class LogosPermissions(LogosSerializable):
    """
    Provide catalogue of permissions
    ================================
    """

    def __init__(self, permissions : list = None):
        """
        """

        if permissions is None:
            pass
        else:
            pass
