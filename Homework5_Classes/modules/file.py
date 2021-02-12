import os


class Files:
    def __init__(self, target_file):
        self.target_file = target_file

    def get_path(self):
        """Generates path to the target file (file name is configurable).
        Will write file to current working directory"""
        target_path = os.path.join(os.getcwd())+'\\'+self.target_file
        return target_path

    def write_file(self, text):
        """Opens target file.
        If there are already records - add new section aftecr 2 newlines,
        if no - add at the beginning of the file
        """
        path = self.get_path()
        with open(path, "a+") as target_file:
            target_file.seek(0)
            data = target_file.read(100)
            if len(data) > 0:
                target_file.write("\n\n")
            target_file.write(text)
