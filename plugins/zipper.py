import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class Zipper(plugin_loader.Parser):
    _alias_ = "Zipper"
    _version_ = "1.3"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        import zipfile
        import os
        from zipfile import ZipFile
        from pathlib import Path

        documents_directory = kwargs.get("temp_dir")
        filenames = kwargs.get("filenames", None)
        download_filename = kwargs.get("download_filename", None)
        user = kwargs.get("username", "")

        filestem = Path(download_filename).stem

        if not filenames:
            return

        zipfile = documents_directory + "/" + user + "-" + filestem + ".zip"
        with ZipFile(zipfile, "w") as zip:
            for filename in filenames:
                zip.write(filename, arcname=os.path.basename(filename))
                os.remove(filename)
            if download_filename:
                zip.write(
                    download_filename,
                    arcname=os.path.basename(download_filename),
                )
                os.remove(download_filename)
        self.logger.info(f"Files zipped: {zipfile}")
        return zipfile
