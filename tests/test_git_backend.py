import os
import subprocess

from dulwich.repo import Repo
import pytest
import volatile


@pytest.yield_fixture()
def repo_dir():
    with volatile.dir() as dtmp:
        subprocess.check_call(['git', 'init', dtmp])
        yield dtmp


@pytest.fixture()
def repo(repo_dir):
    return Repo(repo_dir)


def test_repo_fixture(repo_dir):
    assert os.path.exists(os.path.join(repo_dir, '.git'))
