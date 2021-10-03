"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: attributes
"""


from enum import Enum

from datamodel import LogosLocallyCangeable, LogosUpdateable
from datamodel import LogosUpdateableSingleton
from error import LogosPermissionError
from functiontools import check_data
from texts import Texts


class AttributeObjectLevels(Enum):
    """
    Provide attribute hierarchy level constants
    ===========================================
    """

    CHANNEL = 1
    LOG = 2
    LOG_ENTRY = 3
    USER = 8


class Tags(LogosUpdateableSingleton):
    """
    Singleton to provide available tags and tag texts
    =================================================
    """

    __tag_ids = []


    @classmethod
    def available(cls, tag_id : int) -> bool:
        """
        Check whether tag ID is available
        =================================

        Parameters
        ----------
        tag_id : int
            The ID to check.
        """

        return tag_id in cls.__tag_ids


    @classmethod
    def get(cls, tag_id : int) -> str:
        """
        Get tag text
        ============

        Parameters
        ----------
        tag_id : int
            ID of the tag to get.

        Returns
        -------
        str
            Text of the tag.

        Raises
        ------
        LogosPermissionError
            When the given tag ID is not accessible.

        Notes
        -----
            To avoid exceptions use Tags.available(tag_id) or
            Tags.get_all_ids().
        """

        if not cls.available(tag_id):
            raise LogosPermissionError('Tag #{} is not accessible.'
                                       .format(tag_id))
        return Texts.get('#{}'.format(tag_id))


    @classmethod
    def get_all_ids(cls) -> list:
        """
        Get all available tag IDs
        =========================

        Returns
        -------
        list(int)
            List of available tag IDs.
        """

        return cls.__tag_ids.copy()


    @classmethod
    def get_all_tags_with_id(cls) -> list:
        """
        Get all available tag texts with the corresponding id
        =====================================================

        Returns
        -------
        list(dict( id : int, text : str))
            List of available tags with text and id.
        """

        return [{'id' : tag_id, 'text' : Texts.get('#{}'.format(tag_id))}
                for tag_id in cls.__tag_ids]


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

        return all([super().is_ready(), Texts.is_ready()])


    @classmethod
    def on_data_received(cls, data : list, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : list(int)
            Data to set as new tag IDs.
        version : int
            Version to set as new version.
        """

        super().on_data_received(data, version)
        cls.__tag_ids = data.copy()


class Descriptions(LogosUpdateableSingleton):
    """
    Singleton to provide available description keys, values and their texts
    =======================================================================
    """


    __description_structure = {}


    @classmethod
    def available_key(cls, key : int) -> bool:
        """
        Check whether description key is available
        ==========================================

        Parameters
        ----------
        key : int
            Description key to check.

        Returns
        -------
        bool
            True if description_key is available, False if not.
        """

        return key in cls.__description_structure.keys()


    @classmethod
    def available_value(cls, key : int, value : int) -> bool:
        """
        Check whether description key is available
        ==========================================

        Parameters
        ----------
        key : int
            Description key to check in.
        value : int
            Description value to check for.

        Returns
        -------
        bool
            True if value is available in the description_key , False if not.

        Raises
        ------
        LogosPermissionError
            When desciption key is nat accessible.

        Notes
        -----
            To avoid exceptions use Descriptions.available_key(key).
        """

        if not cls.available_key(key):
            raise LogosPermissionError('Description key #{} is not accessible.'
                                       .format(key))
        return value in cls.__description_structure[key]


    @classmethod
    def get(cls, key : int, value : int) -> dict:
        """
        Get desciption key's and value's texts
        ======================================

        Parameters
        ----------
        key : int
            Key to get.
        value : int
            Value to get.

        Returns
        -------
        dict(desciption : str, value : str)
            Texts of desciption key and value.

        Raises
        ------
        LogosPermissionError
            When the given description_key and value is not accessible.

        Notes
        -----
            To avoud exceptions use
            Descriptions.available_value(description_key, value).
        """

        if not cls.available_value(key, value):
            raise LogosPermissionError('Description value #{} is not '.format(
                                       value) + 'accessible at key #{}.'
                                       .format(key))
        return {'description' : Tags.get(key),
                'value' : Tags.get(value)}


    @classmethod
    def get_all_key_ids(cls) -> list:
        """
        Get all available key IDs
        =========================

        Returns
        -------
        list(int)
            List of available desciption key IDs.
        """

        return list(cls.__description_structure.keys())


    @classmethod
    def get_all_keys_with_id(cls) -> list:
        """
        Get all available description key texts with the corresponding ID
        =================================================================

        Returns
        -------
        list(dict(description_key : int, text : str))
            List of available desciption key IDs.
        """

        return [{'id' : key, 'text' : Tags.get(key)}
                for key in cls.__description_structure.keys()]


    @classmethod
    def get_all_value_ids(cls, key : int) -> list:
        """
        Get all available value IDs for a key
        =====================================

        Parameters
        ----------
        key : int
            Key to search for.

        Returns
        -------
        list(int)
            List of available desciption key IDs.

        Raises
        ------
        LogosPermissionError
            When desciption key is nat accessible.

        Notes
        -----
            To avoid exceptions use Descriptions.available_key(key).
        """

        if not cls.available_key(key):
            raise LogosPermissionError('Description key #{} is not accessible.'
                                       .format(key))
        return cls.__description_structure[key].copy()


    @classmethod
    def get_all_values_with_id(cls, key : int) -> list:
        """
        Get all available value texts and IDs for a key
        ===============================================

        Parameters
        ----------
        key : int
            Key to search for.

        Returns
        -------
        list(dict(key : int, text : str))
            List of available desciption key IDs.

        Raises
        ------
        LogosPermissionError
            When desciption key is nat accessible.

        Notes
        -----
            To avoid exceptions use Descriptions.available_key(key).
        """

        if not cls.available_key(key):
            raise LogosPermissionError('Description key #{} is not accessible.'
                                       .format(key))
        return [{'id' : value, 'text' : Tags.get(value)}
                for value in cls.__description_structure[key]]


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

        return all([super().is_ready(), Tags.is_ready()])


    @classmethod
    def on_data_received(cls, data : list, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : list(int)
            Data to set as new tag IDs.
        version : int
            Version to set as new version.
        """

        super().on_data_received(data, version)
        cls.__description_structure = data.copy()


class LogosAttributes(LogosUpdateable):
    """
    Provide updateable read-only attributes handling
    ================================================
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
        self.__tags = []
        self.__descriptions = {}
        if data is not None:
            self.on_data_received(data, version)


    @property
    def descriptions(self) -> dict:
        """
        Get descriptions
        ================

        Returns
        -------
        dict(int : int)
            Dict of description keys and values.
        """

        self.__descriptions.copy()


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
        check_data(data, ['tags', 'descriptions'])
        self.__tags = data['tags'].copy()
        self.__descriptions = data['descriptions'].copy()


    @property
    def tags(self) -> list:
        """
        Get list of tags
        ================

        Returns
        -------
        list(int)
            List of tag IDs.
        """

        return self.__tags.copy()


class LogosEditableAttributes(LogosLocallyCangeable):
    """
    Provide updateable and editable attributes handling
    ==================================================
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
        self.__tags = []
        self.__descriptions = {}
        if data is not None:
            self.on_data_received(data, version)


    def add_description(self, new_key : int, new_value : int):
        """
        Add desciption
        ==============

        Parameters
        ----------
        new_key : int
            Key to create.
        new_value : int
            Value to set for the key.

        Raises
        ------
        ValueError
            When the given desciption key is already added.
        LogosPermissionError
            When the given desciption key is not accessible.
        LogosPermissionError
            When the given desciption value is not accessible.
        """

        if new_key in self.__descriptions.keys():
            raise ValueError('Description key already exists.')
        if not Descriptions.available_key(new_key):
            raise LogosPermissionError('Description key is not accessible.')
        if not Descriptions.available_value(new_key, new_value):
            raise LogosPermissionError('Description value for this key is not ' +
                                       'accessible.')
        self.__descriptions[new_key] = new_value
        super().om_update()


    def add_tag(self, new_tag : int):
        """
        Add tag
        =======

        Parameters
        ----------
        new_tag : int
            Tag to add.

        Raises
        ------
        ValueError
            When the given tag ID is already added.
        LogosPermissionError
            When the given tag ID is not accessible.
        """

        if new_tag in self.__tags:
            raise ValueError('Tag ID already exists.')
        if not Tags.available(new_tag):
            raise LogosPermissionError('Tag ID is not accessible.')
        self.__tags.append(new_tag)
        super().om_update()


    def change_description(self, key : int, new_value : int):
        """
        Add desciption
        ==============

        Parameters
        ----------
        key : int
            Key to change.
        new_value : int
            Value to change the key too.

        Raises
        ------
        ValueError
            When the given desciption key doesn't exist.
        LogosPermissionError
            When the given desciption key is not accessible.
        LogosPermissionError
            When the given desciption value is not accessible.
        """

        if key not in self.__descriptions.keys():
            raise ValueError('Description key not exists.')
        if not Descriptions.available_key(key):
            raise LogosPermissionError('Description key is not accessible.')
        if not Descriptions.available_value(key, new_value):
            raise LogosPermissionError('Description value for this key is not ' +
                                       'accessible.')
        self.__descriptions[key] = new_value
        super().om_update()


    def change_tag(self, original_tag : int, new_tag : int):
        """
        Change tag
        ==========

        Parameters
        ----------
        original_tag : int
            Tag to change.
        new_tag : int
            Tag to change to.

        Raises
        ------
        ValueError
            When the given tag ID deosn't exist.
        LogosPermissionError
            When the given tag ID is not accessible.
        """

        pos = -1
        for i, _id in enumerate(self.__tags):
            if _id == original_tag:
                pos = i
        if pos < 0 in self.__tags:
            raise ValueError('Tag ID doesn\'t exist.')
        if not Tags.available(new_tag):
            raise LogosPermissionError('Tag ID is not accessible.')
        self.__tags[pos] = new_tag
        super().om_update()


    def delete_description(self, key : int):
        """
        Delete desciption
        =================

        Parameters
        ----------
        key : int
            Key to delete.

        Raises
        ------
        ValueError
            When the given desciption key doesn't exist.
        """

        if key not in self.__descriptions.keys():
            raise ValueError('Description key not exists.')
        result = {}
        for _key, _value in self.__descriptions.items():
            if key != _key:
                result[_key] = _value
        self.__descriptions = result.copy()
        super().om_update()


    def delete_tag(self, tag_id : int):
        """
        Delete tag
        ==========

        Parameters
        ----------
        tag_id : int
            Tag ID to delete.

        Raises
        ------
        ValueError
            When the given tag ID deosn't exist.
        """

        if tag_id not in self.__tags:
            raise ValueError('Tag ID doesn\'t exist.')
        result = []
        for _tag_id in self.__tags:
            if tag_id != _tag_id:
                result.append(_tag_id)
        self.__tags = result.copy()
        super().om_update()


    @property
    def descriptions(self) -> dict:
        """
        Get descriptions
        ================

        Returns
        -------
        dict(int : int)
            Dict of description keys and values.
        """

        self.__descriptions.copy()


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
        check_data(data, ['tags', 'descriptions'])
        self.__tags = data['tags'].copy()
        self.__descriptions = data['descriptions'].copy()


    @property
    def tags(self) -> list:
        """
        Get list of tags
        ================

        Returns
        -------
        list(int)
            List of tag IDs.
        """

        return self.__tags.copy()


    def to_json_dict(self) -> dict:
        """
        Create a dict for creationg a JSON string from it
        =================================================

        Returns
        -------
        dict
            Dict to create a JSON formatted string.
        """

        return {'tags' : self.__tags.copy(),
                'descriptions' : self.__descriptions.copy()}
