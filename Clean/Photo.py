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
    data = {}

    def __init__(self, verbose=False, accuracy=4) -> None:
        self.path = Utils.get_path()
        self.verbose = verbose
        self.photos = listdir(self.path)
        self.accuracy = accuracy
        self.data = {}

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

    def __find_same_visual_recursive(self, path):

        for photo in listdir(path):

            photo_path = path + "/" + photo

            if (Utils.is_directory(photo_path)):
                self.__find_same_visual_recursive(photo_path)
                continue

            if not photo.lower().endswith(('.jpg', '.png', '.jpeg', '.heic')):
                continue

            with Image.open(photo_path) as img:
                hash = imagehash.average_hash(img, self.accuracy * 2)

                if hash in self.data:
                    print(f"Find duplication of {self.data[hash]} by {photo}")
                    name, size, extension = Utils.get_information(
                        photo, self.path)

                    self.duplicates.append(
                        File(name, size, extension, self.path + "/" + photo))
                else:
                    self.data[hash] = photo

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

    def get_duplicates(self):
        return self.duplicates

    def clean(self):
        self.__find_same_visual_recursive(self.path)
        print(self)
        self.__remove_files()
