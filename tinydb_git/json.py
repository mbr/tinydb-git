from __future__ import absolute_import

import json

from . import GitStorage


class JSONGitStorage(GitStorage):
    def __init__(self, repo_path, branch=b'master', filename=b'tinydb.json'):
        super(JSONGitStorage, self).__init__(repo_path, branch, filename)

    def _serialize(self, data):
        return json.dumps(data, sort_keys=True, indent=2).encode('utf8')

    def _deserialize(self, raw):
        return json.loads(raw.decode('utf8'))
