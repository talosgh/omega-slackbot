import plugin_loader as plugin_loader
import fitz
import pandas as pd
from modules.logger import get_logger


class FileParser(plugin_loader.Parser):

    _alias_ = "FileParser"
    _version_ = "1.0"

    def __init__(self, **kwargs) -> None:
        self.logger = get_logger(self._alias_)
        self.logger.info(f"Initializing {self._alias_} - version {self._version_}")
        self.file = kwargs.get("file")
        pass

    def parse(self, **kwargs):
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
                        csv_filename = f"{self.file}_table_{page_num}_{table_index}.csv"
                        df.to_csv(csv_filename)
                        self.filenames.append(csv_filename)
                        text_content += "\n" + df.to_markdown(tablefmt="grid") + "\n\n"
                text_filename = f"{self.file}.txt"
                with open(text_filename, "w") as text_file:
                    text_file.write(text_content)
                self.filenames.append(text_filename)
        except Exception as e:
            self.logger.error(f"Error Parsing {self.file} - {e}")
            return {}
        self.logger.info(f"Successfully parsed {self.file}")
        return self.filenames
