"""
Custom exceptions used across the project.
"""


class ApplicationError(Exception):
    """
    Base exception for the application.
    """
    pass


class S3ObjectNotFoundError(ApplicationError):
    """
    Raised when an S3 object is not found.
    """
    pass


class DynamoDBItemNotFoundError(ApplicationError):
    """
    Raised when an item is not found in DynamoDB.
    """
    pass


class InvalidFileTypeError(ApplicationError):
    """
    Raised when an unsupported file type is uploaded.
    """
    pass


class InvalidFileSizeError(ApplicationError):
    """
    Raised when file size cannot be processed.
    """
    pass


class GlueJobSelectionError(ApplicationError):
    """
    Raised when no Glue Job mapping is found.
    """
    pass


class GlueJobStartError(ApplicationError):
    """
    Raised when a Glue Job fails to start.
    """
    pass


class GlueJobFailureError(ApplicationError):
    """
    Raised when a Glue Job execution fails.
    """
    pass


class CrawlerStartError(ApplicationError):
    """
    Raised when a crawler cannot be started.
    """
    pass


class CrawlerTimeoutError(ApplicationError):
    """
    Raised when crawler does not finish within timeout.
    """
    pass


class AthenaQueryError(ApplicationError):
    """
    Raised when Athena query execution fails.
    """
    pass


class AthenaQueryTimeoutError(ApplicationError):
    """
    Raised when Athena query exceeds timeout.
    """
    pass


class SNSPublishError(ApplicationError):
    """
    Raised when SNS message publication fails.
    """
    pass


class ConfigurationError(ApplicationError):
    """
    Raised when required configuration is missing.
    """
    pass


class ValidationError(ApplicationError):
    """
    Raised when input validation fails.
    """
    pass