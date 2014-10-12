import re
from unittest import TestCase

import fsmanage as fs

test_path = ('first', 'second', 'third')


class Item (TestCase):
    def setUp (self):
        self.item = fs.Item(test_path)

    def test_path (self):
        self.assertEqual(self.item.path, test_path)


class ItemEquality (TestCase):
    def test_equal (self):
        self.assertEqual(fs.Item(test_path), fs.Item(test_path))

    def test_different_paths (self):
        self.assertNotEqual(fs.Item(test_path), fs.Item(('a', 'b')))

    def test_non_item (self):
        self.assertNotEqual(fs.Item(test_path), test_path)


class ItemListPath (TestCase):
    def setUp (self):
        self.item = fs.Item(list(test_path))

    def test_path (self):
        """Should convert path to tuple."""
        self.assertEqual(self.item.path, test_path)


class ItemInvalidPath (TestCase):
    def test_create (self):
        self.assertRaises(TypeError, fs.Item, 5)


class Dir (TestCase):
    def test_create (self):
        fs.Dir(test_path)


class Root (TestCase):
    def test_type (self):
        self.assertIsInstance(fs.ROOT, fs.Dir)

    def test_path (self):
        self.assertEqual(fs.ROOT.path, ())


class OperableItem (TestCase):
    def setUp (self):
        self.item = fs.OperableItem(test_path)

    def test_parent (self):
        self.assertEqual(self.item.parent, ('first', 'second'))

    def test_name (self):
        self.assertEqual(self.item.name, 'third')


class OperableItemSinglePathComponent (TestCase):
    def setUp (self):
        self.item = fs.OperableItem(('name',))

    def test_parent (self):
        self.assertEqual(self.item.parent, ())

    def test_name (self):
        self.assertEqual(self.item.name, 'name')


class OperableItemEmptyPath (TestCase):
    def test_create (self):
        self.assertRaises(ValueError, fs.OperableItem, ())


class OperableDir (TestCase):
    def test_create (self):
        fs.OperableDir(test_path)


class File (TestCase):
    def test_create (self):
        fs.File(test_path)


#class MatchItemName (TestCase):
    #def setUp (self):
        #self.match = fs.match_item_name('matching name')

    #def test_match (self):
        #item = fs.OperableItem(('parent', 'matching name'))
        #self.assertTrue(self.match(item))

    #def test_no_match (self):
        #item = fs.OperableItem(('parent', 'non-matching name'))
        #self.assertFalse(self.match(item))

    #def test_not_operable (self):
        #"""Should not match with non-operable item."""
        #item = fs.Item(('parent', 'matching name'))
        #self.assertFalse(self.match(item))

    #def test_not_item (self):
        #"""Should not match with non-item."""
        #self.assertFalse(self.match('matching name'))


#class MatchItemNameRegex (TestCase):
    #def setUp (self):
        #self.match = fs.match_item_name(re.compile(r'\.txt$'))

    #def test_match (self):
        #item = fs.OperableItem(('parent', 'matching name.txt'))
        #self.assertTrue(self.match(item))

    #def test_no_match (self):
        #item = fs.OperableItem(('parent', 'non-matching name.txt.bak'))
        #self.assertFalse(self.match(item))


#class MatchItemPath (TestCase):
    #def setUp (self):
        #self.match = fs.match_item_path(
            #('matching', 'path'), lambda path: path[0])

    #def test_match (self):
        #item = fs.Item(('matching', 'path'))
        #self.assertTrue(self.match(item))

    #def test_render_match (self):
        #"""Should use render_path."""
        #item = fs.Item(('matching', 'other path'))
        #self.assertTrue(self.match(item))

    #def test_no_match (self):
        #item = fs.Item(('non-matching', 'path'))
        #self.assertFalse(self.match(item))

    #def test_not_item (self):
        #"""Should not match with non-item."""
        #self.assertFalse(self.match(('matching', 'path')))


#class MatchItemPathRendered (TestCase):
    #def setUp (self):
        #self.match = fs.match_item_path('matching', lambda path: path[0])

    #def test_match (self):
        #item = fs.Item(('matching', 'path'))
        #self.assertTrue(self.match(item))

    #def test_no_match (self):
        #item = fs.Item(('non-matching', 'path'))
        #self.assertFalse(self.match(item))


#class MatchItemPathRegex (TestCase):
    #def setUp (self):
        #self.match = fs.match_item_path(
            #re.compile(r'a/b'), lambda path: '/'.join(path))

    #def test_match (self):
        #item = fs.OperableItem(('thing a', 'b thing'))
        #self.assertTrue(self.match(item))

    #def test_no_match (self):
        #item = fs.OperableItem(('other', 'path'))
        #self.assertFalse(self.match(item))


class AttentionItems (TestCase):
    def setUp (self):
        self.attn = fs.AttentionItems(
            (fs.Item(('a', 'one')), fs.Item(('a', 'two'))),
            fs.Item(('parent',)))

    def test_items (self):
        self.assertEqual(self.attn.items,
                         (fs.Item(('a', 'one')), fs.Item(('a', 'two'))))

    def test_parent (self):
        self.assertEqual(self.attn.parent, fs.Item(('parent',)))


class AttentionItemsDefaults (TestCase):
    def setUp (self):
        self.attn = fs.AttentionItems()

    def test_items (self):
        self.assertEqual(self.attn.items, ())

    def test_parent (self):
        self.assertEqual(self.attn.parent, None)


class AttentionItemsExtension (TestCase):
    def test_items_union (self):
        attn1 = fs.AttentionItems((fs.Item(('one',)), fs.Item(('two',))))
        attn2 = fs.AttentionItems((fs.Item(('two',)), fs.Item(('three',))))
        self.assertCountEqual(
            attn1.extended(attn2).items,
            (fs.Item(('one',)), fs.Item(('two',)), fs.Item(('three',))))

    def test_parent_both_missing (self):
        attn = fs.AttentionItems().extended(fs.AttentionItems())
        self.assertEqual(attn.parent, None)

    def test_parent_one_missing (self):
        attn1 = fs.AttentionItems(parent=fs.Item(('parent',)))
        attn2 = fs.AttentionItems()
        self.assertEqual(attn1.extended(attn2).parent, fs.Item(('parent',)))
        self.assertEqual(attn2.extended(attn1).parent, fs.Item(('parent',)))

    def test_parent_both_present (self):
        attn1 = fs.AttentionItems(parent=fs.Item(('parent', 'one')))
        attn2 = fs.AttentionItems(parent=fs.Item(('parent', 'two')))
        self.assertEqual(attn1.extended(attn2).parent,
                         fs.Item(('parent', 'two')))
