from .item import ROOT
from .history import HistoryEvent, History


class ActionManager:
    """Group together actions and manage running them.

:arg op_manager: :class:`OperationManager <fsmanage.opexec.OperationManager>`
    to run operations with.

To make actions available for executing, call :meth:`add_actions`.

"""

    def __init__ (self, op_manager):
        #: ``op_manager`` argument.
        self.operation_manager = None
        #: :class:`set` of :class:`Action <fsmanage.action.Action>` subclasses
        #: supported; call :meth:`add_actions` to add more.
        self.supported_actions = None

    def support_target (self, target, get_context):
        """Add support for a type of :class:`ActionTarget
<fsmanage.action.ActionTarget>`.

:arg target: :class:`ActionTarget <fsmanage.action.ActionTarget>` subclass to
    support.
:arg get_context: function that takes no arguments and returns the current
    context for ``target``.

If this target is already supported, ``get_context`` overrides the function
previously registered.

Whenever you call this function, you should also set up calls to
:meth:`context_changed` for the target's context.

"""
        pass

    def context_changed (self, target):
        """Notify this action manager that the context for a target type has
changed.

:arg target: :class:`ActionTarget <fsmanage.action.ActionTarget>` subclass for
    which the context has changed.

:raises TypeError: if ``target`` is not a supported target type.

This should be called for every change, if possible.

"""
        # lets us know the context for the target changed
        pass

    def on_context_update (self, fn, *actions):
        """Register a callback function for changes to the context of any of an
action's targets.

:arg fn: function called on every context change, as ``fn(action, matches)``,
    where:

        - ``action`` is the :class:`Action <fsmanage.action.Action>` subclass
          in question.
        - ``matches`` is a boolean, the result of calling
          :class:`Action.context_matches_target
          <fsmanage.action.Action.context_matches_target>` on ``action``.
:arg actions: :class:`Action <fsmanage.action.Action>` subclasses to register
    callbacks for.

If ``fn`` is registered twice as the handler for the same action type, it will
still only be called once for each context change.

:raises TypeError: if any action in ``actions`` is not a supported action type.

"""
        # triggered by .context_changed calls
        pass

    def add_actions (self, *actions):
        """Make actions available for executing via :meth:`execute`.

:arg actions: :class:`Action <fsmanage.action.Action>` subclasses to add.

:raises TypeError: if the action cannot be supported for any reason (see
    below).

If an action type has already been added, adding it again has no effect.

For an action to be supported, it needs support for:

- operations it uses in :attr:`operation_manager`.
- :class:`targets <fsmanage.action.ActionTarget>` it specifies.  When created,
  an :class:`ActionManager` doesn't support any targets - to add some, call
  :meth:`support_target`.  Support for targets and contexts defined in
  ``fsmanage`` can be added using the ``action_manager_support_*`` functions in
  this module.

"""
        # instantiates actions when storing
        pass

    def rm_actions (self, *actions):
        """Remove support for actions.

:arg actions: :class:`Action <fsmanage.action.Action>` subclasses to remove.

If an action type has not been added, removing it has no effect.

"""
        # removes functions added through on_context_update
        pass

    def execute (self, action):
        """Run an action.

:arg action: :class:`Action <fsmanage.action.Action>` subclass to execute.

:raises ValueError: if ``action`` is not supported.

"""
        # calls action.context_matches_target then .execute if matches
        pass

    def attention (self, attn_type, items):
        # attn_type: AttentionItems.CHANGED/MARKED
        pass


def action_manager_support_selection (manager):
    """Add support for selections to an :class:`ActionManager`.

Supports: :class:`ItemActionTarget <fsmanage.action.ItemActionTarget>`.

A selection is a group of items which are marked for use by an action.

:arg manager: :class:`ActionManager` instance.

:returns: function to call with any number of :class:`Item
    <fsmanage.item.Item>` instances to set them as the currently selected
    items.

"""
    pass


def action_manager_support_state (manager):
    """Add support for generic state storage to an :class:`ActionManager`.

Supports: :class:`StateActionTarget <fsmanage.action.StateActionTarget>`.

The state is a :class:`dict`.

:arg manager: :class:`ActionManager` instance.

"""
    pass


class NavigationHistoryEvent (HistoryEvent):
    """History event corresponding to a change to the current directory.

:arg path_before: path (like :attr:`NavigationHistory.cwd`) before the change.
:arg path_after: path after the change.

"""

    def __init__ (self, path_before=None, path_after=None):
        #: ``path_before`` argument.
        self.path_before = None
        #: ``path_after`` argument.
        self.path_after = None


class NavigationHistory (History):
    """History specifically for navigation within a filesystem.

:arg root: determines what items are in the top-level directory; this can be:

    - a path (sequence of strings giving path components) to use the items in a
      directory at that path.
    - a sequence of paths use the items at those paths.

Other arguments are as taken by :class:`History <fsmanage.history.History>`.

"""

    #: :attr:`History.event_type <fsmanage.history.History.event_type>`.
    event_type = NavigationHistoryEvent

    def __init__ (self, root=(), *args, **kwargs):
        #: ``root`` argument.
        self.root = None
        #: The current directory (path); :obj:`None` means the top-level
        #: directory (see :attr:`root`).  The initial value is :obj:`None`.
        self.cwd = None

    def navigate (self, path):
        """Change the current directory to the given path."""
        pass


def action_manager_support_navigation (manager, history):
    """Add support for navigation to an :class:`ActionManager`.

Supports: :class:`NavigationHistoryActionTarget
<fsmanage.action.NavigationHistoryActionTarget>`.

:arg manager: :class:`ActionManager` instance.
:arg history: :class:`NavigationHistory` instance to use for storing changes to
    the current directory.

"""
    pass
