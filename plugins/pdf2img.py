import modules.plugin_loader as plugin_loader
from modules.logger import get_logger
from pdf2image import convert_from_path
import tempfile


class Pdf2Img(plugin_loader.Parser):
    _alias_ = "pdf2img"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.paths = kwargs.get("paths", ["Documents", "Downloads"])

    def parse(self, **kwargs):
        file = kwargs.get("file")

        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "/home/belval/example.pdf", output_folder=path
            )
