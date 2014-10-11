import abc


class ActionTarget (metaclass=abc.ABCMeta):
    """A target for an :class:`Action`.

An action is executed 'on' a target - a target instance represents a set of
conditions for the action to run.  A target is associated with a 'context',
which is the source of information needed to determine if the conditions are
met.

"""

    @abc.abstractmethod
    def context_matches (context, op_manager):
        """Determine if this actions conditions are met.

:arg context: information needed to match against conditions - depends on the
    subclass.
:arg op_manager: :class:`OperationManager <fsmanage.opexec.OperationManager>`
    to be used if necessary.

:returns: :attr:`future_type <fsmanage.opexec.OperationExecutor.future_type>`
    whose result is a boolean indicating whether the context matches.

"""
        pass


class ItemActionTarget (ActionTarget):
    """Target which is satisfied based on the selected items.

:arg item_filter: :class:`ItemFilter <fsmanage.item.ItemFilter>` to check for
    matches.  If :obj:`None`, a filter which matches any item is used.

The context is a sequence of :class:`Item <fsmanage.item.Item>` instances,
which are the 'selected' items - items the user has somehow chosen to execute
an action on.  It matches if all items match ``item_filter``.

"""

    def __init__ (self, item_filter=None):
        pass

    def context_matches (self, items):
        """:inherit:"""
        pass


class SingleItemActionTarget (ItemActionTarget):
    """Target which is satisfied based on a single selected item.

Arguments and context are as for :class:`ItemActionTarget`.

The context matches if exactly one item is selected and it matches
``item_filter``.

"""

    def context_matches (self, items):
        """:inherit:"""
        pass


class StateActionTarget (ActionTarget):
    """Target which is satisfied based on a generic state storage.

:arg properties: sequence of property names in the state needed to check the
    target conditions; must be hashable.
:arg match_state: function that takes the context and returns whether it
    matches this target.  By default, it always matches.

The context is a :class:`dict` with keys from ``properties`` and values from
the state.  When passed to :meth:`Action.execute`, modifications to the
required properties should be reflected in further usages of the state.

"""

    def __init__ (self, properties, match_state=None):
        #: ``properties`` argument.
        self.properties = None

    def context_matches (self, state):
        """:inherit:"""
        pass


class NavigationHistoryActionTarget (ActionTarget):
    """Target which is satisfied based on navigation history.

:arg match_history: function that takes the history and returns whether it
    matches this target.  By default, it always matches.

The context is a :class:`NavigationHistory
<fsmanage.actionexec.NavigationHistory>` instance; the same instance should be
used across all actions.

"""

    def __init__ (self, match_history=None):
        pass

    def context_matches (self, history):
        """:inherit:"""
        pass


class CwdActionTarget (NavigationHistoryActionTarget):
    """Target which is satisfied based on the current directory.

:arg item_filter: :class:`ItemFilter <fsmanage.item.ItemFilter>` to match
    against the current directory.  If :obj:`None`, a filter which matches any
    item is used.

Context is as for :class:`NavigationHistoryActionTarget`.  It matches if
:attr:`cwd <fsmanage.actionexec.NavigationHistory.cwd>` is a :class:`Dir
<fsmanage.item.Dir>` and matches ``item_filter``.  It doesn't match if the
current directory is the history :attr:`root
<fsmanage.actionexec.NavigationHistory.root>` and the root is a sequence of
items.

"""

    def __init__ (self, item_filter=None):
        # filter is always &&'d with Dir check
        #: ``item_filter`` argument.
        self.item_filter = None

    def context_matches (self, history):
        """:inherit:"""
        # gets cwd from history (what to do with None?)
        # use item filter matching
        pass


class Action (metaclass=abc.ABCMeta):
    """Represents a user interaction with the filesystem.

:arg manager: :class:`ActionManager <fsmanage.actionexec.ActionManager>`
    instance managing this action.

An action might run some operations, or just query for information, or not
touch the filesystem itself at all.  Actions don't finish and respond with
results, they just have effects - usually interacting with the ``manager``.

"""

    def __init__ (self, manager):
        #: ``manager`` argument.
        self.manager = None

    @property
    @abc.abstractmethod
    def name (self):
        """Lower-case name for the action."""
        pass

    @property
    @abc.abstractmethod
    def operations (self):
        """Sequence of :class:`Operation <fsmanage.operation.Operation>`
subclasses used this type of action.

These are the operations that must be supported by the
:class:`OperationExecutor <fsmanage.opexec.OperationExecutor>` made available
to :meth:`execute`.

"""
        pass

    @property
    @abc.abstractmethod
    def target (self):
        """Sequence of :class:`ActionTarget` instances used by this type of
action.

These are the targets used to determine if this action can be run.

"""
        pass

    @staticmethod
    def context_matches_target (op_manager, *target_contexts):
        """Determine if this action can be run.

:arg op_manager: :class:`OperationManager <fsmanage.opexec.OperationManager>`
    to be used if necessary.
:arg target_contexts: sequence of contexts matching up with the  :attr:`target`
    sequence.

:returns: :attr:`future_type <fsmanage.opexec.OperationExecutor.future_type>`
    whose result is a boolean.

An action can be run if all contexts match their corresponding targets.

"""
        pass

    @abc.abstractmethod
    def execute (self, op_manager, *target_contexts):
        """Determine if this action can be run.

:arg op_manager: :class:`OperationManager <fsmanage.opexec.OperationManager>`
    to be used if necessary.
:arg target_contexts: sequence of contexts matching up with the  :attr:`target`
    sequence.

Implementations should not assume (or check) that the contexts match the
targets because of parallelism issues - instead, they should just try to run
and handle any errors.

"""
        # may return as soon as the operations have been queued
        # calls ActionManager.attention
        pass
