pub mod tools{
    use std::env;

    pub fn flags() -> (String, bool){
        let args: Vec<String> = env::args().collect();

        let mut verbose = false;
        let mut path = "";

        for i in 1..args.len(){
            match args[i].as_str() {
                "-p" => path = args[i+1].as_str(),
                "-v" => verbose = true,
                _ => continue
            }
        }

        (String::from(path), verbose)
    }
}
