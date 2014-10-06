import abc


class ActionTarget (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def context_matches (context):
        # return Future with bool result
        pass


class ItemActionTarget (ActionTarget):
    # .item_filter

    def __init__ (self, item_filter=None):
        # filter defaults to always matching
        pass

    def context_matches (self, items):
        # use item filter matching - need all to match
        pass


class SingleItemActionTarget (ItemActionTarget):
    def context_matches (self, items):
        # check have one item
        pass


class StateActionTarget (ActionTarget):
    # .properties

    # generic key-value state storage, eg. for saving what to paste

    def __init__ (self, properties, match_state=None):
        # properties is [str] giving state properties we care about
        # default match_state is always true
        pass

    def context_matches (self, state):
        # use match_state
        pass


class NavigationHistoryActionTarget (ActionTarget):
    def __init__ (self, match_history=None):
        # match_history is function returning bool; default is always true
        pass

    def context_matches (self, history):
        # use match_history
        pass


class CwdActionTarget (NavigationHistoryActionTarget):
    # .item_filter

    def __init__ (self, item_filter=None):
        # filter is always &&'d with Dir check
        pass

    def context_matches (self, history):
        # gets cwd from history (what to do with None?)
        # use item filter matching
        pass


class Action (metaclass=abc.ABCMeta):
    # .manager

    def __init__ (self, manager):
        # manager is ActionManager
        pass

    @property
    @staticmethod
    @abc.abstractmethod
    def name ():
        pass

    @property
    @staticmethod
    @abc.abstractmethod
    def operations ():
        # sequence of operations required by this action
        pass

    @property
    @staticmethod
    @abc.abstractmethod
    def target ():
        # sequence of ActionTarget
        pass

    @staticmethod
    def context_matches_target (op_manager, *target_contexts):
        # gives action 'sensitivity'
        # each context matches up with context_matches argument for targets in .target
        # returns Future with bool result
        pass

    @abc.abstractmethod
    def execute (self, op_manager, *target_contexts):
        # may return as soon as the operations have been queued
        # calls ActionManager.attention
        pass
