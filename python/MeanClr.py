from Clr import Clr


class MeanClr(Clr):
    def __init__(self, col: tuple[float, ...]):
        super().__init__(col)
        self.n = 1
        self.clrs = []
        self.dists = {}

    def dist_to(self, other: Clr):
        if other in self.dists:
            return self.dists[other]

        dist = self.get_mean().dist_to(other)
        self.dists[other] = dist

        return dist

    def eq(self, other: Clr):
        return self.get_mean().eq(other)

    def add(self, other: Clr):
        self.r += other.r
        self.g += other.g
        self.b += other.b
        self.a += other.a
        self.n += 1
        self.clrs.append(other)

    def get_mean(self) -> Clr:
        return Clr((
            self.r / self.n,
            self.g / self.n,
            self.b / self.n,
            self.a / self.n
        ))

    def compute_all_dists(self, points: list[tuple[Clr, int]]):
        for p, _ in points:
            if self.eq(p):
                continue
            self.dist_to(p)
