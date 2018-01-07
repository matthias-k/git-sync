import pytest
from executor import execute

import gitsync


@pytest.fixture
def new_repo(tmpdir):
    repo_path = tmpdir.mkdir('tmp_repo')
    repo = gitsync.Repository(str(repo_path))
    repo.call('git init')
    return repo


@pytest.fixture
def tmp_repo(new_repo):
    new_repo.pypath.join('file1').write('testcontent')
    new_repo.call('git add .')
    new_repo.call('git commit -m commit1')
    return new_repo


@pytest.fixture
def bare_repo(tmp_repo, tmpdir):
    bare_path = tmpdir.join('bare_repo.git')
    execute('git clone --bare {} {}'.format(tmp_repo.directory, bare_path))
    return gitsync.Repository(str(bare_path))


def test_bare_repo(bare_repo):
    assert bare_repo.pypath.join('config').check()


@pytest.fixture
def repo(bare_repo, tmpdir):
    repo_path = tmpdir.join('repo')
    execute('git clone {} {}'.format(bare_repo.directory, repo_path))
    return gitsync.Repository(str(repo_path))


@pytest.fixture
def repo2(bare_repo, tmpdir):
    repo_path = tmpdir.join('repo2')
    execute('git clone {} {}'.format(bare_repo.directory, repo_path))
    return gitsync.Repository(str(repo_path))


def test_commits_trivial(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()


def test_commits_new_files(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    repo.pypath.join('file2').write('testcontent2')
    assert not repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()


def test_commits_changed_files(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    repo.pypath.join('file1').write('testcontent2')
    assert not repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()


def test_commits_removed_files(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    repo.pypath.join('file1').remove()
    assert not repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()

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
