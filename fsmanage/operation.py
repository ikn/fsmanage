import abc


class Operation (metaclass=abc.ABCMeta):
    # op should be something that changes metadata of an item
    # always perform the simplest case, eg. operate on one item
    # subclass doc says what AttentionItems should be for execute and undo
    #  * should be new/changed items that still exist

    @abc.abstractmethod
    def __init__ (self):
        # subclasses take args for running
        #  * eg. copy takes (src: OperableItem, dest: path)
        #  * and expose them for use by executor
        pass

    @property
    @staticmethod
    @abc.abstractmethod
    def name ():
        pass


class OperationException (Exception):
    # .operation
    # .reverted

    def __init__ (self, op, reverted=True):
        # reverted: bool, whether there's anything to undo
        pass


class Confirmation (metaclass=abc.ABCMeta):
    CONFIRM = 0
    REJECT = 1
    # works per Confirmation subclass in a group of operations
    CONFIRM_ALL = 2

    def __init__ (self, respond):
        # respond: function to call with response
        pass

    @property
    @abc.abstractmethod
    def description (self):
        pass

    def respond (self, action):
        # action is CONFIRM, REJECT or CONFIRM_ALL
        pass
