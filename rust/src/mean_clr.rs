use std::ops::AddAssign;

use crate::{clr::Clr, pretty_print::PrettyPrint};

#[derive(Clone, Debug)]
pub struct MeanClr {
    r: u64,
    g: u64,
    b: u64,
    n: u64,
    clrs: Vec<Clr>,
}

// creating from other Clr
impl From<&Clr> for MeanClr {
    fn from(value: &Clr) -> Self {
        let [r, g, b] = value.get();
        MeanClr {
            r,
            g,
            b,
            n: 1,
            clrs: vec![],
        }
    }
}

impl From<[u64; 3]> for MeanClr {
    fn from(value: [u64; 3]) -> Self {
        let [r, g, b] = value;
        MeanClr {
            r,
            g,
            b,
            n: 1,
            clrs: vec![],
        }
    }
}

// basic arithmetic
impl AddAssign<Clr> for MeanClr {
    fn add_assign(&mut self, rhs: Clr) {
        let [r, g, b] = rhs.get();
        self.r += r;
        self.g += g;
        self.b += b;
        self.n += 1;
        self.clrs.push(rhs);
    }
}

impl PartialEq<Clr> for MeanClr {
    fn eq(&self, other: &Clr) -> bool {
        let [r, g, b] = other.get();
        self.r == r && self.g == g && self.b == b
    }
}

impl PartialEq<MeanClr> for MeanClr {
    fn eq(&self, other: &MeanClr) -> bool {
        let [r, g, b] = other.get();
        self.r == r && self.g == g && self.b == b
    }
}

// printing and post processing
impl PrettyPrint for MeanClr {
    fn get(&self) -> [u64; 3] {
        self.get_mean().get()
    }
}

impl MeanClr {
    pub fn dist_to(&self, other: Clr) -> u64 {
        self.get_mean().dist_to(other)
    }

    fn get(&self) -> [u64; 3] {
        [self.r, self.g, self.b]
    }

    pub fn get_mean(&self) -> Clr {
        let rgb = self.get().map(|x| (x / self.n) as u8);
        Clr::from(rgb)
    }
}
