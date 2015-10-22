import time

from dulwich.repo import Repo
from dulwich.objects import Commit, Tree, Blob
from tinydb.storages import Storage


__version__ = '0.1.dev1'


class JSONGitStorage(Storage):
    def __init__(self, repo_path, branch='master', filename='tinydb.json'):
        self.branch = branch
        self.filename = filename

        if '/' in filename:
            raise NotImplementedError(
                'Currently, subdir support is not implemented. Annoy the '
                'author on github to get it done.')

        self.repo = Repo(repo_path)

    @property
    def _refname(self):
        return b'refs/heads/' + self.branch

    def _serialize(self, data):
        return b'meep'

    def _deserialize(self, raw):
        return {}

    def read(self):
        try:
            commit = self.repo[self._refname]
            tree = self.repo[commit.tree]
            blob = self.repo[tree[self.filename][1]]
        except KeyError:
            raise ValueError

        return self._deserialize(str(blob))

    def write(self, data):
        commit = Commit()

        # commit metadata
        author = b"tinydb"
        commit.author = commit.committer = author
        commit.commit_time = commit.author_time = int(time.time())
        tz = time.timezone if (time.localtime().tm_isdst) else time.altzone
        commit.commit_timezone = commit.author_timezone = tz
        commit.encoding = b"UTF-8"
        commit.message = b"Updated by tinydb-git {}".format(__version__)

        # prepare blob
        blob = Blob.from_string(self._serialize(data))

        try:
            branch_sha = self.repo[self.branch]
        except KeyError:
            # branch does not exist, start with an empty tree
            tree = Tree()
        else:
            raise NotImplementedError

        # no subdirs in filename, add directly to tree
        tree.add(self.filename, 0o100644, blob.id)

        commit.tree = tree.id

        # add objects
        self.repo.object_store.add_object(blob)
        self.repo.object_store.add_object(tree)
        self.repo.object_store.add_object(commit)

        # update refs
        self.repo.refs[self._refname] = commit.id

    def close(self):
        raise NotImplementedError
