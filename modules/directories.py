from pathlib import Path
import sys


class Directories:
    def __init__(self, log, paths):
        self.log = log
        self.paths = paths
        self.run()

    def run(self):
        for p in self.paths:
            try:
                Path(p).mkdir(parents=True, exist_ok=True)
                self.log.info(f"Created input directory: {p}")
            except Exception as e:
                self.log.error(f"Error creating input directory: {e}")
                sys.exit()

        return None
