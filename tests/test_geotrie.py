# -*- coding: utf-8 -*-

import operator
import itertools

import pytest
from geotrie import GeoTrie


class TestAdd(object):

    def test_single(self):
        geotrie = GeoTrie(precision=6)
        point = (51.528642, -0.101599)
        geotrie.add(point, data='foo')
        assert geotrie.trie.has('gcpvjs')
        assert geotrie.trie.values('gcpvjs') == [
            ((51.528642, -0.101599), 'foo')
        ]

    def test_multiple(self):
        geotrie = GeoTrie(precision=6)

        point = (51.528642, -0.101599)
        geotrie.add(point)
        assert geotrie.trie.has('gcpvjs')
        assert geotrie.trie.values('gcpvjs') == [
            ((51.528642, -0.101599), None)
        ]

        point = (51.7505017, -1.3177993)
        geotrie.add(point)
        assert geotrie.trie.has('gcpn6h')
        assert geotrie.trie.values('gcpn6h') == [
            ((51.7505017, -1.3177993), None)
        ]


class TestAddMany(object):

    def test_many(self):
        geotrie = GeoTrie(precision=6)
        points = [
            ((51.528642, -0.101599), None),
            ((51.7505017, -1.3177993), None)
        ]
        geotrie.add_many(points)
        assert geotrie.trie.has('gcpvjs')
        assert geotrie.trie.has('gcpn6h')
        assert geotrie.trie.values('gcpvjs') == [
            ((51.528642, -0.101599), None)
        ]
        assert geotrie.trie.values('gcpn6h') == [
            ((51.7505017, -1.3177993), None)
        ]


class TestRadiusSearch(object):

    PRECISIONS = [
        12,
        8,
        4,
        1
    ]

    SEARCHES = [
        (
            # All points are in a radius of <500m.
            [
                (51.514138, -0.136282),
                (51.513284, -0.135724),
                (51.514405, -0.134737),
                (51.514619, -0.138127),
                (51.513898, -0.138342)
            ],
            (0, 1, 2, 3, 4),
        ),
        (
            # The first two points are within radius, the others are returned by the
            # geohash expansion but are then discarded by the haversive filter.
            [
                (51.514138, -0.136282),
                (51.513284, -0.135724),
                (51.517770, -0.140273),
                (51.518037, -0.139200)
            ],
            (0, 1)
        ),
        (
            # The first two points are within radius, the others are not returned by the
            # geohash expansion.
            [
                (51.514138, -0.136282),
                (51.513284, -0.135724),
                (51.522043, -0.151002),
                (51.521322, -0.140616)
            ],
            (0, 1)
        ),
        (
            # No points are within radius.
            [
                (51.522043, -0.151002),
                (51.521322, -0.140616)
            ],
            []
        )
    ]

    @pytest.mark.parametrize('precision,search', itertools.product(PRECISIONS, SEARCHES))
    def test_search(self, precision, search):
        points, expected_hits = search

        geotrie = GeoTrie(precision=precision)
        for p in points:
            geotrie.add(p)

        center = (51.513284, -0.136539)
        hits = geotrie.radius_search(center, 500)
        assert len(hits) == len(expected_hits)

        hits = map(operator.itemgetter(0), hits)
        for i in expected_hits:
            assert points[i] in hits
