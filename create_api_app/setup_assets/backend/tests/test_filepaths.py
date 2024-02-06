import os


class TestDirPaths:
    def __init__(self) -> None:
        self.static = 'public'
        self.project = '<REPLACE>'
    
    def test_frontend_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend')
        assert conf.DIRPATHS.FRONTEND == path, f"Invalid: {path}"

    def test_backend_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'backend')
        assert conf.DIRPATHS.BACKEND == path, f"Invalid: {path}"

    def test_static_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static)
        assert conf.DIRPATHS.PUBLIC == path, f"Invalid: {path}"
    
    def test_css_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static, 'styles')
        assert conf.DIRPATHS.STYLES == path, f"Invalid: {path}"

