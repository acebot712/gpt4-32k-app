import os
import logging

class PythonFileReader:
    def __init__(self, path='.'):
        self.path = path
        self.logger = logging.getLogger(__name__)

    def get_files_content(self):
        contents = []
        try:
            for file in os.listdir(self.path):
                if file.endswith('.py'):
                    with open(os.path.join(self.path, file), 'r') as f:
                        contents.append(f"# {file}\n{f.read()}")
        except Exception as e:
            self.logger.error(f'Error occurred while reading the files. Reason: {e}')
        return contents
    