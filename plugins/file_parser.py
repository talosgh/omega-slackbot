import modules.plugin_loader as plugin_loader
from modules.logger import get_logger


class FileParser(plugin_loader.Parser):

    _alias_ = "FileParser"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        """
        Initialize the FileParser class
        :param kwargs: file: path of file to parse"""

        self.logger = get_logger(self._alias_)
        pass

    def parse(self, **kwargs):
        """
        Parse the file and return the parsed content
        :param kwargs: path: output path
        :param kwargs: file: file to parse
        :return: filenames: list of filenames created during parsing
        """
        import fitz
        import pandas as pd
        import os

        path = kwargs.get("path")
        file = kwargs.get("file")
        stem = os.path.splitext(file)[0]
        output_path = os.path.join(path, stem)

        self.filenames = []
        try:
            with fitz.open(f"{self.file}") as doc:
                text_content = ""
                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text("text", flags=34)
                    text_content += text

                    tables = page.find_tables() if hasattr(page, "find_tables") else []
                    for table_index, table in enumerate(tables, start=1):
                        df = pd.DataFrame()
                        df = table.to_pandas()
                        csv_filename = (
                            f"{output_path}_table_{page_num}_{table_index}.csv"
                        )
                        df.to_csv(csv_filename)
                        self.filenames.append(csv_filename)
                        text_content += "\n" + df.to_markdown(tablefmt="grid") + "\n\n"
                    text_filename = f"{output_path}.txt"
                with open(text_filename, "w") as text_file:
                    text_file.write(text_content)
                self.filenames.append(text_filename)
        except Exception as e:
            self.logger.error(f"Error Parsing {self.file} - {e}")
            return {}
        self.logger.info(f"Successfully parsed {self.file}")
        return self.filenames
