from .history import HistoryEvent, History


class ActionManager:
    # .operation_manager
    # .supported_actions

    def __init__ (self, op_manager, actions):
        # calls add_actions with actions
        pass

    def support_target (self, target, get_context):
        # get_context() -> context for ActionTarget subclass `target`
        pass

    def context_changed (self, target, context=None):
        # lets us know the context for the target changed
        # target is ActionTarget subclass
        # should be called for every change, if possible
        pass

    def on_context_update (self, fn, *actions):
        # actions are Action subclasses
        # call fn with (action, matches: bool) when context for action changed
        # triggered by .context_changed calls
        pass

    def add_actions (self, *actions):
        # raise TypeError if op_manager doesn't support op required by action
        # raise TypeError if action target types not supported
        # actions are Action subclasses; instantiates them when storing
        pass

    def rm_actions (self, *actions):
        pass

    def execute (self, action):
        # action is Action subclass
        # raises TypeError for unsupported action
        # calls action.context_matches_target then .execute if matches
        # no return value
        pass

    def attention (self, attention_type, items):
        # attention_type: AttentionItems.CHANGED/MARKED
        pass


def action_manager_support_selection (manager):
    # add selections support to an ActionManager
    # call support_target for ItemActionTarget
    # returns function taking items to set current selection
    pass


def action_manager_support_state (manager):
    # add generic state support to an ActionManager
    # call support_target for StateActionTarget
    pass


class NavigationHistoryEvent (HistoryEvent):
    def __init__ (self, path=None):
        # value is path; None is history.root
        pass


class NavigationHistory (History):
    event_type = NavigationHistoryEvent

    # None is .root
    cwd = None

    def __init__ (self, root=ROOT, *args, **kwargs):
        # root: what to show in toplevel dir
        #  * Dir to show its contents
        #  * [Item] giving contents (eg. for search results)
        pass


def action_manager_support_navigation (manager, history, root=ROOT):
    # add navigation support to an ActionManager
    # call support_target for NavigationHistoryActionTarget
    # history is NavigationHistory; raise ValueError if non-empty
    # root: taken by NavigationHistory
    pass
