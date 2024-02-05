import pytest

from ..config.settings import settings


@pytest.fixture
def conf() -> settings:
    return settings
