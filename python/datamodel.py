"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: datamodel
"""


from abc import ABC, abstractmethod
from json import dumps as json_dumps, loads as json_loads

from error import LogosSerializationError
from functiontools import check_data, now


class LogosSerializable(ABC):
    """
    Provide serializability functions
    =================================
    """


    @classmethod
    def deserialize(cls, data : any, **kwargs) -> any:
        """
        Return instance from serialized form
        ====================================

        Parameters
        ----------
        data : any
            Data in serialized form.
        keyword arguments
            Arguments to forward to deserializer staticmethod.

        Returns
        -------
        any
            The object that is created.

        Notes
        -----
        I.
            Main purpose of this function is to provide easy compatibility with
            future serialization/deserialization approaches different than JSON.
        II.
            Parameter data should be an object that is created by the
            .serialize() function of the same type of object.
        """

        return cls.from_json(data, **kwargs)


    @staticmethod
    @abstractmethod
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
        any
            The object that is created.

        Notes
        -----
            This function requires a JSON string that is created by the
            .to_json() function of the same type of object.
        """


    def serialize(self, **kwargs) -> any:
        """
        Create serialized data from an instance
        =======================================

        Parameters
        ----------
        keyword arguments
            Arguments to forward to the serializer funtion.

        Returns
        -------
        str
            Serialized data.

        Notes
        -----
            Main purpose of this function is to provide easy compatibility with
            future serialization/deserialization approaches different than JSON.
        """

        self.to_json(**kwargs)



    def to_json(self, **kwargs) -> str:
        """
        Create JSON from an instance
        ============================

        Parameters
        ----------
        keyword arguments
            Arguments to forward to json.dunps() funtion.

        Returns
        -------
        str
            JSON formatted string.
        """

        return json_dumps(self.to_json_dict(), **kwargs)


    @abstractmethod
    def to_json_dict(self) -> dict:
        """
        Abstract method to create a dict for creationg a JSON string from it
        ====================================================================

        Returns
        -------
        dict
            Dict to create a JSON formatted string.
        """


    @staticmethod
    def json_to_dict_(json_str : str, **kwargs) -> any:
        """
        """

        return json_loads(json_str, **kwargs)


class LogosUpgradeable(LogosSerializable):
    """
    Provide functionality to handle object upgrades
    ===============================================
    """

    def __init__(self, version : int = 0):
        """
        Initialize the object instance
        ==============================

        Parameter
        ---------
        version : int, optional (0 if omitted)
            Initial version ID of the instance.
        """

        self.__version = version


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
            When the given data doesn't contain the key 'version'.

        Notes
        -----
            This function requires a JSON string that is created by the
            .to_json() function of the same type of object.
        """

        data = LogosSerializable.json_to_dict_(json_str, **kwargs)
        if check_data(data, ['version']):
            return LogosUpgradeable(data['version'])


    def to_json_dict(self) -> dict:
        """
        Get JSON compatible dict
        ========================

        Returns
        -------
        dict
            A dict that can be serialized to JSON string.
        """

        return {'version' : self.version}


    def upgrade(self):
        """
        """

        self.__version += 1


    @property
    def version(self) -> int:
        """
        """
        return self.__version


    def __repr__(self) -> str:
        """
        Get the representation of the object
        ====================================

        Returns
        -------
        str
            A string to instantiate the same object.
        """

        return 'LogosUpgradeable({})'.format(self.version)


    def __str__(self) -> str:
        """
        Get human readable description of the object
        ============================================

        Returns
        -------
        str
            A string to describe the characteristics of the object.
        """

        return 'logos.LogosUpgradeable object with version {}'.format(
               self.version)


class LogosUpdateable:
    """
    Provide updateable read-only class template
    ===========================================
    """

    def __init__(self):
        """
        Initialize the object instance
        ==============================

        Note
        ----
            Since version and last_update are protected values, if you have
            custom __init__() function do not forget to call super().__init__()
            from the sublcasse on Initialization.
        """

        self.__last_update = 0
        self.__version = 0


    @property
    def last_update(self) -> int:
        """
        Get the timestamp of the last update
        ====================================

        Returns
        -------
        int
            Millisecond precision timestamp of the last update.
        """

        return self.__last_update


    @property
    def version(self) -> int:
        """
        Get the object's version
        ========================

        Returns
        -------
        int
            The actual version of the object.
        """

        return self.__version


    @property
    def is_ready(self) -> bool:
        """
        Get whether the singleton is ready
        ==================================

        Returns
        -------
        bool
            If the class is ready to work with.
        """

        return self.__last_update > 0


    def on_data_received(self, data : any, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : any
            Data to set as new internal data.
        version : int
            Version to set as new version.

        Notes
        -----
            Always call super().on_data_received(data, version) to update the
            values of last_update and versison.
        """

        self.__last_update = now()
        self.__version = version


    def on_update(self):
        """
        Handle generic update event
        ===========================
        """

        self.__last_update = now()


class LogosLocallyCangeable(LogosUpdateable):
    """
    Provide updateable and locally changeable class template
    ========================================================
    """

    def __init__(self):
        """
        Initialize the object instance
        ==============================

        Note
        ----
            Since version, last_update and is_changed are protected values,
            if you have custom __init__() function do not forget to call
            super().__init__() from the sublcasse on Initialization.
        """

        super().__init__()
        self.__is_changed = False


    @property
    def is_changed(self) -> bool:
        """
        Get changed state of the instance
        =================================

        Returns
        -------
        bool
            True if instance is locally changed, False if not.
        """

        return self.__is_changed


    def on_data_received(self, data : any, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : any
            Data to set as new internal data.
        version : int
            Version to set as new version.

        Notes
        -----
            Always call super().on_data_received(data, version) to update the
            values of last_update and versison.
        """

        super().on_data_received(data, version)
        self.__is_changed = False


    def on_update(self):
        """
        Handle generic update event
        ===========================
        """

        super().on_update()
        self.__is_changed = True


    @abstractmethod
    def to_json_dict(self) -> dict:
        """
        Abstract method to create a dict for creationg a JSON string from it
        ====================================================================

        Returns
        -------
        dict
            Dict to create a JSON formatted string.
        """


class LogosUpdateableSingleton:
    """
    Provide updateable read-only singleton template
    ===============================================
    """

    __last_update = 0
    __version = 0


    @classmethod
    def get_last_update(cls) -> int:
        """
        Get the timestamp of the last update
        ====================================

        Returns
        -------
        int
            Millisecond precision timestamp of the last update.
        """

        return cls.__last_update


    @classmethod
    def get_version(cls) -> int:
        """
        Get the object's version
        ========================

        Returns
        -------
        int
            The actual version of the object.
        """

        return cls.__version


    @classmethod
    def is_ready(cls) -> bool:
        """
        Get whether the singleton is ready
        ==================================

        Returns
        -------
        bool
            If the class is ready to work with.
        """

        return cls.__last_update > 0


    @classmethod
    def on_data_received(cls, data : any, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : any
            Data to set as new internal data.
        version : int
            Version to set as new version.

        Notes
        -----
            Always call super().on_data_received(data, version) to update the
            values of last_update and versison.
        """

        cls.__last_update = now()
        cls.__version = version
