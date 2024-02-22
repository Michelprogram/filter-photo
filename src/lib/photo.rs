pub mod photo{
    use std::collections::HashMap;
    use std::ffi::OsStr;
    use std::fs::{DirEntry, File, read_dir};
    use std::hash::Hash;
    use std::io::{BufReader, Write};
    use image::{DynamicImage, EncodableLayout};
    use image::imageops::FilterType;
    use sha1::{Sha1, Digest};
    use hex::encode;
    use sha1::digest::{DynDigest, Update};



    fn find_photos(path: &str, photos: &mut Vec<DirEntry>){

        for file in read_dir(path).unwrap() {

            let file = file.unwrap();

            if file.path().is_dir(){
                find_photos(&file.path().to_str().unwrap(), photos);
            }

            match file.path().extension(){
                None => continue,
                Some(ext) => {
                    match ext.to_str().unwrap(){
                        "jpg" | "png" | "jpeg" => photos.push(file),
                        _ => continue
                    }
                }
            }
        }
    }

    pub struct Cleaner{
        path: String,
        verbose: bool,
        photos: Vec<DirEntry>,
    }

    impl Cleaner{
        pub fn new(path: String, verbose: bool) -> Self{
            Cleaner{
                path,
                verbose,
                photos: Vec::new(),
            }
        }

        fn hash_image(self, photos: Vec<DirEntry>) -> HashMap<String, Vec<DirEntry>>{

            let mut map:HashMap<String, Vec<DirEntry>> = HashMap::new();

            for photo in photos{
                // Read the image from the given path
                let img = image::open(photo.path().to_str().unwrap().to_string())
                    .expect("Failed to open image");

                // Resize the image to 20x20 pixels
                let resized_img: DynamicImage = img
                    .grayscale()
                    .resize(200, 200, FilterType::Gaussian);

                let hasher = Sha1::new()
                    .chain_update(resized_img.as_bytes())
                    .finalize();

                match map.get_mut(&encode(&hasher)) {
                    None => {
                        map.insert(encode(hasher), vec![photo]);
                    }
                    Some(value) => {
                        value.push(photo);
                    }
                }

            }

            return map;
        }

        pub fn run(self){

            let mut vec = Vec::new();

            find_photos(&self.path, &mut vec);

            println!("All photo finded");

            let duplications = self.hash_image(vec);

        }
    }

}