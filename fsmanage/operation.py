import abc


class Operation (metaclass=abc.ABCMeta):
    """Represents a change to items in the filesystem.

A successful execution of an operation should always make a change - that means
a change to the metadata of at least one item.  An operation should generally
represent the simplest possible change of this sort - for example, changing
only one item rather than many.

Operations are handled based on their type, so each type of operation should
have a different subclass.  The implementation of an operation is in an
:class:`OperationExecutor <fsmanage.opexec.OperationExecutor>`; the operation
itself should document, for both :meth:`execute
<fsmanage.opexec.OperationExecutor.execute>` and :meth:`undo
<fsmanage.opexec.OperationExecutor.undo>` (if well-defined), what:

- changes it is expected to make to the filesystem.
- :class:`AttentionItems <fsmanage.item.AttentionItems>` it should yield -
  this is generally items that were created or changed.

It is up to the executor implementation to decide whether to support undoing
the operation.

To execute an operation, it is passed to an :class:`OperationExecutor
<fsmanage.opexec.OperationExecutor>`, so it should make available, through
properties or methods, all information required to do this (usually taken by
the operation as constructor arguments).  Logic which may be useful for *any*
filesystem implementation should be implemented in methods of the operation.

"""

    @abc.abstractmethod
    def __init__ (self):
        pass

    @property
    @abc.abstractmethod
    def name ():
        """Lower-case name for the operation."""
        pass


class OperationException (Exception):
    """Raised when execution of an operation fails.

:arg op: :class:`Operation` instance that was executing.
:arg reverted: whether any changes made by the operation have been reverted.
    If :obj:`False`, a successful :meth:`undo
    <fsmanage.opexec.OperationExecutor.undo>` call (if supported) should revert
    these.

"""

    def __init__ (self, op, reverted=True):
        #: ``reverted`` argument.
        self.reverted = None

    def summary (self):
        """Short description string of the error that occurred, as sentences.

Defined for this class as: 'Operation failed: <op.name>.'.

"""
        pass

    def detail (self):
        """Extra error information string to accompany :attr:`summary`.

For example, this might mention items involved, or underlying causes for the
error.  May be :obj:`None` (as is the case for this class).

"""
        pass


class Confirmation (metaclass=abc.ABCMeta):
    """Represents a yes/no question for the user about an operation.

:arg respond: function to be called with the response to the question - one of
    :attr:`CONFIRM`, :attr:`REJECT` or :attr:`CONFIRM_ALL`.

This is an abstract class and may not be instantiated.  The :attr:`CONFIRM_ALL`
response groups by subclass, so each different question should be implemented
using a different subclass.

"""

    #: Answer 'yes' to the question.
    CONFIRM = 0
    #: Answer 'no' to the question.
    REJECT = 1
    #: Answer 'yes' to the question, and to all further instances of the same
    #: question in some group of operations.
    CONFIRM_ALL = 2

    def __init__ (self, respond):
        pass

    @property
    @abc.abstractmethod
    def description (self):
        """A phrasing of the question, as sentences.

- Should only enumerate the choices if :attr:`yes_text` and :attr:`no_text`
  cannot convey sufficient understanding.
- May contain multiple paragraphs (separated by pairs of line breaks).

This is an abstract property - it must be defined by subclasses.

"""
        pass

    @property
    @abc.abstractmethod
    def yes_text (self):
        """Title-case string for the option corresponding to
:attr:`CONFIRM`."""
        pass

    @property
    @abc.abstractmethod
    def no_text (self):
        """Title-case string for the option corresponding to
:attr:`REJECT`."""
        pass

    def respond (self, action):
        """Respond to this question.

:attr:`CONFIRM`, :attr:`REJECT` or :attr:`CONFIRM_ALL`.

:raises TypeError: if this method has already been called for this instance.

"""
        pass
