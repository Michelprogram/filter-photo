class Utils:

    @staticmethod
    def get_file_size(file_path):
        """Get the size of file in MB"""
        size = os.path.getsize(file_path)
        return round(size / (1024 * 1024), 2)

    @staticmethod
    def get_information(file, path):
        """Return the name, extension and size of on file"""
        name = ''.join(str.split(file, '.')[:-1])
        extension = str.split(file, '.')[-1]
        size = Utils.get_file_size(path + "/" + file)

        return name, size, extension

    @staticmethod
    def get_path():
        """Ask path where to clean"""
        print('Path you would like to clear files :')
        x = input()
        return x.replace('\\', '/')


class File:

    name = ""
    size = 0
    extension = ""
    path = ""

    def __init__(self, name, size, extension, path) -> None:
        self.name = name
        self.size = size
        self.extension = extension
        self.path = path

    def __str__(self) -> str:
        return f"Name : {self.name} as a size of {self.size} MB with extension {self.extension}\n"
