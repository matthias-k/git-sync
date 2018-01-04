import pytest
from executor import execute

import gitsync

@pytest.fixture
def new_repo(tmpdir):
    execute('git init', directory=str(tmpdir), silent=True)
    return tmpdir

@pytest.fixture
def repo(new_repo):
    new_repo.join('file1').write('testcontent')
    execute('git add .', directory=str(new_repo), silent=True)
    execute('git commit -m commit1', directory=str(new_repo), silent=True)
    return new_repo


def test_commits_new_files(repo):
    assert repo.join('file1').check()
    assert gitsync.check_repository(str(repo))
    repo.join('file2').write('testcontent2')
    assert not gitsync.check_repository(str(repo))
    gitsync.commit_repository(str(repo))
    assert gitsync.check_repository(str(repo))


def test_commits_changed_files(repo):
    assert repo.join('file1').check()
    assert gitsync.check_repository(str(repo))
    repo.join('file1').write('testcontent2')
    assert not gitsync.check_repository(str(repo))
    gitsync.commit_repository(str(repo))
    assert gitsync.check_repository(str(repo))


def test_commits_removed_files(repo):
    assert repo.join('file1').check()
    assert gitsync.check_repository(str(repo))
    repo.join('file1').remove()
    assert not gitsync.check_repository(str(repo))
    gitsync.commit_repository(str(repo))
    assert gitsync.check_repository(str(repo))

#def test_commits_changed_files(repo):
#    assert 0

#def test_commits_deleted_files(repo):
#    assert 0

# test pull and merge: success
# test pull and merge: fail cleans up correctly

# test pushes to master if possible
# test pushes to conflict1 if not possible
# test pushes to conflict2 if conflict1 conflicting too

# test notifications
