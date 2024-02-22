pub mod clear {
    use std::collections::HashMap;
    use std::fmt::Display;
    use std::fs::{DirEntry, read_dir};
    use std::fs::ReadDir;
    use regex::Regex;
    use crate::lib::utils::file::File;

    pub struct CleanFile{
        path: String,
        verbose: bool,
        duplicates: HashMap<String, Vec<File>>
    }

    impl Display for CleanFile{
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {


            let mut sentence = String::new();

            for (key,value) in &self.duplicates {

                if value.len() > 1{
                    sentence += &format!("File {} have {} duplications\n", key, value.len() - 1);

                    value.iter()
                        .filter(|file|  &file.name != key)
                        .for_each(|file| sentence.push_str(&file.to_string()));
                }

            }

            let (count, size) = self.count_duplication_size();

            sentence.push_str(format!("You have {} files with duplications, that represent total of {} bytes\n", count, size).as_str());

            write!(f, "{}", sentence)
        }
    }

    impl CleanFile{
        pub fn new(path: String, verbose: bool) -> Self{
            return CleanFile{
                verbose,
                path:path.clone(),
                duplicates: HashMap::new(),
            }
        }

        fn remove_dump_name_duplicate(&self, name: &String) -> String{
            let pattern= Regex::new(r" \(\d\)").unwrap();

            let replaced = pattern.replace_all(name,"");

            replaced.trim().to_string()
        }

        fn find_duplicate_file_by_name(&mut self){

            for file in read_dir(&self.path).unwrap() {
                let file = File::new(file.unwrap());

                if file.name != "" && file.is_image() {
                    let cleaned_name = self.remove_dump_name_duplicate(&file.name);

                    match self.duplicates.get_mut(&cleaned_name) {
                        None => {
                            self.duplicates.insert(cleaned_name, vec![file]);
                        }
                        Some(value) => {
                            value.push(file);
                        }
                    }
                }
            }
        }

        fn count_duplication_size(&self) -> (usize, u64){

            let mut counter = 0;
            let mut size = 0;

            for value in self.duplicates.values(){
                counter += value.len() - 1;
                value
                    .iter()
                    .skip(1)
                    .for_each(|f| size += f.size);
            }

            return (counter, size);
        }

        pub fn run(&mut self){
            self.find_duplicate_file_by_name();

            if self.verbose{
                println!("{}", self)
            }

        }
    }
}

