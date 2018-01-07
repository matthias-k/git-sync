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

    def rev_parse(self, name):
        return self.call('git rev-parse "{}"'.format(name), capture=True).strip()

    @property
    def HEAD(self):
        return self.rev_parse('HEAD')

    def automatic_commit(self):
        self.call('git add .')
        if not self.is_clean():
            self.call('git commit -m "automatic commit {}"'.format(datetime.utcnow()))

    def push(self, remote='origin', remote_branch='master'):
        self.call('git push {} {}'.format(remote, remote_branch))

    def pull(self, remote='origin', remote_branch='master'):
        self.call('git pull --no-edit {} {}'.format(remote, remote_branch))

    def auto_sync(self):
        """perform full auto sync cycle"""
        self.automatic_commit()
        self.pull()
        self.push()

    def call(self, cmd, capture=False, silent=True):
        return execute(cmd, directory=self.directory, capture=capture, silent=silent)

    @property
    def pypath(self):
        return py.path.local(self.directory)
