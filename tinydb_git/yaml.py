from __future__ import absolute_import

import yaml

from . import GitStorage


class YAMLGitStorage(GitStorage):
    ENCODING = 'utf8'

    def __init__(self, repo_path, branch=b'master', filename=b'tinydb.yaml'):
        super(YAMLGitStorage, self).__init__(repo_path, branch, filename)

    def _serialize(self, data):
        return yaml.dump(data,
                         indent=2,
                         default_flow_style=False,
                         encoding=self.ENCODING)

    def _deserialize(self, raw):
        return yaml.load(raw.decode(self.ENCODING))
