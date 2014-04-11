from unittest import TestCase

from dictdiffer import DictDiffer


class TestDictDiffer(TestCase):
    def setUp(self):
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 2, 'd': 0}
        self.d = DictDiffer(b, a)

    def test_added(self):
        self.assertEqual(self.d.added(), set(['d']))

    def test_removed(self):
        self.assertEqual(self.d.removed(), set(['c']))

    def test_changed(self):
        self.assertEqual(self.d.changed(), set(['b']))

    def test_unchanged(self):
        self.assertEqual(self.d.unchanged(), set(['a']))

    def test_changes(self):
        self.assertEqual(self.d.changes(), {'added': 1,
                                            'removed': 1,
                                            'changed': 1})

    def test_changes_same(self):
        """Dict are same
        """
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 1, 'c': 0}
        tdf = DictDiffer(b, a)

        self.assertEqual(tdf.changes(), {'added': 0,
                                         'removed': 0,
                                         'changed': 0})

    def test_haschanges(self):
        self.assertEqual(self.d.has_changes(), True)

    def test_haschanges_no(self):
        """Dict are the same
        """
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 1, 'c': 0}
        tdf = DictDiffer(b, a)

        self.assertEqual(tdf.has_changes(), False)

    def test_haschanges_empty(self):
        """Dict are empty
        """
        tdf = DictDiffer({}, {})
        self.assertFalse(tdf.has_changes())

    def test_nb_changes(self):
        """Number of changes
        """
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 2}
        tdf = DictDiffer(b, a)

        self.assertEqual(tdf.nb_changes(), 2)

    def test_nb_changes_same(self):
        """Number of changes
        """
        a = {'a': 1, 'b': 1}
        b = {'a': 1, 'b': 1}
        tdf = DictDiffer(b, a)

        self.assertEqual(tdf.nb_changes(), 0)

    def test_nb_changes_full(self):
        """Number of changes
        """
        a = {'a': 1, 'b': 1}
        b = {'d': 1, 'f': 1}
        tdf = DictDiffer(b, a)

        self.assertEqual(tdf.nb_changes(), 4)

    def test_fulldiff(self):
        """
        """
        a = {'a': 1, 'b': 1, 'c': 4}
        b = {'d': 1, 'f': 1, 'c': 5}
        tdf = DictDiffer(b, a)

        diff = tdf.fulldiff()
        result = {'added': [{'d': 1}, {'f': 1}],
                  'changed': [{'key': 'c', 'old': 4, 'new': 5}],
                  'removed': [{'a': 1}, {'b': 1}]}

        self.assertEqual(diff, result)
