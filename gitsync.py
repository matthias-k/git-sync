#!/bin/env python3
from datetime import datetime

from executor import execute
import py


class Repository(object):
    def __init__(self, directory):
        self.directory = directory

    def status(self):
        return self.call('git status', capture=True, silent=False)

    def is_clean(self):
        output = self.status()
        clean_output = output.lower()
        return 'nothing to commit' in clean_output and 'working tree clean' in clean_output

    def automatic_commit(self):
        self.call('git add .')
        self.call('git commit -m "automatic commit {}"'.format(datetime.utcnow()))

    def call(self, cmd, capture=False, silent=True):
        return execute(cmd, directory=self.directory, capture=capture, silent=silent)

    @property
    def pypath(self):
        return py.path.local(self.directory)
