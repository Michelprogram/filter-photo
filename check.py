import os
from re import sub
from collections import defaultdict
from PIL import Image
import imagehash

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
        return x.replace('\\','/')

class CleanFiles :

    path = ""
    verbose = False
    files = []
    duplicated = {}

    def __init__(self, verbose = False) -> None:
        self.path = Utils.get_path()
        self.verbose = verbose
        self.files = os.listdir(self.path)
        self.duplicated = {}
    
    def __remove_dump_name_duplicate(self, name):
        """Clean name of duplicated file ex : IMG_9982 (1) -> IMG_9982"""
        return sub(r" \(\d\)", '',name)
    
    def __find_duplicate_file_by_name(self):
        """Looking in directory if files have same name"""
        data = defaultdict(list)

        for file in self.files:

            name, size, extension = Utils.get_information(file, self.path)

            if name != "":
                clean_name = self.__remove_dump_name_duplicate(name)

                data[clean_name].append(File(name, size, extension, self.path + "/" + file))
            
        return {k:v for k,v in data.items() if len(v) > 1}
    
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
                    print(f"File {clean_name} it's a fake duplication of {file.name}")

                    counter+=1
                    new_name = f"{self.path}/{file.name}_{counter}.{file.extension}"
                    os.rename(file.path, new_name)

                    print(f"Rename of {file.path} to {new_name}")

    def __remove_files(self):
        """Remove duplicated files"""

        print(f"Would you like to remove {self.__count_duplication()} duplications files ? (y/n)")

        x = input()
        total = 0
        counter = 0

        if x == 'y':
            for _, v in self.duplicated.items():
                for i in range(0, len(v)-1):
                    os.remove(v[i].path)
                    total += v[i].size
                    counter += 1
            print(f"You have deleted {counter} files, that represent {total} MB")
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
    

class CleanPhoto:

    path = ""
    verbose = False
    accuracy = 0
    photos = []
    duplicates = []

    def __init__(self, verbose = False, accuracy = 4) -> None:
        self.path = Utils.get_path()
        self.verbose = verbose
        self.photos = os.listdir(self.path)
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
                    name, size, extension = Utils.get_information(photo, self.path)

                    self.duplicates.append(File(name, size, extension, self.path + "/" + photo))
                else:
                    data[hash] = photo

    def __remove_files(self):
        print(f"Would you like to remove {len(self.duplicates)} duplications files ? (y/n)")

        x = input()

        if x == 'y':
            for photo in self.duplicates:
                os.remove(photo.path)
            print(f"You have deleted {len(self.duplicates)} files, that represent {self.__count_duplication_size()} MB")
        else:
            print("Remove operation was canceled.")


                
    def clean(self):
        self.__find_same_visual()
        print(self)
        self.__remove_files()


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


""" app = CleanFiles()

app.clean() """

app = CleanPhoto(accuracy=12, verbose=True)

app.clean()
