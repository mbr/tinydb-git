from functools import partial
import os
import subprocess

from dulwich.repo import Repo
import pytest
from tinydb import TinyDB
from tinydb_git.json import JSONGitStorage
from tinydb_git.yaml import YAMLGitStorage
from tinyrecord import transaction
import volatile


@pytest.yield_fixture()
def repo_dir():
    with volatile.dir() as dtmp:
        subprocess.check_call(['git', 'init', dtmp])
        yield dtmp


@pytest.fixture()
def repo(repo_dir):
    return Repo(repo_dir)


@pytest.fixture(params=['yaml', 'json'])
def db_factory(request, repo_dir):
    if request.param == 'json':
        return partial(TinyDB, repo_dir, storage=JSONGitStorage)
    if request.param == 'yaml':
        return partial(TinyDB, repo_dir, storage=YAMLGitStorage)
    assert False, 'unreachable'


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


def test_single_commit_per_transaction(repo, db):
    db.insert({'a': 1})
    # 2 commits so far, one for intializations, one for adding insert

    commit = repo[db._storage._refname]
    parent_commit = repo[commit.parents[0]]

    assert parent_commit.parents == []

    # create transction with 3 inserts, this should return into a single
    # new commit
    with transaction(db.table('_default')) as t:
        t.insert({'b': 2})
        t.insert({'c': 3})
        t.insert({'d': 4})

    latest = repo[db._storage._refname]
    assert latest.parents == [commit.id]
