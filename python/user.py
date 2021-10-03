"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: user
"""


from enum import Enum

from attributes import LogosAttributes
from datamodel import LogosSerializable, LogosUpdateable
from datamodel import LogosUpdateableSingleton
from functiontools import check_data
from functiontools import rsa_str_to_private_key, rsa_str_to_public_key


# ------------- CLIENT SIDE ------------- #


class LogosActivityStates(Enum):
    """
    Provide constants to handle user activity
    =========================================
    """

    OFFLINE = 0
    ONLINE = 1
    WRITING = 2


class LogosUser(LogosUpdateable):
    """
    Provide non-current user's functionality
    ========================================
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
        self.__id = None
        self.__display_name = None
        self.__attributes = None
        self.__activity = LogosActivityStates.OFFLINE.value
        if data is not None:
            self.on_data_received(data, version)


    @property
    def activity(self) -> int:
        """
        Get activity status
        ===================

        Returns
        -------
        int
            The activity status of the user.
        """

        return self.__activity


    @property
    def attributes(self) -> any:
        """
        Get direct acces to attributes
        ==============================

        Returns
        -------
        any
            Attributes of the user.
        """

        return self.__attributes


    @property
    def display_name(self) -> str:
        """
        Get displayed name
        ==================

        Returns
        -------
        str
            The displayed name of the user.
        """

        return self.__display_name


    @property
    def id(self) -> str:
        """
        Get user ID
        ===========

        Returns
        -------
        str
            The ID of the user.
        """

        return self.__id


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
        check_data(data, ['id', 'display_name', 'attributes', 'activity'])
        self.__id = data['id']
        self.__display_name = data['display_name']
        self.__attributes = None # TODO: implement
        self.__activity = data['activity']


class CurrentUser(LogosUpdateableSingleton):
    """
    Singleton to provide access to the curent user
    """


    __attributes = None
    __display_name = None
    __id = None
    __server_key = None
    __sig_key = None
    __terminal_settings = None


    @classmethod
    def get_attributes(cls) -> str:
        """
        Get attributes of the curent user
        =========================================

        Returns
        -------
        str
            The attributes of the curcent user.
        """

        return cls.__attributes


    @classmethod
    def get_display_name(cls) -> str:
        """
        Get the displayed name of the curent user
        =========================================

        Returns
        -------
        str
            The displayed name of the curcent user.
        """

        return cls.__display_name


    @classmethod
    def get_id(cls) -> str:
        """
        Get the ID of the curent user
        =============================

        Returns
        -------
        str
            The ID of the curcent user.
        """

        return cls.__id


    @classmethod
    def get_server_key(cls) -> str:
        """
        Get server key
        ==============

        Returns
        -------
        str
            The key of the server.
        """

        return cls.__sig_key


    @classmethod
    def get_sig_key(cls) -> str:
        """
        Get signautre key of the current user
        =====================================

        Returns
        -------
        str
            The signature key of the curcent user.
        """

        return cls.__sig_key


    @classmethod
    def get_terminal_settings(cls) -> str:
        """
        Get the settings of the terminal of the curent user
        ===================================================

        Returns
        -------
        str
            The settings of the terminal of the curcent user.
        """

        return cls.__terminal_settings


    @classmethod
    def on_data_received(cls, data : dict, version : int):
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
        check_data(data, ['id', 'display_name', 'attributes', 'sig_key',
                   'server_key', 'terminal_settings'])
        self.__id = data['id']
        self.__display_name = data['display_name']
        self.__attributes = None # TODO Implement
        self.__sig_key = data['sig_key']
        self.__server_key = data['server_key']
        self.__terminal_settings = data['terminal_settings']


# ------------- SERVER SIDE ------------- #


class LogosBaseUser(LogosSerializable):
    """
    Provide base user
    =================
    """

    def __init__(self, id : str):
        """
        Initialize the object instance
        ==============================

        Parameters
        ----------
        id : str
            ID of the user.
        """

        self.__id = id


    @staticmethod
    def from_json(json_str : str, **kwargs) -> any:
        """
        Abstract methot to build object from JSON string
        ================================================
        Parameters
        ----------

        json_string : str
            The JSON formatted string that contains all the needed data.
        keyword arguments
            Arguments to forward to json.loads() funtion.

        Returns
        -------
        LogosBaseUser
            The object that is created.

        Raises
        ------
        LogosSerializationError
            When the given data is not a dict.
        LogosSerializationError
            When the given data doesn't contain the key 'id'.

        Notes
        -----
            This function requires a JSON string that is created by the
            .to_json() function of the same type of object.
        """

        data = LogosSerializable.json_to_dict_(json_str, **kwargs)
        if check_data(data, ['id']):
            return LogosBaseUser(data['id'])


    @property
    def id(self) -> str:
        """
        Get ID of the user
        ==================

        Returns
        -------
        str
            The ID of the user.
        """

        return self.__id


    def to_json_dict(self) -> dict:
        """
        Get JSON compatible dict
        ========================

        Returns
        -------
        dict
            A dict that can be serialized to JSON string.
        """

        return {'id' : self.id}


    def __repr__(self) -> str:
        """
        Get the representation of the object
        ====================================

        Returns
        -------
        str
            A string to instantiate the same object.
        """

        return 'LogosBaseUser({})'.format(self.id)


    def __str__(self) -> str:
        """
        Get human readable description of the object
        ============================================

        Returns
        -------
        str
            A string to describe the characteristics of the object.
        """

        return 'logos.LogosBaseUser object with ID {}'.format(self.id)


class LogosSignUser(LogosBaseUser):
    """
    Provide user with public key
    ============================
    """

    def __init__(self, id : str, sig_key : str):
        """
        Initialize the object instance
        ==============================

        Parameters
        ----------
        id : str
            ID of the user.
        sig_key : str
            Public signature key of the user.
        """

        super().__init__(id)
        self.__sig_key = sig_key


    @staticmethod
    def from_json(json_str : str, **kwargs) -> any:
        """
        Abstract methot to build object from JSON string
        ================================================
        Parameters
        ----------

        json_string : str
            The JSON formatted string that contains all the needed data.
        keyword arguments
            Arguments to forward to json.loads() funtion.

        Returns
        -------
        LogosBaseUser
            The object that is created.

        Raises
        ------
        LogosSerializationError
            When the given data is not a dict.
        LogosSerializationError
            When the given data doesn't contain the keys 'id' and 'sig_key'.

        Notes
        -----
            This function requires a JSON string that is created by the
            .to_json() function of the same type of object.
        """

        data = LogosSerializable.json_to_dict_(json_str, **kwargs)
        if check_data(data, ['id', 'sig_key']):
            return LogosSignUser(data['id'], data['sig_key'])


    @property
    def sig_key(self) -> str:
        """
        """

        return self.__sig_key


    def to_json_dict(self) -> dict:
        """
        Get JSON compatible dict
        ========================

        Returns
        -------
        dict
            A dict that can be serialized to JSON string.
        """

        return {'id' : self.id, 'sig_key' : self.sig_key}


    def __repr__(self) -> str:
        """
        Get the representation of the object
        ====================================

        Returns
        -------
        str
            A string to instantiate the same object.
        """

        return 'LogosSignUser({}, {})'.format(self.id, self.sig_key)


    def __str__(self) -> str:
        """
        Get human readable description of the object
        ============================================

        Returns
        -------
        str
            A string to describe the characteristics of the object.
        """

        return 'logos.LogosSignUser object with ID {}, public key {}'.format(
                self.id, self.sig_key)


class LogosServerUser(LogosSignUser):
    """
    Provide server side user
    ========================
    """

    def __init__(self, id : str, pass_hash : str, sig_key : str,
                 display_name : str, attributes : LogosAttributes = None):
        """
        Initialize the object instance
        ==============================

        Parameters
        ----------
        id : str
            ID of the user.
        pass_hash : str
            Password hash of the user.
        sig_key : str
            Public signature key of the user.
        display_name : str
            Display name of the user.
        attributes : LogosAttributes, optional (None if omitted.)
            Other attributes of the user.
        """

        super().__init__(id, sig_key)
        self.__display_name = display_name
        self.__pass_hash = pass_hash
        if attributes is None:
            self.__attributes = LogosAttributes()
        else:
            self.__attributes = attributes


    @property
    def display_name(self) -> str:
        """
        """

        return self.__display_name


    @staticmethod
    def from_json(json_str : str, **kwargs) -> any:
        """
        Abstract methot to build object from JSON string
        ================================================
        Parameters
        ----------

        json_string : str
            The JSON formatted string that contains all the needed data.
        keyword arguments
            Arguments to forward to json.loads() funtion.

        Returns
        -------
        LogosBaseUser
            The object that is created.

        Raises
        ------
        LogosSerializationError
            When the given data is not a dict.
        LogosSerializationError
            When the given data doesn't contain the required keys.

        Notes
        -----
            This function requires a JSON string that is created by the
            .to_json() function of the same type of object.
        """

        data = LogosSerializable.json_to_dict_(json_str, **kwargs)
        if check_data(data, ['id', 'pass_hash', 'sig_key', 'display_name',
                             'attributes']):
            return LogosServerUser(data['id'], data['pass_hash'],
                                   data['sig_key'], data['display_name'],
                                   LogosAttributesObject
                                   .from_dict(data['attributes']))


    @property
    def pass_hash(self) -> str:
        """
        """

        return self.__pass_hash


    def to_json_dict(self) -> dict:
        """
        Get JSON compatible dict
        ========================

        Returns
        -------
        dict
            A dict that can be serialized to JSON string.
        """

        return {'id' : self.id}


    def __repr__(self) -> str:
        """
        Get the representation of the object
        ====================================

        Returns
        -------
        str
            A string to instantiate the same object.
        """

        return 'LogosBaseUser({})'.format(self.id)


    def __str__(self) -> str:
        """
        Get human readable description of the object
        ============================================

        Returns
        -------
        str
            A string to describe the characteristics of the object.
        """

        return 'logos.LogosBaseUser object with ID {}'.format(self.id)
