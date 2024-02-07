import os
import pytest


class TestLocalDotEnv:
    def test_backend_path_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), 'app', 'backend', '.env.local')
        assert conf.FILEPATHS.ENV_LOCAL == path, f'Invalid: {conf.FILEPATHS.ENV_LOCAL}'

    def test_data_valid(self, conf) -> None:
        assert conf.DB_URL is not None,  "'.env.local' appears to be missing!"


class TestProdDotEnv:
    def test_path_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), '.env.prod')
        assert conf.FILEPATHS.ENV_PROD == path, f'Invalid: {conf.FILEPATHS.ENV_PROD}'

    def test_data_valid(self, conf) -> None:
        assert conf.ENV_TYPE is not None, "'.env.prod' appears to be missing!"


class TestConf:
    def test_data_valid(self, conf) -> None:
        assert conf.PROJECT_NAME == 'app'


    def test_data_invalid(self, conf) -> None:
        with pytest.raises(AttributeError):
            _ = conf.DUMMY_VARIABLE
