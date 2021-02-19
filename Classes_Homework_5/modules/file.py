from os.path import dirname, join


class Files:
    def get_path(self, file_name):
        """Generate path to the target file (file name is configurable).
        Will write file to the grand-parent directory of this module
        """
        folder = dirname(dirname(__file__).replace('/', '\\'))
        file_path = join(folder, file_name)
        return file_path

    def write_file(self, text, file_name):
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
