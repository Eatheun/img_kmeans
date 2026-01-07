from math import floor, sqrt
from typing_extensions import Self


class Clr():
    def __init__(self, col: tuple[float, ...]):
        n_items = len(col)
        self.r = col[0]
        self.g = col[1]
        self.b = col[2]
        self.a = col[3] if n_items > 3 else 255  # prob will never use this lol

    def get_ansi_str(self) -> str:
        r, g, b, _ = self.get_rgba_floored()
        return f"\033[48;2;{r};{g};{b}m"

    def block(self) -> str:
        return f"{self.get_ansi_str()} \033[0m\033[1m"

    def to_hex(self) -> str:
        r, g, b, _ = map(
            lambda x: hex(x).removeprefix("0x").rjust(2, "0"),
            self.get_rgba_floored()
        )

        # don't include alpha value
        # UNLESS YOU HAVE A COMPOSITOR
        return f"{r}{g}{b}"

    def dist_to(self, other: Self) -> float:
        dr = self.r - other.r
        dg = self.g - other.g
        db = self.b - other.b
        return sqrt(dr ** 2 + dg ** 2 + db ** 2)

    def eq(self, other: Self) -> bool:
        return self.r == other.r and\
            self.g == other.g and\
            self.b == other.b and\
            self.a == other.a

    def get_rgba(self) -> tuple[float, ...]:
        return (self.r, self.g, self.b, self.a)

    def get_rgba_floored(self) -> tuple[int, ...]:
        return (
            floor(self.r),
            floor(self.g),
            floor(self.b),
            floor(self.a),
        )

    def lighter(self, mod: int) -> Self:
        return Clr(tuple(map(
            lambda v: min(v + mod, 0xff),
            self.get_rgba()
        )))

    def darker(self, mod: int) -> Self:
        return Clr(tuple(map(
            lambda v: max(v - mod, 0x0),
            self.get_rgba()
        )))

    # arbitrary formula to get how "vibrant" or "poppy" a colour is
    def get_vibrancy(self) -> float:
        rgb = self.get_rgba()[:-1]
        smudged_clr_val = sum(rgb) / len(rgb)
        highest_val = max(rgb)
        lowest_val = min(rgb)
        return (highest_val - smudged_clr_val)**2 +\
            (lowest_val - smudged_clr_val)**2

    def print_sample(self):
        print(f"{self.get_ansi_str()}{self.to_hex()}\033[0m\033[1m")

    def print_hex(self):
        print(f"{self.to_hex()}")
