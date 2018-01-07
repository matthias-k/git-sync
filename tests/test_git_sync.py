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


@pytest.fixture
def local_commited_changes(repo):
    repo.pypath.join('file4').write('local testcontent4')
    repo.call('git add file4')
    repo.call('git commit -m debugcommit')
    return repo


@pytest.fixture
def local_uncommited_changes(repo):
    repo.pypath.join('file1').write('local testcontent2')
    repo.pypath.join('file2').write('local testcontent3')
    return repo


@pytest.fixture
def upstream_changes(repo2):
    repo2.pypath.join('file3').write('remote testcontent')
    repo2.automatic_commit()
    repo2.call('git add file3')
    repo2.call('git push')
    return repo2


def test_commits_trivial(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    head = repo.HEAD
    repo.automatic_commit()
    assert repo.is_clean()
    assert repo.HEAD == head


def test_commits_new_files(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    head = repo.HEAD
    repo.pypath.join('file2').write('testcontent2')
    assert not repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()
    assert repo.HEAD != head


def test_commits_changed_files(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    head = repo.HEAD
    repo.pypath.join('file1').write('testcontent2')
    assert not repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()
    assert repo.HEAD != head


def test_commits_removed_files(repo):
    assert repo.pypath.join('file1').check()
    assert repo.is_clean()
    head = repo.HEAD
    repo.pypath.join('file1').remove()
    assert not repo.is_clean()
    repo.automatic_commit()
    assert repo.is_clean()
    assert repo.HEAD != head


def test_auto_sync_only_local(repo, bare_repo, local_uncommited_changes):
    old_head = repo.HEAD
    repo.auto_sync()
    new_head = repo.HEAD
    assert new_head != old_head
    assert bare_repo.HEAD == new_head


def test_auto_sync_only_remote(repo, bare_repo, upstream_changes):
    old_local_head = repo.HEAD
    old_remote_head = bare_repo.HEAD
    assert old_local_head != old_remote_head
    repo.auto_sync()
    assert bare_repo.HEAD == old_remote_head, "remote did not change"
    assert repo.HEAD == bare_repo.HEAD, "local is now as upstream"


def test_auto_sync_local_and_remote(repo, bare_repo, local_uncommited_changes, upstream_changes):
    old_local_head = repo.HEAD
    old_remote_head = bare_repo.HEAD
    assert old_local_head != old_remote_head
    repo.auto_sync()
    assert bare_repo.HEAD != old_remote_head, "remote changed"
    assert repo.HEAD != old_local_head, "remote changed"
    assert repo.HEAD == bare_repo.HEAD, "local is now as upstream"


# test pull and merge: success
# test pull and merge: fail cleans up correctly

# test pushes to master if possible
# test pushes to conflict1 if not possible
# test pushes to conflict2 if conflict1 conflicting too

# test notifications
