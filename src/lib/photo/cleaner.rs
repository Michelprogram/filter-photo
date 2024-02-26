pub mod cleaner{

    use hex::encode;
    use sha1::{Digest, Sha1};
    use std::{
        collections::HashMap,
        fs::{
            read,
            read_dir,
            remove_file,
            DirEntry
        },
        thread::spawn,
        sync::{Arc, Mutex},
        io::{BufRead, stdin},
        process::exit
    };

    pub fn find_photos(path: &str, photos: &mut Vec<DirEntry>) {
        for file in read_dir(path).unwrap() {
            let file = file.unwrap();

            if file.path().is_dir() {
                find_photos(&file.path().to_str().unwrap(), photos);
            }

            match file.path().extension() {
                None => continue,
                Some(ext) => match ext.to_str().unwrap() {
                    "jpg" | "png" | "jpeg" => photos.push(file),
                    _ => continue,
                },
            }
        }
    }


    pub struct Cleaner {
        path: String,
        verbose: bool,
        photos: Vec<DirEntry>,
    }

    impl Cleaner {
        pub fn new(path: String, verbose: bool) -> Self {
            Cleaner {
                path,
                verbose,
                photos: Vec::new(),
            }
        }

        fn hash_images(&self, photos: Vec<DirEntry>) -> HashMap<String, Vec<DirEntry>> {

            let num_threads = num_cpus::get();
            let map = Arc::new(Mutex::new(HashMap::new()));
            let photos = Arc::new(Mutex::new(photos));
            let mut threads = Vec::with_capacity(num_threads);

            for _ in 0..num_threads {
                let map = Arc::clone(&map);
                let photos = Arc::clone(&photos);
                threads.push(spawn(move || {
                    loop {
                        let mut data = photos.lock().unwrap();

                        //println!("Salut from {:?} value {}", thread::current().id(), data.len());
                        if data.is_empty() {
                            break;
                        }

                        let mut map = map.lock().unwrap();
                        let photo = data.remove(0);

                        // Read and process the image
                        match read(photo.path()) {
                            Ok(bytes) => {
                                let img = image::load_from_memory(&bytes)
                                    .expect("Failed to load image");

                                // Hash the resized image
                                let hasher = Sha1::new()
                                    .chain_update(img.as_bytes());
                                let hash = encode(hasher.finalize());

                                // Update the hash map
                                match map.get_mut(&hash) {
                                    None => {
                                        map.insert(hash, vec![photo]);
                                    }
                                    Some(value) => {
                                        value.push(photo);
                                    }
                                }

                            }
                            Err(err) => {
                                eprintln!("Error reading file: {}", err);
                            }
                        }

                    }
                }));
            }

            for thread in threads {
                thread.join().unwrap();
            }

            let res = Arc::try_unwrap(map)
                .unwrap()
                .into_inner()
                .unwrap();

            let _ = res.iter().filter(|(k, v)| v.len() > 1);

            return res;

        }

        fn count_duplication_size(&self, map: &HashMap<String, Vec<DirEntry>>) -> (usize, u64){

            let mut counter = 0;
            let mut size = 0;

            for value in map.values(){
                counter += value.len() - 1;
                value
                    .iter()
                    .skip(1)
                    .for_each(|f| size += f.metadata().unwrap().len());
            }

            return (counter, size);
        }

        fn remove_duplications(self, map: HashMap<String, Vec<DirEntry>>) {
            println!("Would you like to remove duplications files ? (y/n/i)");
            let mut read = String::new();
            let _ = stdin().lock().read_line(&mut read);

            if read.trim() == "y"{
                for files in map.values(){
                    files
                        .iter()
                        .skip(1)
                        .for_each(|f| remove_file(f.path()).unwrap());
                }
                return;
            }else if read.trim() == "i"{
                for files in map.values(){
                    println!("{} duplications of file {}", &files.len(), &files[0].path().to_str().unwrap());
                    for file in files.iter().skip(1){
                        println!("- {}", file.path().to_str().unwrap())
                    }
                }
                self.remove_duplications(map);
            }

            println!("Your duplications aren't going to be delete.");

            exit(1);
        }

        pub fn run(self) {
            let mut vec = Vec::new();

            find_photos(&self.path, &mut vec);

            let duplications = self.hash_images(vec);

            let (count, size) = self.count_duplication_size(&duplications);

            if self.verbose{
                println!("Found {} duplications that represent {} bytes", count, size);
            }

            if count >= 1{
                self.remove_duplications(duplications);
            }

        }
    }
}
