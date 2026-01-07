use std::{collections::HashMap, env::args, error::Error, fs::exists, process::exit};

use image::ImageReader;
use itertools::Itertools;
use rand::{
    distr::{Distribution, weighted::WeightedIndex},
    seq::IndexedRandom,
};

use crate::{clr::Clr, mean_clr::MeanClr, pretty_print::PrettyPrint};

mod clr;
mod mean_clr;
mod pretty_print;

static SIZE: u32 = 300; // test your cpu :0
static N_CLRS: u32 = 8; // default clusters

fn vec_clr_to_counter(clrs: &[Clr]) -> HashMap<Clr, i32> {
    clrs.iter().fold(HashMap::new(), |mut points, c| {
        *points.entry(*c).or_default() += 1;
        points
    })
}

fn run_kmeans(points: Vec<(&Clr, &i32)>, k: u32) -> Vec<MeanClr> {
    let mut rng = rand::rng();

    // do k means ++ to find optimal clusters
    let mut means = vec![];
    for _ in 0..k {
        if means.is_empty() {
            let first_mean = MeanClr::from(points.choose(&mut rng).unwrap().0);
            means.push(first_mean);
            continue;
        }

        let (x, min_l2_norms): (Vec<&Clr>, Vec<u64>) = points
            .iter()
            .map(|(p, _)| {
                // compute all the l2_norms then find minimum(s) (if any non-zero)
                if let Some(l2_norm) = means
                    .iter()
                    .map(|mu| mu.get_mean().dist_to(**p))
                    .map(|d| d * d)
                    .min()
                {
                    (*p, l2_norm)
                } else {
                    (*p, 0)
                }
            })
            .filter(|(_, d)| *d != 0)
            .unzip();

        if min_l2_norms.is_empty() {
            continue;
        }

        let weighted_l2_norm_dist = WeightedIndex::new(min_l2_norms).unwrap();
        let new_mean = MeanClr::from(x[weighted_l2_norm_dist.sample(&mut rng)]);

        means.push(new_mean);
    }

    // main k means algorithm
    points.iter().for_each(|(p, _)| {
        // find closest mean
        let min_mu_idx = match means
            .iter()
            .enumerate()
            .min_by_key(|(_, mu)| mu.dist_to(**p))
        {
            Some((idx, _)) => idx,
            None => 0,
        };

        // refit means
        means[min_mu_idx] += **p;
    });

    means.sort_by_key(|mu| u64::from_str_radix(&mu.get_mean().to_hex(), 16).unwrap());
    means
}

fn main() -> Result<(), Box<dyn Error>> {
    // unsafe and very rudimentary arg parsing
    let argv: Vec<String> = args().collect();
    let argc = argv.len();
    if argc < 2 {
        println!("Usage: {} <file> [k]", argv[0]);
        exit(1);
    }

    // check that img fn exists
    let img_fn = argv.get(1).unwrap().to_string();
    if exists(&img_fn).is_err() {
        println!("Image file {img_fn} does not exist!");
        exit(1);
    }

    // check for k
    let k = match argc >= 3 {
        true => match argv[2].parse() {
            Ok(k) => k,
            Err(_) => {
                println!("[k] should be a valid integer, skipping");
                N_CLRS
            }
        },
        false => N_CLRS,
    };

    // this is image processing + k means
    let img = ImageReader::open(img_fn)?
        .decode()?
        .thumbnail(SIZE, SIZE)
        .to_rgb8();
    let cc: Vec<Clr> = img.pixels().map(|c| Clr::from(*c)).collect();
    let points = vec_clr_to_counter(&cc);
    let num_chunks = 4;
    let mut chunk_size = points.len() / num_chunks;
    if points.len() % num_chunks != 0 {
        chunk_size += 1;
    }
    let point_chunks = points.iter().chunks(chunk_size);
    let chunk_means = point_chunks
        .into_iter()
        .flat_map(|points| run_kmeans(points.collect::<Vec<(&Clr, &i32)>>(), k))
        .map(|mu| mu.get_mean())
        .collect::<Vec<Clr>>();

    // printing
    let means = run_kmeans(
        vec_clr_to_counter(&chunk_means)
            .iter()
            .collect::<Vec<(&Clr, &i32)>>(),
        k,
    );
    means.iter().for_each(|mu| {
        mu.print_sample();
    });

    exit(0);
}
