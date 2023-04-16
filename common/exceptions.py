class DataPipelineException(Exception):
    """
    Data Pipeline base exception. Handled at the outermost level.
    All other exception types are subclasses of this exception type.
    """


class DataPipelineOperationalException(DataPipelineException):
    """
    Requires manual intervention and will stop the service..
    """
