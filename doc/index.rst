fsmanage documentation
======================

Documentation for ``fsmanage``, a Python library containing filesystem
management tools.

- version: ``0-next``
- dependencies: Python 3.3 or later 3.x
- home page: http://ikn.org.uk/fsmanage

This package contains tools for writing filesystem management interfaces for
arbitrary filesystem implementations.  It should be flexible enough to support
any sort of interface, but is aimed at long-running programs (for example, an
application, as opposed to a one-shot command like ``cp`` or ``mv``).

The top-level package contains all core objects - everything from
:mod:`item <fsmanage.item>`, :mod:`history <fsmanage.history>`,
:mod:`operation <fsmanage.operation>`, :mod:`opexec <fsmanage.opexec>`,
:mod:`action <fsmanage.action>` and :mod:`actionexec <fsmanage.actionexec>`.

Items
-----

:class:`Item <fsmanage.item.Item>` instances are just for referring to files.
They don't provide much information (path and vague type, eg. file/directory),
and don't allow querying for more information or changing the files they refer
to.

Whenever a path is used instead of an item, it is a sequence of string path
components (like :attr:`Item.path <fsmanage.item.Item.path>`).

History
-------

A :class:`History <fsmanage.history.History>` represents a series of changes to
a system, implemented as :class:`HistoryEvent <fsmanage.history.HistoryEvent>`
instances.  When an event is added, it is 'executed' to change the state of the
system tracked by the history, and, if successful, is stored in the history's
event list.

Implements:

- undo/redo.
- expiry of old events.
- asynchronous event execution via any method.
- waiting for each event to finish before executing the next one.

Operations
----------

An :class:`Operation <fsmanage.operation.Operation>` represents a change to the
filesystem, usually to a single item.  For example: move, copy, delete.

The actual filesystem is implemented by supporting the execution of operations
in an :class:`OperationExecutor <fsmanage.opexec.OperationExecutor>` subclass.
This might, for example, be an in-memory filesystem, the standard system
filesystem, or a filesystem within an archive file.  An operation executor
allows handling confirmations (such as overwriting files) through callbacks.

Managing the execution of many operations is done with a subclass of
:class:`OperationManager <fsmanage.opexec.OperationManager>`, which uses a
:class:`History <fsmanage.history.History>` to do so.  This might, for example,
run operations in series, in multiple threads, or on other computers.

Actions
-------

An :class:`Action <fsmanage.action.Action>` represents a way a user might want
to interact with the filesystem, and might represent one or more operations, or
a query that doesn't cause any changes, or might not even touch the filesystem.
For example: cut, paste, open, undo.  Executing an action requires an
:class:`OperationManager <fsmanage.opexec.OperationManager>`.

Actions operate on targets, each type of which is represented by an
:class:`ActionTarget <fsmanage.action.ActionTarget>` - for example, some subset
of filesystem items, or the current working directory.  When an action's
targets do not match the current system, the action cannot be run.

To group the actions you want to provide together and run them more easily, you
can use an :class:`ActionManager <fsmanage.actionexec.ActionManager>`.  This
will not support any actions until the targets required by the actions are
supported - for example, :func:`action_manager_support_selection
<fsmanage.actionexec.action_manager_support_selection>` allows using actions
that operate on filesystem items.

Modules
-------

- :ref:`index of names <genindex>`

.. toctree::
   :maxdepth: 2

   item
   history
   operation
   opexec
   action
   actionexec
