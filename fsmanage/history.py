import time


class HistoryEventResult:
    """The result of a change to history.

:arg state: indicates whether the change succeeded: :attr:`SUCCESS`,
    :attr:`REVERTED` or :attr:`FAILED`.
:arg result: the actual result of the execution function
    (:meth:`HistoryEvent.execute` or :meth:`HistoryEvent.undo`).

"""

    #: History change was successful.
    SUCCESS = 0
    #: History change failed, and all intermediate changes were reverted.
    REVERTED = 1
    #: History change failed, and some intermediate changes might not have been
    #: reverted.
    FAILED = 2

    def __init__ (self, state, result):
        #: ``state`` argument
        self.state = None
        #: ``result`` argument
        self.result = None


class HistoryEvent:
    """Represents a change in history.

Knows how to make (and possibly revert) the change.

"""

    #: Whether the change associated with this event can be undone.
    can_undo = True

    def __init__ (self):
        pass

    def execute (self):
        """Make the change associated with this event.

:returns: :attr:`future <fsmanage.opexec.OperationExecutor.future_type>` whose
    result is a :class:`HistoryEventResult`.

This implementation does nothing.

"""
        pass

    def undo (self):
        """Undo the change associated with this event, if possible.

Should raise :class:`TypeError` if this is not possible (and :attr:`can_undo`
should be :obj:`False`).

:returns: :attr:`future <fsmanage.opexec.OperationExecutor.future_type>` whose
    result is a :class:`HistoryEventResult`.

This implementation does nothing.

"""
        pass


class History:
    """Manage a history of events.

:arg permanent: if :obj:`True`, changes to this history are irreversible,
    regardless of :attr:`HistoryEvent.can_undo`.
:arg max_events: if given, this restricts the maximum number of saved events
    (accessed through :attr:`past`, :meth:`undo`, etc.) to this many.
:arg expire_future_first: if ``max_events`` is specified, this determines which
    events to remove first - if ``True``, those in :attr:`future` (used via
    :meth:`redo`) are removed before those in :attr:`past`.
:arg max_event_age: if given, remove events which were last executed (or
    reverted) this long ago (according to ``current_time``).  This means that
    this may cause expiry of :attr:`future` events.  Removal occurs when a
    change is made (:meth:`add`, :meth:`undo`, etc.), or through
    :meth:`expire_events`.
:arg current_time: a function that takes no arguments and returns the current
    time as a number.  Only relative times matter, and the magnitude only
    matters as regards ``max_event_age``.
:arg require_reversible: if :obj:`True` and ``permanent`` is :obj:`False`,
    :meth:`add` will raise :class:`TypeError` when the passed ``event`` does
    not support :meth:`undo <HistoryEvent.undo>`.

"""

    # execute waits for executing to finish if non-permanent

    #: The type of events that this history can track (:class:`HistoryEvent`
    #: subclass).
    event_type = HistoryEvent

    def __init__ (self, permanent=False, max_events=None,
                  expire_future_first=False, max_event_age=None,
                  current_time=time.monotonic, require_reversible=False):
        #: ``permanent`` argument.
        self.permanent = None
        #: ``max_events`` argument.
        self.max_events = None
        #: ``expire_future_first`` argument.
        self.expire_future_first = None
        #: ``max_event_age`` argument.
        self.max_event_age = None
        #: ``current_time`` argument.
        self.current_time = None
        #: ``require_reversible`` argument.
        self.require_reversible = None
        #: Current index in :attr:`events` - those before this index are in the
        #: 'past' (have been executed), and those after it are in the 'future'
        #: (have been reverted).
        self.position = None

    @property
    def events (self):
        """Sequence of :class:`HistoryEvent` instances stored in this history.

In execution order.  See also :attr:`position`.

"""
        # immutable
        pass

    @property
    def past (self):
        """Sequence of :class:`HistoryEvent` instances that are in the 'past'.

``history.past`` is equivalent to ``history.events[:history.position]``.

"""
        # immutable
        pass

    @property
    def future (self):
        """Sequence of :class:`HistoryEvent` instances that are in the
'future'.

``history.future`` is equivalent to ``history.events[history.position:]``.

"""
        # immutable
        pass

    def add (self, event):
        """Add an event to the history.

:arg event: :class:`HistoryEvent` to add; :meth:`execute
    <HistoryEvent.execute>` is called.

:returns: :attr:`future <fsmanage.opexec.OperationExecutor.future_type>` whose
    result is a :class:`HistoryEventResult` from executing the event.

:raises TypeError: if ``event`` is not of type :attr:`event_type`; or if
    :attr:`permanent` is :obj:`False`, :attr:`require_reversible` is
    :obj:`True` and ``event`` does not support :meth:`undo
    <HistoryEvent.undo>`.

"""
        pass

    def can_undo (self):
        """Return whether there is something that can be undone.

Note that a subsequent call to :meth:`undo` is not guaranteed to succeed - this
function should only really be used when you do not intend to undo anything
(eg. to indicate whether undo is possible in a user interface).

"""
        pass

    def undo (self):
        """Try to undo the most recently executed event.

This is the last event in :attr:`past`.

:returns: :attr:`future <fsmanage.opexec.OperationExecutor.future_type>` whose
    result is a :class:`HistoryEventResult` from undoing the event.

:raises TypeError: if this is not possible - if there are no events to undo, or
    if the most recently executed event cannot be undone.

"""
        pass

    def can_redo (self):
        """Return whether there is something that can be redone.

See :meth:`can_undo` for usage notes.

"""
        pass

    def redo (self):
        """Try to redo the most recently reverted event.

This is the first event in :attr:`future`.

:returns: :attr:`future <fsmanage.opexec.OperationExecutor.future_type>` whose
    result is a :class:`HistoryEventResult` from redoing the event.

:raises TypeError: if there are no events to redo.

"""
        pass

    def on_change (self, *fns):
        """Register functions for calling when an event change occurs.

:arg fns: any number of functions to register as callbacks.  Whenever an event
    is executed or reverted, each of these is called like
    ``fn(event, result)``, where:

        - ``event`` is the :class:`HistoryEvent` which did something.
        - ``result`` is the :class:`HistoryEventResult` from the call.

"""
        pass

    def expire_events (self):
        """Check the age of known events and expire old ones.

See also :attr:`max_event_age`.

Note that expiry is also performed whenever an event change happens.

"""
        pass
