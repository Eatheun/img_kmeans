use std::fmt::Debug;

use image::Rgb;

use crate::pretty_print::PrettyPrint;

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct Clr {
    r: u64,
    g: u64,
    b: u64,
}

impl From<Rgb<u8>> for Clr {
    fn from(value: Rgb<u8>) -> Self {
        let [r, g, b] = value.0.map(|x| x.into());
        Clr { r, g, b }
    }
}

impl From<[u8; 3]> for Clr {
    fn from(value: [u8; 3]) -> Self {
        let [r, g, b] = value.map(|x| x.into());
        Clr { r, g, b }
    }
}

// printing and post processing
impl PrettyPrint for Clr {
    fn get(&self) -> [u64; 3] {
        [self.r, self.g, self.b]
    }
}

// main arithmetic
impl Clr {
    // note this gives the l2 norm
    pub fn dist_to(&self, other: Clr) -> u64 {
        let dr = self.r.abs_diff(other.r);
        let dg = self.g.abs_diff(other.g);
        let db = self.b.abs_diff(other.b);
        (dr * dr + dg * dg + db * db).isqrt()
    }
}
