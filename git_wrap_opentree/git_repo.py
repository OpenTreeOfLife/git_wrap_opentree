#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ConstGitRepo is a base class containing methods that specify
repo-specific information, but no methods that alter the state
of the repository. This includes methods that just read from
the git db. They do not checkout, or switch branches...


"""
import pygit2
import os

_EMPTY_TREE_OID = None
_EMPTY_OID = None
def empty_tree_oid(repository=None):
    global _EMPTY_TREE_OID
    if _EMPTY_TREE_OID is None:
        _EMPTY_TREE_OID = repository.TreeBuilder().write()
    return _EMPTY_TREE_OID

def null_oid():
    global _EMPTY_OID
    if _EMPTY_OID is None:
        _EMPTY_OID = pygit2.Oid(hex='0000000000000000000000000000000000000000')
    return _EMPTY_OID

class ConstGitRepo(object):
    def __init__(self, repo_top=None, git_dir=None):
        self._repo_top = None
        self._git_dir = None
        if repo_top is None:
            if git_dir is None:
                raise ValueError('"repo_top" or "git_dir" must be specified.')
            agd = os.path.abspath(git_dir)
            rt, gd = os.path.split(agd)
            if gd != '.git':
                m = "Expecting git_dir to end with .git, but found {}"
                raise ValueError(m.format(git_dir))
            self._repo_top = rt
            self._git_dir = agd
        else:
            rf = os.path.abspath(repo_top)
            gd = os.path.join(rf, '.git')
            if (git_dir is not None) and (gd != os.path.abspath(git_dir)):
                m = '"repo_top" ({}) and "git_dir" ({}) both specified, but they disagree.'
                raise ValueError(m.format(repo_top, git_dir))
            self._repo_top = rf
            self._git_dir = gd
        if not os.path.isdir(self.git_dir):
            raise ValueError('Expected git_dir "{}" to be a directory'.format(self.git_dir))
        self._repo = pygit2.Repository(self.git_dir)
        empty_tree_oid(self._repo)

    @property
    def git_dir(self):
        return self._git_dir

    @property
    def repo_top(self):
        return self._repo_top

    def commits_after(self, after_sha=None, until_sha=None):
        """Returns commits (after_sha, until_sha].

        Sorted oldest to newest.
        If after_sha is None, it defaults to the initial commit.
        If until_sha is None, it defaults to the HEAD.
        """
        if after_sha is not None:
            after_sha = after_sha.strip()
            if not after_sha:
                after_sha = None
        if not until_sha:
            until_sha = self._repo.head.target
        r = []
        for c in self._repo.walk(until_sha, pygit2.GIT_SORT_TIME):
            if after_sha is not None and str(c.id).startswith(after_sha):
                break
            r.append(c)
        return r[::-1]
    
    
    def files_touched(self, commit):
        """Returns an iterable of pairs of (path-from-top, object ids) of files
        changed by a commit.

        object id O
        will be returned if a file is removed.
        """
        if commit.parents:
            par_list = commit.parents
        else:
            par_list = [empty_tree_oid()]
        new_oid_set = set()
        for p in par_list:
            diff = self._repo.diff(p, commit)
            for dd in diff.deltas:
                new_oid_set.add((dd.new_file.path, dd.new_file.id))
        return new_oid_set

    def get_file_contents(self, oid, encoding='utf-8'):
        if oid == null_oid():
            return ''
        return self._repo.get(oid).data.decode(encoding)
