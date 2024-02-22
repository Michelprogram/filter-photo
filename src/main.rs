use crate::lib::photo::photo::Cleaner;

pub mod lib;


fn main() {
    let PATH:String = String::from("/Users/michel-developer/Desktop/photo mamy");

    //let path = tools::get_path();

/*    let mut file = CleanFile::new(PATH, true);

    file.run();*/

    let mut photo = Cleaner::new(PATH, true);

    photo.run()
}
