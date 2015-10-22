from functools import partial
import os
import subprocess

from dulwich.repo import Repo
import pytest
from tinydb import TinyDB
from tinydb_git import JSONGitStorage
import volatile


@pytest.yield_fixture()
def repo_dir():
    with volatile.dir() as dtmp:
        subprocess.check_call(['git', 'init', dtmp])
        yield dtmp


@pytest.fixture()
def repo(repo_dir):
    return Repo(repo_dir)


@pytest.fixture()
def db_factory(repo_dir):
    return partial(TinyDB, repo_dir, storage=JSONGitStorage)


@pytest.fixture()
def db(db_factory):
    return db_factory()


def test_repo_fixture(repo_dir):
    assert os.path.exists(os.path.join(repo_dir, '.git'))


def test_backend_simple(db):
    pass


def test_read_write(db_factory):
    db1 = db_factory()
    assert not db1.all()

    db1.insert({'type': 'apple', 'count': 7})
    db1.insert({'type': 'peach', 'count': 3})
    all1 = db1.all()

    assert len(all1) == 2
    assert all1[0] == {'type': 'apple', 'count': 7}
    assert all1[1] == {'type': 'peach', 'count': 3}

    db2 = db_factory()
    all2 = db2.all()

    assert len(all2) == 2
    assert all2[0] == {'type': 'apple', 'count': 7}
    assert all2[1] == {'type': 'peach', 'count': 3}


def test_writes_parent(repo, db):
    db.insert({'a': 1})

    commit = repo[db._storage._refname]
    parent_id = commit.id
    # initial commit will also have a parent, containing the empty database

    db.insert({'b': 1})
    commit = repo[db._storage._refname]

    assert commit.parents == [parent_id]
