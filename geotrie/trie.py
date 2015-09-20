# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import chain


SENTINEL = None


class KeyNotFound(Exception):
    """Raised when a key is not present in the trie."""
    pass


class _Node(object):

    __slots__ = ('_values', '_children')

    def __init__(self, values=None, children=None):
        if children is None:
            children = defaultdict(_Node)
        if values is None:
            values = []
        self._values = values
        self._children = children

    def __getitem__(self, key):
        return self._children[key]

    def __contains__(self, key):
        return key in self._children

    @property
    def values(self):
        return self._values

    def add_value(self, value):
        self._values.append(value)

    def iterate_values(self, selector=None):
        children = self._children
        if selector:
            children = [child for child in children if selector(child)]
        iterables = [n.iterate_values() for n in children.itervalues()]
        return chain(self._values, chain(*iterables))

    def walk(self, key, sentinel=False, create=False):
        lkey = list(key)
        if sentinel:
            lkey.append(SENTINEL)
        node = self
        for ch in lkey:
            if ch not in node._children and not create:
                raise KeyNotFound(key)
            node = node._children[ch]
        return node


class Trie(object):

    def __init__(self, tuples=None):
        self.root = _Node()
        if tuples:
            self.add_many(tuples)

    def add(self, key, value):
        node = self.root.walk(key, sentinel=True, create=True)
        node.add_value(value)

    def add_many(self, tuples):
        for key, value in tuples:
            self.add(key, value, value)

    def has(self, key):
        try:
            self.root.walk(key, sentinel=True)
            return True
        except KeyNotFound:
            return False

    def has_prefix(self, key):
        try:
            self.root.walk(key)
            return True
        except KeyNotFound:
            return False

    def values(self, key):
        node = self.root.walk(key, sentinel=True)
        return node.values

    def values_for_prefix(self, key):
        node = self.root.walk(key)
        return node.iterate_values()
