#!/bin/env python3
from datetime import datetime

from executor import execute, ExternalCommandFailed
import py

SUCCESS = 'success'
CONFLICT = 'conflict'


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
        self.call('git push {} HEAD:{}'.format(remote, remote_branch), silent=True)

    def pull(self, remote='origin', remote_branch='master'):
        self.call('git pull --no-edit {} {}'.format(remote, remote_branch), capture=True, silent=True)


    def try_pull(self, remote='origin', remote_branch='master'):
        try:
            self.pull(remote=remote, remote_branch=remote_branch)
            return True
        except ExternalCommandFailed as e:
            command = e.command
            output = command.decoded_stdout
            if 'CONFLICT' in output:
                return False
            raise


    def auto_sync(self):
        """perform full auto sync cycle"""
        self.automatic_commit()
        merge_success = self.try_pull()
        if merge_success:
            self.push()
            return {'status': SUCCESS, 'remote_branch': 'master'}
        else:
            self.push(remote_branch='conflict1')
            return {'status': CONFLICT, 'remote_branch': 'conflict1'}

    def call(self, cmd, capture=False, silent=True):
        return execute(cmd, directory=self.directory, capture=capture, silent=silent)

    @property
    def pypath(self):
        return py.path.local(self.directory)
