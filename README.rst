tinydb-git
==========

A storage backend for tinydb that stores database changes inside a git
branch.

``tinydb-git`` lets you use any branch in a git repository as a backend for
tinydb_.

.. code-block:: sh

    hiro@wintermute:tmp$ git init example
    Initialized empty Git repository in /tmp/example/.git/

Every modification of the database results in a new commit:

.. code-block:: pycon

    >>> import tinydb
    >>> from tinydb_git import JSONGitStorage
    >>> db = tinydb.TinyDB('example', storage=JSONGitStorage)
    >>> db.insert({'text': 'first record'})
    1

.. code-block:: sh

    hiro@wintermute:example$ git log
    commit de9a07844783b8e420fce6f9568e126dd7779e74

        Updated by tinydb-git 0.1.dev1

    commit 3b31825cf312cb5d42f792998faddf20b634c7d9

        Updated by tinydb-git 0.1.dev1

Multiple ``insert()`` calls result in a commit for each call. This can be
avoided by using a tinyrecord_ transaction:

.. code-block:: pycon

    >>> from tinyrecord import transaction
    >>> with transaction(db.table('_default')) as t:
    ...         t.insert({'b': 2})
    ...         t.insert({'c': 3})
    ...         t.insert({'d': 4})
    ...
    >>>

The result:

.. code-block:: sh

    hiro@wintermute:example$ git log
    commit e02a3af06d7cd7eeb6990277777cc24d384249e8

        Updated by tinydb-git 0.1.dev1

    commit de9a07844783b8e420fce6f9568e126dd7779e74

        Updated by tinydb-git 0.1.dev1

    commit 3b31825cf312cb5d42f792998faddf20b634c7d9

        Updated by tinydb-git 0.1.dev1

Internally, data gets stored as json, with ``sort_keys=True`` and ``indent=2``,
to make diffs pleasant to read and help with compression:

.. code-block:: sh

    hiro@wintermute:example$ git diff master^ master
    diff --git a/tinydb.json b/tinydb.json
    index a27ff44..d9711f0 100644
    --- a/tinydb.json
    +++ b/tinydb.json
    @@ -2,6 +2,15 @@
       "_default": {
         "1": {
           "text": "first record"
    +    },
    +    "2": {
    +      "b": 2
    +    },
    +    "3": {
    +      "c": 3
    +    },
    +    "4": {
    +      "d": 4
         }
       }
     }
    \ No newline at end of file


.. _tinydb: http://tinydb.readthedocs.org/
.. _tinyrecord: https://github.com/eugene-eeo/tinyrecord
