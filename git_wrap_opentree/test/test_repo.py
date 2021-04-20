#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import logging
from git_wrap_opentree import ConstGitRepo
from git_wrap_opentree.test.support.pathmap import get_test_path_mapper as ntest_path_mapper
import os

pathmap = ntest_path_mapper()

_LOG = logging.getLogger(__name__)

class TestConstGitRepo(unittest.TestCase):
    def setUp(self):
        self.cgr = None
        pkg = os.path.realpath(pathmap.package_dir)
        self.repo_top = os.path.split(pkg)[0]
        gd = os.path.join(self.repo_top, '.git')
        if os.path.isdir(gd):
            self.cgr = ConstGitRepo(git_dir=gd)
        else:
            self.skipTest('not being run from git-checked out source')
            return

    def testInit(self):
        rtcgr = ConstGitRepo(repo_top=self.repo_top)
        self.assertEqual(rtcgr.git_dir, self.cgr.git_dir)
        bcgr = ConstGitRepo(repo_top=self.repo_top, git_dir=self.cgr.git_dir)
        self.assertEqual(bcgr.git_dir, self.cgr.git_dir)
        self.assertRaises(ValueError, ConstGitRepo, repo_top=self.cgr.git_dir)
        self.assertRaises(ValueError, ConstGitRepo)
        grand_par = os.path.split(self.repo_top)[0]
        self.assertRaises(ValueError, ConstGitRepo, repo_top=grand_par,
                                                    git_dir=self.cgr.git_dir)

    def testCommitsAfter(self):    
        print(self.cgr.commits_after())

if __name__ == "__main__":
    unittest.main()
