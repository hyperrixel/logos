"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: client
"""

from queue import PriorityQueue

from assets import AssetManager
from attributes import Descriptions, Tags
from attributes import LogosAttributes, LogosEditableAttributes
from flow import LogosChannel, LogosLog, LogosLogContainer, LogosLogEntry
from networking import Client
from systemtools import Event
from texts import Texts

class LogosClientBackend:
    """
    Provide client backeng functions
    ================================
    """

    def __init__(self):
        """
        Initialize the object instance
        ==============================
        """

        self.__is_healthy = True
        self.__log = PriorityQueue(maxsize=100)


    def close_log_entry(self, log_entry_id : str):
        """
        """

        return None # info about success


    def create_channel(self, attributes : dict = {}):
        """
        """

        return None # info about success and channel ID


    def create_log(self, channel_id : str, attributes : dict = {}):
        """
        """

        return None # info about success and log ID


    def create_log_entry(self, log_id : str, attributes : dict = {}):
        """
        """

        # Inform server about the beginning of the editing process
        return None # PackageID


    @property
    def catalog(self):
        """
        """

        # Additional catalog functions possible.
        return None # catalog


    def detach_channel(self, channel_id : str):
        """
        """

        return None # info about success


    def finish_log(self, log_id : str):
        """
        """

        return None # info about success


    def get_catalog(self):
        """
        """

        return # info about success


    def get_content(self, query_object : dict):
        """
        """

        return None # info and content


    def login(self, user_name : str, user_password : str):
        """
        """

        return None # Info about success and some user data

    def logout(self):
        """
        """

        return None  # Info about success


    def open_log_entry(self, log_entry_id : str):
        """
        """

        return None # info about success


    def save_log_entry(self, log_entry_id : str, storage_type : int):
        """
        storage_type <-- StorageTypes
        """

        return None


    def subscribe_to_stream(self, query_object : dict):
        """
        """

        return None # info about success and channel ID


    def unsubscribe_from_stream(self, channel_id : str):
        """
        """

        return None # info about success


    def update_log_entry(self, log_entry_id : str, text : str, metadata : dict,
                         attachments : dict, storage_type : int):
        """
        """

        return None # Info about success
