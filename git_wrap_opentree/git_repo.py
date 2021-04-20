#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ConstGitRepo is a base class containing methods that specify
repo-specific information, but no methods that alter the state
of the repository. This includes methods that just read from
the git db. They do not checkout, or switch branches...


"""
import pygit2
import os

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

    @property
    def git_dir(self):
        return self._git_dir

    @property
    def repo_top(self):
        return self._repo_top

    def commits_after(self, sha=None):
        # if sha is None:
        #     sha = repo.head.target
        for c in self._repo.walk():
            print(c)
    
    