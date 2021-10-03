"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: systemtools
"""

from enum import Enum

class Event(Enum):
    """
    Provide log priority constans
    """

    ERROR = 1
    DEBUG = 2
    WARNING = 3
    INFO = 4
