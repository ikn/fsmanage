import re


class Item:
    """Representation of something found in a filesystem tree.

:arg path: sequence of strings representing components in the path that points
    this item is found at.

Just used to represent an item's type and location when querying or
manipulating the real items represented.

This class may be used directly when you don't want to be specific about the
item's type, or its type is unknown and shouldn't matter for what you're doing.

Items are equal to each other if they have the same path.

"""

    def __init__ (self, path):
        #: ``path`` argument.
        self.path = tuple(path)

    def __eq__ (self, other):
        return isinstance(other, Item) and other.path == self.path


class Dir (Item):
    """Item that contains other items."""
    pass


#: The top-level item (:attr:`path <Item.path>` is an empty sequence).
ROOT = Dir(())


class OperableItem (Item):
    """Base class for items that can be changed by
:mod:`operations <fsmanage.operation>`.

:raises ValueError: if ``path`` is an empty sequence.

"""

    def __init__ (self, path):
        # check path is non-empty
        if not path:
            raise ValueError('OperableItem path must be non-empty; got:', path)
        Item.__init__ (self, path)


    @property
    def parent (self):
        """Path to the directory containing this item."""
        return self.path[:-1]

    @property
    def name (self):
        """The last component of :attr:`path <Item.path>`."""
        return self.path[-1]


class OperableDir (Dir, OperableItem):
    """Directory that can be changed."""
    pass


class File (OperableItem):
    """Item that contains binary data."""
    pass


def match_item_name (pattern):
    """Match an :class:`OperableItem`'s :attr:`name <OperableItem.name>`
against a pattern.

match_item_name(pattern) -> item_filter

:arg pattern: exact name to expect, or a :mod:`re` regular expression object to
    search for in the name.

:returns: item filter function as taken by :class:`ItemFilter` that works on
    :class:`OperableItem` instances (returns :obj:`False` for objects of the
    wrong type).


"""
    match = (
        (lambda name: name == pattern)
        if isinstance(pattern, str)
        else (lambda name: pattern.search(name) is not None)
    )

    return lambda item, op_manager: (
        match(item.name) if isinstance(item, OperableItem) else False
    )


def match_item_path (pattern, render_path):
    """Match an :class:`Item`'s :attr:`path <Item.path>` against a pattern.

match_item_path(pattern, render_path) -> item_filter

:arg pattern: exact path (sequence of strings) to expect, exact rendered path
    to expect, or a :mod:`re` regular expression object to search for in the
    rendered path.
:arg render_path: function to use to render a path to a string when comparing
    to strings/regular expressions; takes a sequence of strings and returns a
    string.

:returns: item filter function as taken by :class:`ItemFilter` (returns
    :obj:`False` for objects of the wrong type).

"""
    if isinstance(pattern, str):
        # rendered path
        match = lambda path: path == pattern
    elif hasattr(pattern, '__getitem__') and hasattr(pattern, '__len__'):
        # sequence (path)
        expect_path = render_path(pattern)
        match = lambda path: path == expect_path
    else:
        # regex
        match = lambda path: pattern.search(path) is not None

    return lambda item, op_manager: (
        match(render_path(item.path)) if isinstance(item, Item) else False
    )


def match_item_metadata (prop, pattern):
    """Match an :class:`Item`'s metadata against a pattern.

match_item_metadata(prop, pattern) -> item_filter

Metadata is retrieved using :meth:`OperationExecutor.get_metadata
<fsmanage.opexec.OperationExecutor.get_metadata>`.

:arg prop: property to match against.
:arg pattern: exact value to expect, or a :mod:`re` regular expression object
    to search for in the value.  Missing properties become empty strings.

:returns: item filter function as taken by :class:`ItemFilter` (returns
    :obj:`False` for objects of the wrong type).

"""
    pass


class ItemFilter:
    """Filter :class:`Item` instances.

:arg match: predicate defining how to filter items; this is an :class:`Item`
    subclass to filter for items of that type; or it can be a function called
    like ``match(item, op_manager) -> match_result``, where:

        - ``item`` is the item to match against.
        - ``op_manager`` is an :class:`OperationExecutor
          <fsmanage.opexec.OperationExecutor>` that can be used to query for
          item details.
        - ``match_result`` is a boolean indicating whether ``item`` matches the
          predicate, or a :attr:`future
          <fsmanage.opexec.OperationExecutor.future_type>` whose result is a
          boolean.

    The ``match_item_*`` functions in this module provide functions suitable
    for this argument.

"""

    def __init__ (self, match):
        pass

    def match (self, item, op_manager):
        """Check whether an item matches this filter.

:arg item: the item to match against.
:arg op_manager: :class:`OperationExecutor <fsmanage.opexec.OperationExecutor>`
    to use to query for item details.

:returns: :attr:`future <fsmanage.opexec.OperationExecutor.future_type>` whose
    result is a boolean indicating whether ``item`` matches.

Filters can be combined using binary ``or`` (``a | b``) and ``and``
(``a & b``).

"""
        pass

    def __or__ (self, other):
        pass

    def __and__ (self, other):
        pass


class AttentionItems:
    """Representing a group of items needing attention.

:arg items: the :class:`Item` instances in question.
:arg parent: :class:`Item` representing a location for the items in question -
    this makes sense when the items might not exist, but there is a common link
    between them (usually the :class:`Dir` containing them).

"""

    #: Attention type indicating that the items are recently new or changed
    CHANGED = 0
    #: Attention type that marks the items for use in a future action
    MARKED = 1

    def __init__ (self, items=(), parent=None):
        #: ``items`` argument.
        self.items = tuple(items)
        #: ``parent`` argument.
        self.parent = parent

    def extended (self, other):
        """Return a combination of groups of attention items.

:arg other: :class:`AttentionItems` to extend with.

:returns: :class:`AttentionItems` which is a combination of this instance and
    ``other``.  :attr:`items` attributes are combined by union over paths, and
    :attr:`parent` attributes are combined by using one or the other, with
    ``other`` taking precedence.

"""
        return AttentionItems(tuple({
            item.path: item for item in self.items + other.items
        }.values()), other.parent or self.parent)
