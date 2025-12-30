"""Custom exceptions for the application."""


class ModelNotLoadedError(Exception):
    """Raised when a model is not loaded properly."""
    pass


class PredictionError(Exception):
    """Raised when a prediction fails."""
    pass


class InvalidInputError(Exception):
    """Raised when input validation fails."""
    pass
