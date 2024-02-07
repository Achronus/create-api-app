import os


class TestDirPaths:
    def __init__(self) -> None:
        self.static = 'public'
        self.project = 'app'

    def test_backend_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), 'backend')
        assert conf.DIRPATHS.BACKEND == path, f"Invalid: {path}"

    def test_project_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), 'backend', self.project)
        assert conf.DIRPATHS.APP == path, f"Invalid: {path}"

    def test_static_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, self.static)
        assert conf.DIRPATHS.PUBLIC == path, f"Invalid: {path}"
