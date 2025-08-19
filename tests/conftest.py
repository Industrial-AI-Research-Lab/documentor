from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def data_dir(pytestconfig) -> Path:
    """
    Абсолютный путь к tests/data вне зависимости от того,
    из какого места запущен pytest.
    """
    path = Path(pytestconfig.rootdir, "tests", "data").resolve()
    return path
