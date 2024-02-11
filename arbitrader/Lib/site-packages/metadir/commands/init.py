import os
import sys
import yaml
import json
import pickle
import pprint
from .base import Base
from .utils import dir_metatree

"""The init command."""


class Init(Base):

    def run(self):

        data = dir_metatree(
            _ROOT_=self.options.get('<path>') or '.',
            ignore_dot_files=not self.options.get('--all')
        )

        # as_string = yaml.dump(data, allow_unicode=True)
        as_string = pprint.pformat(data)

        # content = '# FORMAT\n```yaml\n{}```'.format(as_string)
        content = '{}```'.format(as_string)

        print(content)
