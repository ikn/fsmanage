import abc

from .history import HistoryEvent, History


class OperationHistoryEvent (HistoryEvent):
    """History event corresponding to the execution of a group of operations.

:arg run: function to call to execute or undo a single operation; the function
    signature is the same as :meth:`OperationManager.run`.
:arg ops: sequence of :class:`Operation <fsmanage.operation.Operation>`
    instances to use.
:arg confirm: confirmation function as taken by
    :meth:`OperationManager.execute`.
:arg allow_parallel: whether the operations may be executed or reverted out of
    order or at the same time.
:arg undo_yields_attention: whether :meth:`undo` passes through the
    :class:`AttentionItems <fsmanage.item.AttentionItems>` instance returned by
    ``run`` (if :obj:`False`, it always returns one with no items).

"""

    # handles CONFIRM_ALL behaviour over all ops

    def __init__ (self, run, ops, confirm, allow_parallel=True,
                  undo_yields_attention=False):
        #: ``ops`` argument.
        self.operations = None

    def execute (self, revert_on_failure):
        """:meth:`HistoryEvent.execute
<fsmanage.history.HistoryEvent.execute>`.

Returned future is from :meth:`OperationExecutor.execute`.

"""
        # calls run('execute', op, confirm)
        pass

    def can_undo (self):
        """:inherit:"""
        pass

    def undo (self):
        """:meth:`HistoryEvent.undo <fsmanage.history.HistoryEvent.undo>`.

Returned future is from :meth:`OperationExecutor.undo`.

"""
        # calls run('undo', op)
        pass


class OperationHistory (History):
    """History specifically for operations."""

    #: :attr:`History.event_type <fsmanage.history.History.event_type>`.
    event_type = OperationHistoryEvent


class OperationExecutor (metaclass=abc.ABCMeta):
    """Implements execution of operations and querying of items.

This is an abstract class and may not be instantiated - all actual operation
implementations are in subclasses.

"""

    def __init__ (self):
        pass

    @property
    @abc.abstractmethod
    def future_type (self):
        """Type of futures returned by :meth:`execute`, :meth:`undo` and
:meth:`get_metadata`.

Must support at least the ``add_done_callback``, ``set_result``,
``set_exception``, ``result`` and ``exception`` properties of
:class:`concurrent.futures.Future`.

"""
        pass

    @property
    def supported_operations (self):
        """Set of :class:`Operation <fsmanage.operation.Operation>` subclasses
supported by this executor."""
        pass

    def support_operation (self, op, execute, undo=None):
        """Add support for an operation type.

:arg op: :class:`Operation <fsmanage.operation.Operation>` subclass to support.
:arg execute: execution function for the operation; has the same signature as
    :meth:`execute`.
:arg undo: optional undo function for the operation; has the same signature as
    :meth:`undo`.  If :obj:`None`, operations of this type cannot be undone.

This adds ``operation`` to :attr:`supported_operations`.  If the operation is
already supported, ``execute`` and ``undo`` override existing values.

"""
        pass

    def can_undo (self, op):
        """Return whether undo is supported for operations of a particular
type.

:arg op: :class:`Operation <fsmanage.operation.Operation>` subclass to check.

Note that if this function returns :obj:`True`, a subsequent call to
:meth:`undo` is not guaranteed to succeed - this function should only really be
used when you do not intend to undo anything (eg. to indicate whether undo is
possible in a user interface).

"""
        pass

    def execute (self, op, confirm):
        """Execute an operation.

:arg op: :class:`Operation <fsmanage.operation.Operation>` instance to execute.
:arg confirm: function to be called with a :class:`Confirmation
    <fsmanage.operation.Confirmation>` instance whenever there is a question
    for the user; a response is required.

:returns: :attr:`future_type` whose result is an :class:`AttentionItems
    <fsmanage.item.AttentionItems>` instance and whose exception is an
    :class:`OperationException <fsmanage.operation.OperationException>`.

:raises TypeError: if ``op`` is not in :attr:`supported_operations`.

"""
        pass

    def undo (self, op):
        """Undo an operation, if possible.

:arg op: :class:`Operation <fsmanage.operation.Operation>` instance to execute.

:returns: :attr:`future_type` whose result is an :class:`AttentionItems
    <fsmanage.item.AttentionItems>` instance and whose exception is an
    :class:`OperationException <fsmanage.operation.OperationException>`.

:raises TypeError: if ``op`` is not in :attr:`supported_operations`, or if undo
    is not supported for operations of ``op``'s type.

"""
        pass

    @abc.abstractmethod
    def get_metadata (self, item, *properties):
        """Retrieve metadata about an item in the filesystem.

:arg item: :class:`Item <fsmanage.item.Item>` instance to query.
:arg properties: names of properties to query.  Supported properties are
    dependent on the implementation, but these should always be supported:

        - ``items``, for :class:`Dir <fsmanage.item.Dir>` instances, should be
          a sequence of :class:`Item <fsmanage.item.Item>` instances
          'contained' in the directory.

:returns: :attr:`future_type` whose result is a :class:`dict` with keys from
    ``properties`` giving the metadata.  If the value of a property cannot be
    determined for any reason, it is omitted from the result.

"""
        pass


class OperationManager (metaclass=abc.ABCMeta):
    """Manage the execution of operations.

:arg executor: :class:`OperationExecutor` to use.
:arg history: :class:`OperationHistory` to use.
:arg undo_yields_attention: as taken by :class:`OperationHistoryEvent`.

This is an abstract class and may not be instantiated - subclasses should
implement :meth:`run`, eg. for multi-threaded execution.

To undo and redo, use methods of :attr:`history`.

"""
    # to undo/redo, use .history

    def __init__ (self, executor, history, undo_yields_attention=False):
        #: ``executor`` argument.
        self.executor = None
        #: ``history`` argument.
        self.history = None
        #: ``undo_yields_attention`` argument.
        self.undo_yields_attention = None

    @abc.abstractmethod
    def run (self, action, *args):
        """Execute something using :attr:`executor`.

:arg action: action to perform - a string corresponding to an
    :class:`OperationExecutor` method: ``'execute'``, ``'undo'`` or
    ``'get_metadata'``.
:arg args: arguments taken by the :class:`OperationExecutor` method
    corresponding to ``action``.

:returns: :attr:`future_type <OperationExecutor.future_type>` as returned by
    the called method.  If the method raises any other exception (quite
    possibly :class:`TypeError`), return a future containing it.

Abstract method - must be implemented by subclasses.

"""
        pass

    def get_metadata (self, item, *properties):
        """Like :meth:`OperationExecutor.get_metadata`."""
        # calls run('get_metadata', item, properties)
        pass

    def execute (self, ops, confirm=None, allow_parallel=True):
        """Execute a group of operations.

:arg ops: sequence of :class:`Operation fsmanage.operation.Operation`
    instances; adding them together places them in the same
    :class:`OperationHistoryEvent`, so they are grouped for :meth:`undo
    <fsmanage.history.History.undo>`.
:arg confirm: confirmation function as taken by
    :class:`OperationExecutor.execute`.  If :obj:`None`, the response is always
    :attr:`Confirmation.CONFIRM_ALL
    <fsmanage.operation.Confirmation.CONFIRM_ALL>`.

:returns: result of :meth:`OperationExecutor.execute`.

:raises TypeError: if the operation is not supported.

"""
        # call history.add with OperationHistoryEvent(self.run, ops, confirm, allow_parallel, undo_yields_attention)
        pass
