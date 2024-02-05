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
        assert conf.DIRPATHS.STATIC == path, f"Invalid: {path}"
    
    def test_css_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static, 'css')
        assert conf.DIRPATHS.CSS == path, f"Invalid: {path}"

    def test_js_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static, 'js')
        assert conf.DIRPATHS.JS == path, f"Invalid: {path}"

    def test_imgs_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static, 'imgs')
        assert conf.DIRPATHS.IMGS == path, f"Invalid: {path}"

    def test_templates_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', 'templates')
        assert conf.DIRPATHS.TEMPLATES == path, f"Invalid: {path}"


class TestFilePaths:
    def __init__(self) -> None:
        self.static = 'public'
        self.project = '<REPLACE>'

    def test_input_css_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static, 'css', 'input.css')
        assert conf.FILEPATHS.INPUT_CSS == path, f"Invalid: {path}"

    def test_output_css_valid(self, conf) -> None:
        path = os.path.join(os.getcwd(), self.project, 'frontend', self.static, 'css', 'styles.min.css')
        assert conf.FILEPATHS.OUTPUT_CSS == path, f"Invalid: {path}"
