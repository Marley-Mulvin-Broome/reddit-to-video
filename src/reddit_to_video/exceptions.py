class ScriptElementTooLongError(Exception):
    """Raised when a ScriptElement's duration is too long to be added to a VideoScript object"""


class NotInCollectionError(Exception):
    """Raised when an item is not found in a collection"""


class NoAudioError(Exception):
    """Raised when a script element has no audio but is not a video"""


class EmptyCollectionError(Exception):
    """Raised when a collection is empty"""


class OutputPathValidationError(Exception):
    """Raised when an output path is not valid"""

class OsNotSupportedError(Exception):
    """Raised when the OS is not supported"""

class ConfigKeyError(Exception):
    """Raised when a config key is not found"""

class DirectoryNotFoundError(Exception):
    """Raised when a directory is not found"""
