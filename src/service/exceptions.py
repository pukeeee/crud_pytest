class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    pass

class EmailAlreadyExistsError(Exception):
    """Raised when trying to create a user with an email that already exists."""
    pass

class ForbiddenError(Exception):
    """Raised when a user tries to access a resource they don't have permission for."""
    pass

class NothingToUpdateError(Exception):
    """Raised when an update is requested with no data."""
    pass

class InternalError(Exception):
    pass