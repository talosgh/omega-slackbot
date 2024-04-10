import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class Zipper(plugin_loader.Parser):
    _alias_ = "Zipper"
    _version_ = "1.3"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        """
        Create a ZIP archive of the given files in a temporary location.
        Args:
            filenames (list): List of filenames to include in the zip.
            temp_dir (str): Path to the temporary directory containing the files.
            download_filename (str, optional): An additional file to include in the zip.
            username (str): Username to prefix the zip filename.
        Returns:
            str: Path to the created ZIP file.
        """

        import os
        from zipfile import ZipFile
        import tempfile
        from pathlib import Path
        import shutil

        filenames = kwargs.get("filenames")
        temp_dir = kwargs.get("temp_dir")
        download_filename = kwargs.get("download_filename", "")
        username = kwargs.get("username")

        if not filenames:
            self.logger.error("No filenames provided to the zipper.")
            return None

        filenames = kwargs.get("filenames", [])
        temp_dir = kwargs.get("temp_dir", "")
        download_filename = kwargs.get("download_filename", "")
        username = kwargs.get("username", "")

        filestem = "archive"  # Default archive name if not specified

        if download_filename:
            filestem = download_filename.split("/")[-1]
        temp_zip_path = tempfile.mktemp(prefix=f"{username}-{filestem}-", suffix=".zip")

        with ZipFile(temp_zip_path, "w") as zipf:
            for filename in filenames:
                # Construct full path to file
                full_path = os.path.join(temp_dir, filename)
                if os.path.exists(full_path):
                    zipf.write(full_path, arcname=os.path.basename(filename))
                else:
                    self.logger.warning(
                        f"File {filename} not found in temporary directory."
                    )

            if download_filename and os.path.exists(download_filename):
                zipf.write(
                    download_filename, arcname=os.path.basename(download_filename)
                )

        # Cleanup the temporary directory after zipping its contents
        shutil.rmtree(temp_dir, ignore_errors=True)

        self.logger.info(f"Files zipped: {temp_zip_path}")
        return temp_zip_path
