from os.path import dirname, join, normcase
from exec_utils.configloader import Config

cnf = Config()


class Files:
    def get_path(self, file_name):
        """Generate path to /files directory. 'files' folder name is configurable"""
        parent_folder = normcase(dirname(dirname(__file__))) # parent package path
        new_folder = cnf.get_values("PATHS", "files_folder")
        file_path = join(parent_folder, new_folder, file_name)
        return file_path

    def append_file(self, text, file_name):
        """Open target file.
        If there are already records - add new section after 2 newlines,
        if no - add at the beginning of the file
        """
        target_path = self.get_path(file_name)
        with open(target_path, "a+", encoding="utf-8") as target_file:
            target_file.seek(0)
            data = target_file.read(100)
            if len(data) > 0:
                target_file.write("\n\n")
            target_file.write(text)
