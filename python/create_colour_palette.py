#!./bin/python3

from Clr import Clr
import sys

if __name__ == "__main__":
    arg_clrs = sys.argv[1:]
    if len(arg_clrs) < 5:
        print(f"Usage: {sys.argv[0]} <colour1> [colour2] ...")
        print("Please enter at least 5 colours")
        sys.exit(1)

    # processing args into Clr classes
    clrs = []
    for clr in arg_clrs:
        if len(clr) != 6:  # no alpha values
            print(f"Invalid colour {clr} must be a 6-digit hexadecimal number")
            sys.exit(1)

        # split string
        raw_clr_hex = tuple(clr[i:i+2] for i in range(0, len(clr), 2))

        try:
            raw_clr_dec = tuple(map(lambda tok: int(tok, 16), raw_clr_hex))
            clrs.append(Clr(raw_clr_dec))
        except Exception as e:
            print(e)
            print(f"Invalid colour {clr} must be a 6-digit hexadecimal number")
            sys.exit(1)

    # this is how much we're gonna add/minus from the vals
    mod = 0x35

    # find the lightest and then calc super light
    blk_clr = Clr((0, 0, 0))
    lightest_clr = max(clrs, key=lambda clr: clr.dist_to(blk_clr))
    super_light_clr = lightest_clr.lighter(mod)

    # find the darkest and then calc super dark
    wht_clr = Clr((255, 255, 255))
    darkest_clr = max(clrs, key=lambda clr: clr.dist_to(wht_clr))
    super_dark_clr = darkest_clr.darker(mod)

    # find 3 most vibrant colours
    vibrancies = list(map(lambda clr: (clr, clr.get_vibrancy()), clrs))
    vibrancies.sort(key=lambda v: v[1], reverse=True)

    modulations = []

    for clr, vibrancy in vibrancies[:3]:
        lighter = clr.lighter(mod)
        darker = clr.darker(mod)

        # for punchy, well add mod to some indices
        rgb = list(clr.get_rgba()[:-1])
        highest_idx, _, lowest_idx = tuple(map(
            lambda kv: kv[0],
            sorted(
                enumerate(rgb),
                key=lambda kv: kv[1],
                reverse=True
            )
        ))
        rgb[highest_idx] = min(rgb[highest_idx] + mod * 2, 0xff)
        rgb[lowest_idx] = min(rgb[lowest_idx] + mod, 0xff)
        punchy = Clr(tuple(rgb))

        negative = Clr(tuple(map(lambda val: 0xff - val, rgb)))

        # append to palette
        modulations.append((clr, lighter, darker, punchy, negative))

    # READ THIS FOR ORDER OF OUTPUT
    # order of colours is IMPORTANT
    # for each of the 3 most vibrant colours, print:
    # - base
    # - lighter
    # - darker
    # - punchy
    # - negative
    # print lightest and then super light
    # print darkest and then super dark
    for base, light, dark, punchy, negative in modulations:
        base.print_hex()
        light.print_hex()
        dark.print_hex()
        punchy.print_hex()
        negative.print_hex()
    lightest_clr.print_hex()
    super_light_clr.print_hex()
    darkest_clr.print_hex()
    super_dark_clr.print_hex()
