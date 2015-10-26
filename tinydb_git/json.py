from __future__ import absolute_import

import json

from . import GitStorage


class JSONGitStorage(GitStorage):
    def _serialize(self, data):
        return json.dumps(data, sort_keys=True, indent=2).encode('utf8')

    def _deserialize(self, raw):
        return json.loads(raw.decode('utf8'))
