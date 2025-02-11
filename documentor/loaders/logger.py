class LoaderLogger:
    # TODO add docstring and attribute descriptions
    def __init__(self):
        self._logs = {
            "info": [],
            "warning": [],
            "error": []
        }

    def add_info(self, message: str) -> None:
        # TODO add docstring
        self._logs["info"].append(message)

    def add_warning(self, message: str) -> None:
        # TODO add docstring
        self._logs["warning"].append(message)

    def add_error(self, message: str) -> None:
        # TODO add docstring
        self._logs["error"].append(message)

    def get_info_logs(self) -> list[str]:
        # TODO add docstring
        return self._logs["info"]

    def get_warning_logs(self) -> list[str]:
        # TODO add docstring
        return self._logs["warning"]

    def get_error_logs(self) -> list[str]:
        # TODO add docstring
        return self._logs["error"]

    def get_all_logs(self) -> dict[str, list[str]]:
        # TODO add docstring
        return self._logs
