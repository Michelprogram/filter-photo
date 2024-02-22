pub mod file{
    use std::fs::DirEntry;
    use std::path::PathBuf;

    #[derive(Debug)]
    pub struct File{
        path: String,
        pub size: u64,
        pub extension: String,
        pub name: String
    }

    impl ToString for File{
        fn to_string(&self) -> String {
            format!("Path : {} as a size of {} bytes with extension {}\n", self.path, self.size, self.extension)
        }
    }

    impl File{

        pub fn new(entry: DirEntry) -> Self{

            let (path, name,extension, size) = Self::get_information(entry.path());

            return File{
                path,
                name,
                size,
                extension,
            }
        }

        pub fn is_image(&self) -> bool{
            match self.extension.as_str() {
                "png" | "jpg" | "jpeg" => true,
                _ => false
            }
        }

        fn get_information(path: PathBuf) -> (String, String, String, u64){

            let path = path.to_str().unwrap();

            let splitted: Vec<&str> = path
                .split(".")
                .collect();

            let extension = splitted
                .last()
                .unwrap()
                .to_string();

            let name = splitted
                .first()
                .unwrap()
                .split("/")
                .last()
                .unwrap()
                .to_string();


            (path.to_string(), name, extension, super::tools::get_file_size(path))
        }

    }
}

pub mod tools{
    use std::fs::metadata;
    use std::io::{stdin, stdout, Write};

    /*
        Get file size as megabyte
     */
    pub fn get_file_size(path: &str) -> u64{
        let file = metadata(path);

        file.unwrap().len()
    }

    pub fn get_path() -> String{
        println!("Path :");
        let mut line = String::new();
        match stdin().read_line(&mut line){
            Ok(_) => line.replace("\\","/"),
            _ => String::from("")
        }
    }

    pub fn is_directory(path: &str) -> bool{
        metadata(path).unwrap().is_dir()
    }

}
