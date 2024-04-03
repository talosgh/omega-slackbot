import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class FileToDatabase(plugin_loader.Parser):
    _alias_ = "FileToDatabase"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)

    def parse(self, **kwargs):
        """Save file to database
        Args:
            file (str): File path
            db (obj): Database object
        """
        import hashlib
        import os
        import magic
        from datetime import datetime

        filepath = kwargs.get("file")
        db = kwargs.get("db")
        try:
            with open(filepath, "rb") as f:
                file_content = f.read()
                filehash = hashlib.sha256(file_content).hexdigest()
                filename = os.path.basename(filepath)
                mimetype = magic.from_buffer(file_content, mime=True)
                filesize = os.stat(filepath).st_size
                self.logger.info(f"Attempting to save file {filename} to database")

                # Part 1: Try to insert the file information
                insert_query = """INSERT INTO documents
                    (file, filename, filesize, mimetype, filehash, timestamp) 
                    VALUES (%s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (filehash) DO NOTHING;"""
                params = (
                    file_content,
                    filename,
                    filesize,
                    mimetype,
                    filehash,
                    datetime.now(),
                )
                db.execute_query(insert_query, params)

                # Part 2: Retrieve the id for the entry with the given filehash
                select_query = "SELECT id FROM documents WHERE filehash = %s;"
                document_id = db.execute_query(
                    select_query,
                    [
                        filehash,
                    ],
                )
                # Assuming execute_query() method is adjusted to return single value correctly
                if document_id:
                    document_id = document_id[0][0]
                    self.logger.info(
                        f"{filename} is in the database with id {document_id}."
                    )
                    return document_id
                else:
                    self.logger.error(
                        f"Failed to retrieve document id for filehash {filehash}."
                    )
                    return None
        except Exception as e:
            self.logger.error(f"Error processing the file: {e}")
            return None
