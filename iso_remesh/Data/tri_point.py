import numpy as np
from typing import Tuple

from iso_remesh.Data.bi_point import BiPoint


class TriPoint:
    def __init__(self, vertices: np.ndarray | Tuple[np.ndarray]) -> None:
        self.vertices = (
            vertices if isinstance(vertices, np.ndarray) else np.vstack(vertices)
        )
        self._lengths = self.get_lenghts()
        self._vectors = self.vertices[1:] - self.vertices[0][np.newaxis, :]

    def get_area(self) -> float:
        # https://en.wikipedia.org/wiki/Heron%27s_formula
        s = np.sum(self._lengths) / 2.0
        mask = np.isclose(s, self._lengths)  # fix rounding issue.
        aux = np.where(mask, 0.0, s - self._lengths)
        return np.sqrt(s * np.prod(aux))

    def get_lenghts(self) -> np.ndarray:
        vectors = np.diff(self.vertices, axis=0, append=self.vertices[0][np.newaxis, :])
        return np.linalg.norm(vectors, axis=1)

    def get_compactness(self) -> float:
        return 4 * np.sqrt(3.0) * self.get_area() / np.linalg.norm(self._lengths) ** 2

    def get_normal(self, normalize: bool = True) -> np.ndarray:
        n = np.cross(self._vectors[0], self._vectors[1])
        if normalize:
            n /= np.linalg.norm(n)
        return n

    def get_angle(self, **kwargs) -> float:
        return BiPoint.angle(self._vectors, **kwargs)

    def get_cotangent(self) -> float:
        return BiPoint.cotangent(self._vectors)

    def get_cosecant(self) -> float:
        return BiPoint.cosecant(self._vectors)

    def get_is_collinear(self) -> bool:
        n = self.get_normal(normalize=False)
        return np.allclose(n, 0)

    def get_is_obtuse(self) -> Tuple[bool, bool, bool]:
        # https://mathworld.wolfram.com/LawofCosines.html
        # https://mathworld.wolfram.com/ObtuseTriangle.html
        a, b, c = self._lengths[0], self._lengths[1], self._lengths[2]
        return (a**2 + c**2 < b**2), (a**2 + b**2 < c**2), (b**2 + c**2 < a**2)

    def get_barycentric_region(self) -> float:
        return self.get_area() / 3.0

    def get_voronoi_region(self) -> float:
        a, _, c = self._lengths[0], self._lengths[1], self._lengths[2]
        p, r, q = self.vertices[0], self.vertices[1], self.vertices[2]
        return (1 / 8.0) * (
            a**2 * BiPoint.cotangent((p - q, r - q))
            + c**2 * BiPoint.cotangent((p - r, q - r))
        )

    def get_mixed_voronoi_region(self) -> float:
        # http://rodolphe-vaillant.fr/entry/20/compute-harmonic-weights-on-a-triangular-mesh#mixed_voro_area
        obts = self.get_is_obtuse()
        if not any(obts):
            return self.get_voronoi_region()
        return self.get_area() / 2.0 if obts[0] else self.get_area() / 4.0

    def get_barycenter(self) -> np.ndarray:
        return np.mean(self.vertices, axis=0)

    def get_barycentric_coords(self, point: np.ndarray) -> np.ndarray:
        p, r, q = self.vertices[0], self.vertices[1], self.vertices[2]
        coords = np.array(
            [
                TriPoint.area((point, q, r)),
                TriPoint.area((point, p, q)),
                TriPoint.area((point, p, r)),
            ]
        )
        coords /= np.sum(coords)
        return coords

    def get_barycentric_interp(self, values: np.ndarray) -> float:
        bary = self.get_barycenter()
        coords = self.get_barycentric_coords(bary)
        return np.inner(values, coords)

    @classmethod
    def is_collinear(cls, vertices):
        return cls(vertices).get_is_collinear()

    @classmethod
    def barycenter(cls, vertices):
        return cls(vertices).get_barycenter()

    @classmethod
    def normal(cls, vertices, **kwargs):
        return cls(vertices).get_normal(**kwargs)

    @classmethod
    def area(cls, vertices):
        return cls(vertices).get_area()

    @classmethod
    def barycentric_interp(cls, vertices, *args, **kwargs):
        return cls(vertices).get_barycentric_interp(*args, **kwargs)
