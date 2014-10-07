import abc

from .history import HistoryEvent, History


class OperationHistoryEvent (HistoryEvent):
    # .operation

    # handles CONFIRM_ALL behaviour over all ops
    # whether to attempt revert is specified by failure_behaviour

    def __init__ (self, execute, op, confirm, allow_parallel=True,
                  undo_yields_attention=False):
        # allow_parallel: if false, waits between each _execute call
        # undo_yields_attention: whether .undo() calls also give AttentionItems
        pass

    def execute (self):
        # calls execute('execute', op, confirm)
        # returns Future with OperationException exception
        pass

    def can_undo (self):
        pass

    def undo (self):
        # calls execute('undo', op)
        # returns Future with OperationException exception
        pass


class OperationHistory (History):
    event_type = OperationHistoryEvent


class OperationExecutor (metaclass=abc.ABCMeta):
    # .supported_operations

    # runs single operations

    def __init__ (self):
        pass

    def support_operation (self, op, execute, undo=None):
        # add support for operation as execute and undo functions
        pass

    def can_undo (self, op):
        pass

    @abc.abstractmethod
    def execute (self, op, confirm):
        # op is Operation instance
        # runs operation with given args and returns Future with AttentionItems/OperationException
        # confirm is called with Confirmation and responds with action to take (Confirmation.SUCCESS, etc.)
        pass

    @abc.abstractmethod
    def undo (self, op):
        # runs reverse of executing op and returns Future with AttentionItems/OperationException
        # raises TypeError if can't undo this operation
        pass

    @abc.abstractmethod
    def get_metadata (self, item, *properties):
        # empty properties means get all available metadata
        # returns Future with {property: value}
        # Dir should support 'items' property which gives list of items in it
        # needs to support Dir item type, plus any returned in 'items' property
        # needs to support properties required by actions used
        # properties are missing where they can't be determined (eg. item doesn't exist)
        pass


class OperationManager (metaclass=abc.ABCMeta):
    # .executor
    # .supported_operations
    # .history
    # .failure_behaviour
    # .undo_yields_attention

    # eg. could run in series or parallel, with asyncio, threading or multiprocessing, or offloading to another service
    # to undo/redo, use .history

    REVERT_CURRENT = 0
    # leaves inconsistent state as is
    DO_NOTHING = 1
    REVERT_GROUP = 2

    def __init__ (self, executor, ops, history,
                  failure_behaviour=REVERT_CURRENT,
                  undo_yields_attention=False):
        # ops are operation subclasses
        # history is OperationHistory; raise ValueError if non-empty
        # undo_yields_attention: taken by OperationHistoryEvent
        # raise TypeError for op not supported by executor
        pass

    @abc.abstractmethod
    def _execute (self, action, *args):
        # just calls executor.{execute,undo,get_metadata}(*args) using chosen method
        # returns Future with executor's result and OperationException exception
        pass

    def get_metadata (self, item, properties):
        # calls _execute('get_metadata', item, properties)
        # note: don't need to wrap anything like with execute
        pass

    def execute (self, ops, confirm=None, allow_parallel=True):
        # raises TypeError for unsupported op
        # confirm=None means always confirm
        # handles failure_behaviour
        # call history.add with OperationHistoryEvent(self._execute, ops, confirm, allow_parallel, undo_yields_attention)
        # returns Future with executor's result and OperationException exception
        pass
