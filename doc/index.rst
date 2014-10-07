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

Usage is split between operations and actions:

 - An operation causes a change to the filesystem, usually to a single item,
   and is implemented by an
   :class:`OperationExecutor <fsmanage.opexec.OperationExecutor>`.  For
   example: move, copy, delete.  If you want to work with options, you probably
   want to use an :class:`OperationManager <fsmanage.opexec.OperationManager>`.

 - An action represents a way a user might want to interfact with the
   filesystem, and might represent one or more operations, or a query that
   doesn't cause any changes.  For example: cut, paste, open, undo.  If you
   want to work with actions, you probably want to use an
   :class:`ActionManager <fsmanage.actionexec.ActionManager>`.

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
   core
