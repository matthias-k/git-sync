# git-sync

`git-sync` is a tool to automatically keep a git repository in sync with its remote. It's main intended usecase is for smartphones
(e.g. via termux), where you might want to syncronize text files with git but where it's cumbersome to do so manually and where it's even
more cumbersume to deal with merge conflicts.

`git-sync`'s way of dealing with merge conflicts is to push the local version to a new remote `conflict1` branch and let the user
resolve the merge conflict whereever it is most convenient (usually you local machine). As long as master conflicts, `git-sync` will
push to `conflict1` unless this is conflicting too. Then it will push to `conflict2` and so on. This guarantees that no data is lost.

`git-sync` supports user notifications in case of successfull pushes, pulls, merges or conflicts.

## Setup

```
pkg upgrade
pkg install git
pkg install openssh
pkg install python
```


