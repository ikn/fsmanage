class HistoryEventResult:
    # .state
    # .result

    SUCCESS = 0
    # failed and successfully reverted
    REVERTED = 1
    # failed, state changed and revert failed
    FAILED = 2

    def __init__ (self, state, result):
        # state is SUCCESS, REVERTED or FAILED
        # result is execute/undo result
        pass


class HistoryEvent:
    # passed to History .on_change() callbacks
    value = None

    def __init__ (self):
        # execute and undo return HistoryEventResult
        pass

    def execute (self):
        # returns Future with HistoryEventResult result
        # this does nothing
        pass

    def can_undo (self):
        # always true
        pass

    def undo (self):
        # should raise TypeError if can't, returns Future with HistoryEventResult result
        # this does nothing
        pass


class History:
    # .permanent
    # .max_events
    # .expire_future_first
    # .max_event_age
    # .events
    # .position - index in .events we're before

    # execute waits for executing to finish if non-permanent

    # type of expected events
    event_type = HistoryEvent

    def __init__ (self, permanent=False, max_events=None,
                  expire_future_first=False, max_event_age=None,
                  current_time=None):
        # permanent: don't support undo/redo
        # current_time: function to give the current time as a number
        # expire_future_first: whether to expire 'future' events before past events
        # never expires future by time
        pass

    @property
    def past (self):
        # immutable sequence of events in the past
        pass

    @property
    def future (self):
        # immutable sequence of events in the future
        pass

    def add (self, event, time=None):
        # raise TypeError if event type is not event_type
        # runs event.execute(), returns HistoryEventResult
        # time is used for expiry
        #  * should be a number comparable to current_time
        #  * defaults to getting the current time
        pass

    def can_undo (self):
        pass

    def undo (self):
        # raises TypeError if can't, returns Future with HistoryEventResult result
        pass

    def can_redo (self):
        pass

    def redo (self):
        # raises TypeError if can't, returns Future with HistoryEventResult result
        pass

    def clear (self):
        # just delete all events, don't run anything
        pass

    def on_change (self, *fns):
        # call functions with event.value when latest event changes
        pass

    def expire_events (self):
        # run expiry routines
        pass
