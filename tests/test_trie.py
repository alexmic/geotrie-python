# -*- coding: utf-8 -*-

import pytest
from geotrie.trie import Trie, SENTINEL, KeyNotFound


def assert_has_key(trie, key, value):
    node = trie.root
    for ch in list(key) + [SENTINEL]:
        assert ch in node
        node = node[ch]
    assert value in node.values


class TestAdd(object):

    def test_single(self):
        trie = Trie()
        trie.add('foo', 1)
        assert_has_key(trie, 'foo', 1)

    def test_multiple_with_different_keys(self):
        trie = Trie()
        trie.add('foo', 1)
        trie.add('bar', 2)
        assert_has_key(trie, 'foo', 1)
        assert_has_key(trie, 'bar', 2)

    def test_multiple_with_same_key(self):
        trie = Trie()
        trie.add('foo', 1)
        trie.add('foo', 2)
        assert_has_key(trie, 'foo', 1)
        assert_has_key(trie, 'foo', 2)

    def test_multiple_with_same_key_prefix(self):
        trie = Trie()
        trie.add('foo', 1)
        trie.add('foobar', 2)
        assert_has_key(trie, 'foo', 1)
        assert_has_key(trie, 'foobar', 2)


class TestAddMany(object):

    def test_many(self):
        trie = Trie()
        trie.add_many([('foo', 1), ('bar', 2)])
        assert_has_key(trie, 'foo', 1)
        assert_has_key(trie, 'bar', 2)


class TestHas(object):

    def test_key_exists(self):
        trie = Trie()
        trie.add('foo', 1)
        assert trie.has('foo')

    def test_key_does_not_exist(self):
        trie = Trie()
        assert not trie.has('foo')


class TestHasPrefix(object):

    def test_prefix_exists(self):
        trie = Trie()
        trie.add('foobar', 1)
        assert trie.has_prefix('foo')

    def test_whole_key_as_prefix(self):
        trie = Trie()
        trie.add('foobar', 1)
        assert trie.has_prefix('foobar')

    def test_key_does_not_exist(self):
        trie = Trie()
        assert not trie.has_prefix('foobar')


class TestValues(object):

    def test_key_exists(self):
        trie = Trie()
        trie.add('foobar', 1)
        trie.add('foobar', 2)
        assert trie.values('foobar') == [1, 2]

    def test_key_does_not_exist(self):
        trie = Trie()
        with pytest.raises(KeyNotFound):
            trie.values('foobar')


class TestValuesForPrefix(object):

    def test_prefix_exists(self):
        trie = Trie()
        trie.add('foob', 1)
        trie.add('fooba', 2)
        trie.add('foobb', 3)
        trie.add('foobar', 4)
        trie.add('foobaz', 5)
        values = list(trie.values_for_prefix('foo'))
        assert len(values) == 5
        for i in range(1, 6):
            assert i in values

    def test_prefix_does_not_exist(self):
        trie = Trie()
        with pytest.raises(KeyNotFound):
            trie.values_for_prefix('foobar')
