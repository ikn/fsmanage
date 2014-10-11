"""fsmanage: filesystem management tools.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License, version 3, as published by the
Free Software Foundation.

If this was not included, it can be found here:
    http://www.gnu.org/licenses/gpl-3.0.txt

"""

"""

todo
----

 * full documentation
    * better overview - mention all main classes and their basic role
 * check everything returning future_type has access to OperationExecutor

to get something working
 * the code
 * basic implementations of functions/abstract classes
 * tests
 * -> ikn

for GCEdit
 * needed implementations of functions/abstract classes
    * mention ones where you only use one alternative in index.rst
 * searching (like gcutil; also by metadata, in-file search, limited depth)
    * needs to be async like opmgr
 * sorting - eg. natural sort, dirs first...
 * qt

 * __str__/__repr__ implementations
 * full examples in documentation
 * internationalisation

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
    AsyncioOperationManager (requires Python 3.4)
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
 * retry behaviour for operations
 * metadata caching (how to expire?)
 * links (Link(OperableItem), Link(Operation), Link(Action))
 * can intercept and handle confirmations in ActionManager
 * operation manager exposes running operations and current progress
 * history
    * something to handle HistoryActionResult.FAILED - option to reject all work if this happens?
    * can set max number of running events
        * events can contribute more than 1
        * move support for event groups and allow_running to History
    * has optional branching behaviour - .redo([branch=most recent])
    * more flexible expiry methods
        * pass sequence of HistoryExpiration which each determine when to expire an event
    * put in separate package
    * can initialise .events/.position on creation
 * qt metadata viewer/editor (action: 'properties' or something)
 * qt History viewer/editor (events need icon and text)

"""
