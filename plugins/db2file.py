import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class DatabaseToFile(plugin_loader.Parser):
    _alias_ = "DatabaseToFile"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        """Retrieve file from database into tempfile
        Args:
            file_id (str): File ID
            db (obj): Database object
        """
        import tempfile

        db = kwargs.get("db")
        file_id = kwargs.get("file_id")

        query = "SELECT file FROM documents WHERE id = %d;"
        params = (file_id,)
        bytea_data, _ = db.execute_query(query, params)

        if bytea_data:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(bytea_data)
                self.logger.info(f"Data written to temporary file: {temp_file.name}")
                return temp_file.name
        return None
