class LoaderLogger:
    """
    LoaderLogger is responsible for storing and managing logs at different severity levels (info, warning, error).

    Attributes:
        _logs (dict[str, list[str]]): A dictionary containing lists of log messages categorized by severity level.
    """
    def __init__(self):
        """
        Initialize the LoaderLogger instance with empty lists for info, warning, and error logs.
        """
        self._logs = {
            "info": [],
            "warning": [],
            "error": []
        }

    def add_info(self, message: str) -> None:
        """
        Add an informational log message.

        Args:
            message (str): The log message to add to the info logs.
        """
        self._logs["info"].append(message)

    def add_warning(self, message: str) -> None:
        """
        Add a warning log message.

        Args:
            message (str): The log message to add to the warning logs.
        """
        self._logs["warning"].append(message)

    def add_error(self, message: str) -> None:
        """
        Add an error log message.

        Args:
            message (str): The log message to add to the error logs.
        """
        self._logs["error"].append(message)

    def get_info_logs(self) -> list[str]:
        """
        Return all informational log messages.

        Returns:
            list[str]: A list containing all info log messages.
        """
        return self._logs["info"]

    def get_warning_logs(self) -> list[str]:
        """
        Return all warning log messages.

        Returns:
            list[str]: A list containing all warning log messages.
        """
        return self._logs["warning"]

    def get_error_logs(self) -> list[str]:
        """
        Return all error log messages.

        Returns:
            list[str]: A list containing all error log messages.
        """
        return self._logs["error"]

    def get_all_logs(self) -> dict[str, list[str]]:
        """
        Return all log messages of all severities.

        Returns:
            dict[str, list[str]]: A dictionary of message lists keyed by severity level.
        """
        return self._logs
