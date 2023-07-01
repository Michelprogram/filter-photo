from Utils import Utils, File
from os import listdir, remove
from collections import defaultdict
from re import sub


class CleanFiles:

    path = ""
    verbose = False
    files = []
    duplicated = {}

    def __init__(self, verbose=False) -> None:
        self.path = Utils.get_path()
        self.verbose = verbose
        self.files = listdir(self.path)
        self.duplicated = {}

    def __remove_dump_name_duplicate(self, name):
        """Clean name of duplicated file ex : IMG_9982 (1) -> IMG_9982"""
        return sub(r" \(\d\)", '', name)

    def __find_duplicate_file_by_name(self):
        """Looking in directory if files have same name"""
        data = defaultdict(list)

        for file in self.files:

            name, size, extension = Utils.get_information(file, self.path)

            if name != "":
                clean_name = self.__remove_dump_name_duplicate(name)

                data[clean_name].append(
                    File(name, size, extension, self.path + "/" + file))

        return {k: v for k, v in data.items() if len(v) > 1}

    def __str__(self):
        """Print some informations about how much duplications"""

        sentence = ""

        if self.verbose:
            for clean_name, v in self.duplicated.items():
                sentence += f"File {clean_name} have {len(v)} duplications\n"
                for file in v:
                    sentence += f"{file}\n"

        sentence += f"You have {len(self.duplicated.keys())} files with duplications, that represent total of {self.__count_duplication()}\n"

        return sentence

    def __count_duplication(self):
        """Count duplication in total"""
        counter = 0

        for _, v in self.duplicated.items():
            counter += len(v)-1

        return counter

    def __find_fake_duplicate(self):
        """Looking for file with same name but different in size"""
        for clean_name, v in self.duplicated.items():
            base = v[0].size
            counter = 0
            for file in v:
                if file.size != base:
                    print(
                        f"File {clean_name} it's a fake duplication of {file.name}")

                    counter += 1
                    new_name = f"{self.path}/{file.name}_{counter}.{file.extension}"
                    os.rename(file.path, new_name)

                    print(f"Rename of {file.path} to {new_name}")

    def __remove_files(self):
        """Remove duplicated files"""

        print(
            f"Would you like to remove {self.__count_duplication()} duplications files ? (y/n)")

        x = input()
        total = 0
        counter = 0

        if x == 'y':
            for _, v in self.duplicated.items():
                for i in range(0, len(v)-1):
                    os.remove(v[i].path)
                    total += v[i].size
                    counter += 1
            print(
                f"You have deleted {counter} files, that represent {total} MB")
        else:
            print("Remove operation was canceled.")

    def clean(self):

        self.duplicated = self.__find_duplicate_file_by_name()

        if len(self.duplicated) == 0:
            print("There are nothing to clean.")
        else:
            print(self)

            self.__find_fake_duplicate()
            self.duplicated = self.__find_duplicate_file_by_name()

            self.__remove_files()
