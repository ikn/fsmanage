class Item:
    def __init__ (self, path):
        # path is tuple of strings
        pass

    @property
    def path (self):
        pass


class Dir (Item):
    pass


ROOT = Dir(())


def OperableItem (Item):
    def __init__ (self, name, parent):
        pass

    @property
    def path (self):
        return self.parent.path + (self.name,)


class OperableDir (Dir, OperableItem):
    pass


class File (OperableItem):
    pass


def match_item_name (pattern):
    # pattern: exact name or regex
    # returns item filter function
    pass


def match_item_path (pattern, render_path):
    # pattern: exact path or regex
    # render_path(path) -> string to match against
    # returns item filter function
    pass


def match_item_metadata (prop, pattern):
    # pattern: exact value or regex
    # returns item filter function
    pass


class ItemFilter:
    def __init__ (self, match):
        # match is Item subclass and items match if they are subclasses of it
        # or match(item, op_manager) -> bool
        # or match(item, op_manager) -> Future(bool)
        # eg. match_item_*
        pass

    def match (self, item, op_manager):
        # returns Future with bool result
        pass

    # these ops do collapsing based on operation already in self/other
    # other can be arg to init (need __ror__/__rand__?)
    def __or__ (self, other):
        pass

    def __and__ (self, other):
        pass


class AttentionItems:
    # .parent
    # .items

    # new/changed items - those from executor
    CHANGED = 0
    # items marked for further usage by actions - like cut
    MARKED = 1

    def __init__ (self, parent, items=()):
        # eg. delete just gives parent
        pass
