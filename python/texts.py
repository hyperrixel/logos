"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: texts
"""


from datamodel import LogosUpdateableSingleton


class Texts(LogosUpdateableSingleton):
    """
    Singleton to handle texts
    =========================
    """

    __DEFAULT_LANGUAGE = 'en'

    __content = {}
    __default_value = ''
    __language = 'en'


    @classmethod
    def exists(cls, key : str, language : str = '',
               strict : bool = False) -> bool:
        """
        Get whether a key exist
        =======================

        Parameters
        ----------
        key : str
            Key of the string to search.
        language : str, optional (Empty string if omitted)
            Language to use on search. If empty string is given, the session
            language is used.
        strict : bool, optional (False if omitted)
            Whether to aply strict search or not.

        Returns
        -------
        bool
            True if the key exists, False if not. In case of strict search only
            the given (or session) language is applied, in case of non-strict
            search both the given (or session) and the default language is
            applied.
        """

        result = False
        if language == '':
            language = cls.__language
        if strict:
            if language in cls.__content.keys():
                result = key in cls.__content[language].keys()
        else:
            if language in cls.__content.keys():
                result = key in cls.__content[language].keys()
            elif cls.__DEFAULT_LANGUAGE in cls.__content.keys():
                result = key in cls.__content[cls.__DEFAULT_LANGUAGE].keys()
        return result


    @classmethod
    def get(cls, key : str, language : str = '') -> str:
        """
        Get text
        ========

        Parameters
        ----------
        key : str
            Key of the string to get.
        language : str, optional (Empty string if omitted)
            Language to use on get. If empty string is given, the session
            language is used.

        Returns
        -------
        str
            If the key exists in the given (or session) language, the value
            gets returned, If the key exists in the default language (en),
            this value gets returned, if the key doesn't exist, the default
            value is returned.
        """

        result = cls.__default_value
        if language == '':
            language = cls.__language
        if language in cls.__content.keys():
            if key in cls.__content[language].keys():
                result = cls.__content[language][key]
        elif cls.__DEFAULT_LANGUAGE in cls.__content.keys():
            if key in cls.__content[cls.__DEFAULT_LANGUAGE].keys():
                result = cls.__content[cls.__DEFAULT_LANGUAGE][key]
        return result


    @classmethod
    def get_default_value(cls) -> str:
        """
        Get default text value
        ======================

        Returns
        -------
        str
            Default text value.
        """

        return cls.__default_value


    @classmethod
    def get_language(cls) -> str:
        """
        Get session language
        ====================

        Returns
        -------
        str
            Default session language.
        """

        return cls.__language


    @classmethod
    def on_data_received(cls, data : dict, version : int):
        """
        Handle event when new data is received
        ======================================

        Parameters
        ----------
        data : dict
            Data to set as new text data.
        version : int
            Version to set as new version.
        """

        super().on_data_received(data, version)
        cls.__content = data.copy()


    @classmethod
    def set_default_value(cls, new_value : str):
        """
        Set default text value
        ======================

        Parameters
        ----------
        new_value : str
            The new default text value.
        """

        cls.__default_value = new_value


    @classmethod
    def set_language(cls, new_value : str):
        """
        Set session language
        ====================

        Parameters
        ----------
        new_value : str
            The new default session language.
        """

        cls.__language = new_value
