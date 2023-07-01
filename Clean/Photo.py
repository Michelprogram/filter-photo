from Utils import Utils, File
import imagehash
from os import listdir, remove
from PIL import Image


class CleanPhoto:

    path = ""
    verbose = False
    accuracy = 0
    photos = []
    duplicates = []

    def __init__(self, verbose=False, accuracy=4) -> None:
        self.path = Utils.get_path()
        self.verbose = verbose
        self.photos = listdir(self.path)
        self.accuracy = accuracy

    def __str__(self):
        sentence = ""

        if self.verbose:
            for photo in self.duplicates:
                sentence += f"{photo}"

        sentence += f"You have {len(self.duplicates)} photos have duplicate that represent {round(self.__count_duplication_size(),2)} MB."

        return sentence

    def __count_duplication_size(self):
        total = 0

        for photo in self.duplicates:
            total += photo.size

        return total

    def __find_same_visual(self):

        data = {}

        for photo in self.photos:

            with Image.open(self.path + "/" + photo) as img:
                hash = imagehash.average_hash(img, self.accuracy * 2)

                if hash in data:
                    print(f"Find duplication of {data[hash]} by {photo}")
                    name, size, extension = Utils.get_information(
                        photo, self.path)

                    self.duplicates.append(
                        File(name, size, extension, self.path + "/" + photo))
                else:
                    data[hash] = photo

    def __remove_files(self):
        print(
            f"Would you like to remove {len(self.duplicates)} duplications files ? (y/n)")

        x = input()

        if x == 'y':
            for photo in self.duplicates:
                remove(photo.path)
            print(
                f"You have deleted {len(self.duplicates)} files, that represent {self.__count_duplication_size()} MB")
        else:
            print("Remove operation was canceled.")

    def clean(self):
        self.__find_same_visual()
        print(self)
        self.__remove_files()
