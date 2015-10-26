from __future__ import absolute_import

from tinydb.database import Element
import yaml

from . import GitStorage


# using a SafeDumper causes no tags to be written, which is much easier on the
# eyes, however it means we need to add a representer for the TinyDB database
# element:
class TinyDBDumper(yaml.SafeDumper):
    pass


TinyDBDumper.add_representer(Element, TinyDBDumper.represent_dict)


class YAMLGitStorage(GitStorage):
    ENCODING = 'utf8'

    def __init__(self,
                 repo_path,
                 branch=b'master',
                 filename=b'tinydb.yaml',
                 yaml_dumper=TinyDBDumper):
        super(YAMLGitStorage, self).__init__(repo_path, branch, filename)
        self.dumper_class = yaml_dumper

    def _serialize(self, data):
        return yaml.dump(data,
                         Dumper=self.dumper_class,
                         indent=2,
                         default_flow_style=False,
                         encoding=self.ENCODING)

    def _deserialize(self, raw):
        return yaml.load(raw.decode(self.ENCODING))
