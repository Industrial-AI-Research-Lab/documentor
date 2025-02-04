class Logger:
    def __init__(self):
        self._logs = {
            "info": [],
            "warning": [],
            "error": []
        }

    def add_info(self, message: str) -> None:
        self._logs["info"].append(message)

    def add_warning(self, message: str) -> None:
        self._logs["warning"].append(message)

    def add_error(self, message: str) -> None:
        self._logs["error"].append(message)

    def get_info_logs(self) -> list[str]:
        return self._logs["info"]

    def get_warning_logs(self) -> list[str]:
        return self._logs["warning"]

    def get_error_logs(self) -> list[str]:
        return self._logs["error"]

    def get_all_logs(self) -> dict[str, list[str]]:
        return self._logs
