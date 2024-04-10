import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class FileParser(plugin_loader.Parser):

    _alias_ = "FileParser"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        pass

    def parse(self, **kwargs):
        """
        Parse the file and return the parsed content using temporary files.
        :param kwargs: file: file to parse
        :return: filenames: list of filenames created during parsing
        """

        import fitz  # PyMuPDF
        import pandas as pd
        import tempfile
        import os
        import shutil

        file = kwargs.get("file")

        self.filenames = []
        temp_dir = tempfile.mkdtemp()
        try:
            with fitz.open(file) as doc:
                text_content = ""
                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text("text", flags=34)
                    text_content += text

                    tables = page.find_tables() if hasattr(page, "find_tables") else []
                    for table_index, table in enumerate(tables, start=1):
                        df = pd.DataFrame()
                        df = table.to_pandas()
                        # Creating a temporary file for each table CSV
                        temp_csv_file = os.path.join(
                            temp_dir, f"table_{page_num}_{table_index}.csv"
                        )
                        df.to_csv(temp_csv_file)
                        self.filenames.append(temp_csv_file)
                        text_content += "\n" + df.to_markdown(tablefmt="grid") + "\n\n"

                # Creating a temporary file for text content
                text_filename = os.path.join(temp_dir, "parsed_content.md")
                with open(text_filename, "w") as text_file:
                    text_file.write(text_content)
                self.filenames.append(text_filename)

        except Exception as e:
            self.logger.error(f"Error Parsing {file} - {e}")
            shutil.rmtree(temp_dir)
            return []

        self.logger.info(f"Successfully parsed {file}")
        return self.filenames, temp_dir
