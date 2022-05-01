class InputTooLittleError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)


class SegfaultError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)


class MarkersNotFoundError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)


class MarkersNotDefinedError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)


class ValueExtractionError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)


class InputNotVulnerableError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)


class NullByteInAddressError(Exception):
    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)
