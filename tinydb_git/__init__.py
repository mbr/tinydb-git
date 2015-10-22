import json
import time

from dulwich.repo import Repo
from dulwich.objects import Commit, Tree, Blob
from tinydb.storages import Storage


__version__ = '0.1.dev1'


class JSONGitStorage(Storage):
    def __init__(self, repo_path, branch=b'master', filename=b'tinydb.json'):
        self.branch = branch
        self.filename = filename

        if b'/' in filename:
            raise NotImplementedError(
                'Currently, subdir support is not implemented. Annoy the '
                'author on github to get it done.')

        self.repo = Repo(repo_path)

    @property
    def _refname(self):
        return b'refs/heads/' + self.branch

    def _serialize(self, data):
        return json.dumps(data, sort_keys=True, indent=2).encode('utf8')

    def _deserialize(self, raw):
        return json.loads(raw.decode('utf8'))

    def read(self):
        try:
            commit = self.repo[self._refname]
            tree = self.repo[commit.tree]
            blob = self.repo[tree[self.filename][1]]
        except KeyError:
            raise ValueError

        buf = blob.as_raw_string()
        return self._deserialize(buf)

    def write(self, data):
        commit = Commit()

        # commit metadata
        author = b"tinydb"
        commit.author = commit.committer = author
        commit.commit_time = commit.author_time = int(time.time())
        tz = time.timezone if (time.localtime().tm_isdst) else time.altzone
        commit.commit_timezone = commit.author_timezone = tz
        commit.encoding = b'UTF-8'
        commit.message = ('Updated by tinydb-git {}'.format(__version__)
                          .encode('utf8'))

        # prepare blob
        blob = Blob.from_string(self._serialize(data))

        try:
            parent_commit = self.repo[self._refname]
        except KeyError:
            # branch does not exist, start with an empty tree
            tree = Tree()
        else:
            commit.parents = [parent_commit.id]
            tree = self.repo[parent_commit.tree]

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
