# -*- coding: utf-8 -*-

from __future__ import division

import geohash
from haversine import haversine

from .trie import Trie, KeyNotFound


DEFAULT_PRECISION = 10

PRECISION_LEVELS = (
    (0.00925, 12),
    (0.074, 11),
    (0.6, 10),
    (2.4, 9),
    (19, 8),
    (76, 7),
    (610, 6),
    (2400, 5),
    (20000, 4),
    (78000, 3),
    (630000, 2),
    (2500000, 1)
)


class GeoTrie(object):

    def __init__(self, points=None, precision=MAX_PRECISION):
        self._precision = MAX_PRECISION
        self.trie = Trie()
        if points is not None:
            self.add_many(points)

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        raise NotImplementedError

    def add(self, point, data=None):
        encoded = geohash.encode(*point, precision=self.precision)
        self.trie.add(encoded, (point, data))

    def add_many(self, tuples):
        for point, data in tuples:
            self.add(point, data=data)

    def radius_search(self, center, radius):
        """Returns all points that are `radius` distance apart from the center.

        :param center: A coordinate tuple.
        :param radius: The radius in meters.

        """
        precision = min(self.precision, self._radius_to_precision(radius))
        center_hash = geohash.encode(*center, precision=precision)
        hits = self._get_hits(center_hash)
        return [(p, d) for p, d in hits if haversine(p, center) <= (radius / 1000)]

    def _get_hits(self, center_hash):
        hits = []
        for hash_ in geohash.expand(center_hash):
            try:
                hits.extend(self.trie.values_for_prefix(hash_))
            except KeyNotFound:
                pass
        return hits

    def _radius_to_precision(self, radius):
        for size, precision in PRECISION_LEVELS:
            if size >= radius / 2:
                return precision
        return None
