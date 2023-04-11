class ScriptElementTooLongError(Exception):
    """Raised when a ScriptElement's duration is too long to be added to a VideoScript object"""
    pass


class NotInCollectionError(Exception):
    """Raised when an item is not found in a collection"""
    pass


class NoAudioError(Exception):
    """Raised when a script element has no audio but is not a video"""
    pass


class EmptyCollectionError(Exception):
    """Raised when a collection is empty"""
    pass


class OutputPathValidationError(Exception):
    """Raised when an output path is not valid"""
    pass


class OsNotSupportedError(Exception):
    """Raised when the OS is not supported"""
    pass

class ConfigKeyError(Exception):
    """Raised when a config key is not found"""
    pass

class DirectoryNotFoundError(Exception):
    """Raised when a directory is not found"""
    pass