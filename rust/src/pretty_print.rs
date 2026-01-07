pub trait PrettyPrint {
    fn get(&self) -> [u64; 3];

    fn get_ansi_str(&self) -> String {
        let [r, g, b] = self.get();
        format!("\x1b[48;2;{r};{g};{b}m")
    }

    fn to_hex(&self) -> String {
        let [r, g, b] = self.get().map(|x| format!("{x:02x}"));
        format!("{r}{g}{b}")
    }

    fn print_sample(&self) {
        println!("{}{}\x1b[0m\x1b[1m", self.get_ansi_str(), self.to_hex())
    }
}
