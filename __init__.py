"""fsmanage: filesystem management tools.

Version: 0-next.

Requires Python 3.3 or later 3.x.

This package contains tools for writing filesystem management interfaces for
arbitrary filesystem implementations.  It should be flexible enough to support
any sort of interface, but is aimed at long-running programs (for example, an
application, as opposed to a one-shot command like 'cp' or 'mv').

Usage is split between operations and actions:

 - An operation causes a change to the filesystem, usually to a single item,
   and is implemented by an OperationExecutor.  For example: move, copy,
   delete.  If you want to work with options, you probably want to use an
   OperationManager.

 - An action represents a way a user might want to interfact with the
   filesystem, and might represent one or more operations, or a query that
   doesn't cause any changes.  For example: cut, paste, open, undo.  If you
   want to work with actions, you probably want to use an ActionManager.

"""

"""

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License, version 3, as published by the
Free Software Foundation.

If this was not included, it can be found here:
    http://www.gnu.org/licenses/gpl-3.0.txt

"""

"""

todo
----

 * full documentation, and sphinx with makefile
    * split out enums into separate classes?

to get something working
 * the code
 * basic implementations of functions/abstract classes, including __str__/__repr__

for GCEdit
 * needed implementations of functions/abstract classes
 * searching (like gcutil; also by metadata, in-file search, limited depth)
    * needs to be async like opmgr
 * sorting - eg. natural sort, dirs first...
 * qt

implementations
---------------

render_path
    render_path(root, sep)
    render_path_posix
    render_path_windows

Operation
    Copy
    Move
    Delete

Confirmation
    Overwrite(item, with=None)
    Delete(item)

OperationExecutor
    FilesystemOperationExecutor(root=real root)
    MemoryOperationExecutor(tree) # track changes somehow - maybe items have IDs

OperationManager
    SynchronousOperationManager
    AsyncioOperationManager
    ThreadedOperationManager
    MultiprocessingOperationManager

Action
    Cut
    Copy
    Paste
    Delete
    Undo
    Redo
    NavigateInto (open dir)
    NavigateUp
    NavigateBack
    NavigateForwards
    Remove (from this view - only for toplevel, with custom root)

ActionManager.attention
    change selection to be/include them
    tie them to an action execution somehow, and do things like
     * only use if action execution was recent
     * only use if no other actions were executed since

future
------

 * other implementations of functions/abstract classes
 * for lots of arguments taking instances, default is None to create (a specific type of) one with default args

 * progress reporting (and events for start/stop operations - maybe also events for progress from any operation?)
 * cancelling/pausing operations
 * transparent archives - open as dirs
 * OperationManager: can set max number of running operations
 * retry behaviour for operations
 * metadata caching (how to expire?)
 * links (Link(OperableItem), Link(Operation), Link(Action))
 * can intercept and handle confirmations in ActionManager
 * operation manager exposes running operations and current progress
 * history
    * has optional branching behaviour - .redo([branch=most recent])
    * more flexible expiry methods
        * pass sequence of HistoryExpiration which each determine when to expire an event
    * put in separate package
 * qt metadata viewer/editor (action: 'properties' or something)
 * qt History viewer/editor (events need icon and text)

"""
