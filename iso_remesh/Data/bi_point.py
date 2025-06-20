import numpy as np
from typing import Tuple


class BiPoint:
    def __init__(self, vertices: np.ndarray | Tuple[np.ndarray]) -> None:
        self.vertices = (
            vertices if isinstance(vertices, np.ndarray) else np.vstack(vertices)
        )
        self._norms = np.linalg.norm(self.vertices, axis=1, keepdims=True)
        self._normed = self.vertices / self._norms
        self._ip = np.inner(self.vertices[0], self.vertices[1])
        self._cp = np.cross(self.vertices[0], self.vertices[1])

    def get_midpoint(self) -> np.ndarray:
        return np.sum(self.vertices, axis=0) / 2.0

    def get_distance(self) -> np.ndarray:
        v = np.diff(self.vertices, axis=0)
        return np.linalg.norm(v)

    def get_angle(self, degree: bool = True) -> float:
        ip = np.inner(self._normed[0], self._normed[1])
        cs = np.clip(ip, -1, 1)  # fix rounding issue.
        rads = np.arccos(cs)
        return np.rad2deg(rads) if degree else rads

    def get_cotangent(self) -> float:
        return self._ip / np.linalg.norm(self._cp)

    def get_cosecant(self) -> float:
        return np.prod(self._norms) / np.linalg.norm(self._cp)

    @classmethod
    def angle(cls, vertices, **kwargs):
        return cls(vertices).get_angle(**kwargs)

    @classmethod
    def distance(cls, vertices):
        return cls(vertices).get_distance()

    @classmethod
    def midpoint(cls, vertices):
        return cls(vertices).get_midpoint()

    @classmethod
    def cotangent(cls, vertices):
        return cls(vertices).get_cotangent()

    @classmethod
    def cosecant(cls, vertices):
        return cls(vertices).get_cosecant()
