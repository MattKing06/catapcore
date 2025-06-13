class InvalidHardwareType(Exception):
    """
    Raise an exception when the hardware type is invalid
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class MachineAreaNotProvided(Exception):
    """
    Raise an exception when the machine area is not provided
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class MachineAreaNotFound(Exception):
    """
    Raise an exception when the machine area is not found
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class HardwareNameNotProvided(Exception):
    """
    Raise an exception when the hardware name is not provided
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class HardwareNameNotFound(Exception):
    """
    Raise an exception when the hardware name is not found
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class MissingConfigProperty(Exception):
    """
    Raise an exception when there is a missing property in the config file
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class UnexpectedPVEntry(UserWarning):
    """
    Raise an exception when an unexpected PV is found in the YAML file
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class FailedEPICSOperationWarning(UserWarning):
    """
    Raise a warning when an EPICS operation fails
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class EPICSOperationWarning(UserWarning):
    """
    Raise a warning regarding an EPICS command
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class EPICSOperationTimeoutWarning(UserWarning):
    """
    Raise a warning when an EPICS operation does not complete in time
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class InvalidSnapshotSetting(UserWarning):
    """
    Raise a warning when a snapshot is not valid
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message


class InvalidHardwareSubtype(UserWarning):
    """
    Raise a warning when the hardware subtype is invalid
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self):
        return self._message
