#!/bin/env python3
from datetime import datetime

from executor import execute


def check_repository(directory):
    output = execute('git status', directory=str(directory), capture=True)
    clean_output = output.lower()
    return 'nothing to commit' in clean_output and 'working tree clean' in clean_output


def commit_repository(directory):
    execute('git add .', directory=directory, silent=True)
    execute('git commit -m "automatic commit {}"'.format(datetime.utcnow()), directory=directory, silent=True)
