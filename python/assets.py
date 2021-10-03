"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: assets
"""


from os.path import isfile, join

from datamodel import LogosLocallyCangeable


class LogosAttachments(LogosLocallyCangeable):
    """
    Provide updateable read-only attachments handling
    =================================================
    """


    def __init__(self, data : dict = None, version : int = 0):
        """
        Initialize the object instance
        ==============================

        Parameters
        ----------
        data : dict, optional (None if omitted)
            Data to set as initial internal data.
        version : int, optional (0 if omitted)
            Version to set as initial version.
        """

        super().__init__()
        self.__attachments = {}
        if data is not None:
            self.on_data_received(data, version)


    def add_attachment(self):
        """
        """


    def on_data_received(self, data : dict, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : dict
            Data to set as new internal data.
        version : int
            Version to set as new version.
        """

        super().on_data_received(data, version)
        self.__attachments = data.copy()


class AssetManager:
    """
    Provide asset management singleton
    ==================================
    """


    __DEFAULT_FOLDER = '.'

    __assets = {}
    __folder = '.'
