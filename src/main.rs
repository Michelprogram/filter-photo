use std::time::Instant;
use crate::lib::photo::{
    utils::tools::flags,
    cleaner::cleaner::Cleaner
};

mod lib;

fn main() {

    let (path, verbose) = flags();

    let photo = Cleaner::new(path, verbose);

    let start = Instant::now();
    photo.run();
    println!("Time elapsed in photo run is: {:?}", start.elapsed());
}
