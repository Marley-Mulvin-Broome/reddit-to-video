class CommentTooBigError(Exception):
    """Raised when a comment is too big to be added to a video"""
    pass


class NotInCollectionError(Exception):
    """Raised when an item is not found in a collection"""
    pass
