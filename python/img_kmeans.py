#!./bin/python3
from PIL import Image
from Clr import Clr
from MeanClr import MeanClr
from random import choice
import numpy as np
import sys

SIZE = 200  # test your cpu :0
N_CLRS = 8  # default clusters


def run_kmeans(
    points: list[tuple[Clr, int]],
    k: int
) -> list[MeanClr]:
    # do k means ++ to find optimal clusters
    means = []
    for i in range(k):
        if len(means) == 0:
            first_mean = MeanClr(choice(points)[0].get_rgba())
            first_mean.compute_all_dists(points)
            means.append(first_mean)
            continue

        x = []
        min_l2_norms = []
        for p, _ in points:
            # compute all the l2_norms
            l2_norms = []
            for mu in means:
                dist = mu.dist_to(p)
                if dist == 0:
                    continue

                l2_norms.append(dist ** 2)

            if len(l2_norms) == 0:
                continue

            # add
            x.append(p)
            min_l2_norms.append(min(l2_norms))

        total_l2_norms = sum(min_l2_norms)
        px = list(map(lambda d: d / total_l2_norms, min_l2_norms))
        new_mean = MeanClr(np.random.choice(x, p=px).get_rgba())

        means.append(new_mean)

    # main k means algorithm
    for p, n in points:
        for _ in range(n):
            # find closest mean
            min_dist = float("Inf")
            min_mu_idx = 0
            for i, mu in enumerate(means):
                curr_dist = mu.dist_to(p)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    min_mu_idx = i

            # refit means
            means[min_mu_idx].add(p)

    means.sort(key=lambda mu: int(mu.get_mean().to_hex(), 16))
    return means


def run_kmeans_on_img(img_fn: str, k: int):
    img = Image.open(img_fn)
    img.thumbnail((SIZE, SIZE))
    cc = img.getcolors(SIZE ** 2)
    if cc is None:
        print(f"Unexpected image file {img_fn}")
        sys.exit(1)

    points = [
        (Clr(colour), n)
        for n, colour in cc
        if isinstance(colour, tuple)
    ]

    # run the k means
    means = run_kmeans(points, k)

    return means


if __name__ == "__main__":
    # unsafe and very rudimentary arg parsing
    img_fn = ""
    k = N_CLRS
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: {sys.argv[0]} <file> [k]")
        sys.exit(1)
    elif argc < 3:
        img_fn = sys.argv[1]
    else:
        img_fn = sys.argv[1]
        k = int(sys.argv[2])

    # run kmeans and print palette
    means = run_kmeans_on_img(img_fn, k)

    for mu in means:
        clr = mu.get_mean()
        print(clr.to_hex())

    sys.exit(0)
