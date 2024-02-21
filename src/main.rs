use crate::lib::utils::{file, tools};
use std::fs::{read, read_dir, ReadDir};
use crate::lib::file::clear::CleanFile;

pub mod lib;


fn main() {
    let PATH:String = String::from("/Users/michel-developer/Desktop/photo mamy/2016-12");

    let path = tools::get_path();

    let mut file = CleanFile::new(PATH, true);

    file.run();
}
