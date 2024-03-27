import modules.plugin_loader as plugin_loader
from pathlib import Path
from modules.logger import get_logger


class Directories(plugin_loader.Parser):
    _alias_ = "Directory"
    _version_ = "1.2"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.paths = kwargs.get("paths", ["Documents", "Downloads"])

    def parse(self, **kwargs):
        self.logger.info(f"Creating Directories if they don't exist")
        for path in self.paths:
            directory = Path(path)
            try:
                if not directory.exists():
                    directory.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created directory: {path}")
                else:
                    self.logger.info(f"Directory already exists: {path}")
            except Exception as e:
                self.log.error(f"Error creating directory '{path}': {e}")
                raise RuntimeError(f"Failed to create directory '{path}': {e}") from e
