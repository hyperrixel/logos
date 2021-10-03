"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: flow
"""


from attributes import LogosAttributes, LogosEditableAttributes
from datamodel import LogosLocallyCangeable, LogosUpdateable
from error import LogosPermissionError, LogosStatusError
from functiontools import check_data, now
from security import LogosPermissionTypes
from user import CurrentUser


class LogosFlowObject(LogosUpdateable):
    """
    Provide common flow functions
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
        self.__name = None
        self.__access_mode = LogosPermissionTypes.NO_PERMISSION.value
        self.__attributes = None
        if data is not None:
            self.on_data_received(data, version)


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
        check_data(data, ['id', 'name', 'access_mode', 'attributes'])
        self.__id = data['id']
        self.__name = data['name']
        self.__access_mode = data['access_mode']
        self.__attributes = LogosAttributes(data['attributes'])


    @property
    def access_mode(self) -> int:
        """
        Get access mode of the channel
        ==============================

        Return
        ------
        str
            The access mode of the channel.
        """

        return self.__access_mode


    @property
    def attributes(self) -> any:
        """
        Get direct access to the attributes
        ===================================

        Returns
        -------
        any
            Attributes of the instance.
        """

        return self.__attributes



    @property
    def id(self) -> str:
        """
        Get ID of the channel
        =====================

        Return
        ------
        str
            The ID of the channel.
        """

        return self.__id


    @property
    def name(self) -> str:
        """
        Get name of the channel
        =======================

        Return
        ------
        str
            The name of the channel.
        """

        return self.__name


class LogosLog(LogosFlowObject):
    """
    Provide log's functions
    =======================
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
        self.__entries = None
        if data is not None:
            self.on_data_received(data, version)


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
        check_data(data, ['id', 'name', 'access_mode', 'attributes', 'entries'])
        self.__entries = None # TODO Implement


class LogosLogContainer(dict):
    """
    Provide container for logs
    ==========================
    """


    def __init__(self, logs : dict = None):
        """
        Initialize the object instance
        ==============================
        """

        super().__init__()
        self.__in_init = True
        if logs is not None:
            for key, value in logs.items():
                self[key] = Log(value)
        self.__in_init = False


    def __setitem__(self, key : str, value : LogosLog):
        """
        Provide compatibility with the built-in __setitem__ method
        ==========================================================

        Parameters
        ----------
        key : str
            Key to set.
        value : LogosLog
            Value to set.

        Raises
        ------
        LogosPermissionError
            If tried to change a key after Initialization since
            LogosLogContainer is immutable.
        """

        if not self.__in_init:
            raise LogosPermissionError('LogosLogContainer is immutable.')
        super().__setitem__(key, value)


class LogosChannel(LogosFlowObject):
    """
    Provide channel's functions
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
        self.__logs = LogosLogContainer()
        if data is not None:
            self.on_data_received(data, version)


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
        check_data(data, ['id', 'name', 'access_mode', 'attributes', 'logs'])
        self.__logs = LogosLogContainer(data['logs'])


    @property
    def logs(self) -> any:
        """
        Get direct access to the logs
        ===================================

        Returns
        -------
        any
            Logs of the instance.
        """

        return self.__logs


class LogosLogEntry(LogosLocallyCangeable):
    """
    Provide log entry's functions
    =============================
    """

    def __init__(self, data : dict = None, version = 0):
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
        self.__id_time = 0
        self.__id_user = ''
        self.__access_mode = LogosPermissionTypes.NO_PERMISSION.value
        self.__content = ''
        self.__attributes = LogosEditableAttributes()
        self.__attachments = None
        self.__is_finished = False
        if data is not None:
            self.on_data_received(data, version)


    @property
    def access_mode(self) -> int:
        """
        Get the access mode
        ===================

        Return
        ------
        str
            The access mode of the log entry.
        """

        return self.__access_mode


    @property
    def attributes(self) -> any:
        """
        Get direct access to the attributes
        ===================================

        Returns
        -------
        any
            Attributes of the instance.
        """

        return self.__attributes


    @property
    def attachments(self) -> any:
        """
        Get direct access to the attachments
        ====================================

        Returns
        -------
        any
            Attachments of the instance.
        """

        return self.__attachments


    @property
    def content(self) -> str:
        """
        Get text content
        ================

        Returns
        -------
        str
            The text content of the log entry.
        """

        return self.__content


    @content.setter
    def content(self, new_contant : str):
        """
        Set, update text content
        ========================

        Returns
        -------
        new_contant : str
            The new text content of the log entry.
        """

        self.__content = new_contant
        super().on_update()


    @property
    def id(self) -> int:
        """
        Get the combined ID
        ===================

        Returns
        -------
        int
            The combined ID of the log entry.
        """

        return '{}-{}'.format(self.__id_time, self.__id_user)


    @property
    def id_tine(self) -> int:
        """
        Get the time part of the ID
        ===========================

        Returns
        -------
        int
            The time part of the ID of the log entry.
        """

        return self.__id_time


    @property
    def id_user(self) -> str:
        """
        Get the user part of the ID
        ===========================

        Returns
        -------
        str
            The user part of the ID of the log entry.
        """

        return self.__id_time


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

        return any([super().is_changed, self.attributes.is_changed,
                    self.attachments.is_changed])


    @property
    def is_finished(self) -> str:
        """
        Get the finished state
        ======================

        Returns
        -------
        str
            The finished state of the log entry.
        """

        return self.__is_finished


    def on_create(self):
        """
        Handle event when creating new log entry
        ========================================

        Raises
        ------
        LogosStatusError
            When the log entry is already created.
        """

        if super().is_ready():
            raise LogosStatusError('Cannot create a log entry twice.')
        self.__id_time = now()
        self.__id_user = CurrentUser.get_id()
        self.__access_mode = LogosPermissionTypes.READ.value + \
                             LogosPermissionTypes.WRITE.value
        super().on_update()


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
        check_data(data, ['id_time', 'id_user', 'access_mode', 'attributes',
                          'attachments', 'is_finished'])
        self.__id_time = data['id_time']
        self.__id_user = data['id_user']
        self.__access_mode = data['access_mode']
        self.__attributes = None # TODO Implement
        self.__attachments = None # TODO Implement
        self.__is_finished = data['is_finished']


    def to_json_dict(self) -> dict:
        """
        Abstract method to create a dict for creationg a JSON string from it
        ====================================================================

        Returns
        -------
        dict
            Dict to create a JSON formatted string.
        """

        return {'id_time' : self.id_tine, 'id_user' : self.id_user,
                'access_mode' : self.access_mode,
                'attributes' : self.attributes.to_json_dict(),
                'attachments' : self.attachments.to_json_dict(),
                'is_finished' : self.is_finished}
