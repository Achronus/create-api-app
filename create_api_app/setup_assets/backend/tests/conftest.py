import pytest

from app.config.settings import settings


@pytest.fixture
def conf() -> settings:
    return settings
