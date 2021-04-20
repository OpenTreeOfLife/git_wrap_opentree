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
        all_c = self.cgr.commits_after()
        recent = self.cgr.commits_after(after_sha='b81559ac853219345fd2a893641fd6226b851792')
        init_two = self.cgr.commits_after(until_sha='b81559ac853219345fd2a893641fd6226b851792')
        self.assertEqual(all_c, init_two + recent)

    def testFilesChanged(self):
        init_two = self.cgr.commits_after(until_sha='b81559ac853219345fd2a893641fd6226b851792')
        fc = list(self.cgr.files_touched(init_two[1]))
        self.assertEqual(len(fc), 1)
        ffc = fc[0]
        self.assertEqual(ffc[0], 'git_wrap_opentree/__init__.py')
        self.assertEqual(str(ffc[1]), 'a9324baad960d032b8bd3400a323539d7e594ed8')

    def testGetFileContents(self):
        init_two = self.cgr.commits_after(until_sha='b81559ac853219345fd2a893641fd6226b851792')
        oid = list(self.cgr.files_touched(init_two[1]))[0][1]
        fc = self.cgr.get_file_contents(oid)
        self.assertEqual(_FC_EXP, fc)

_FC_EXP = u'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple utility functions used by Open Tree python code.

These function are used by packages that descend from peyotl, but
do not depend on any part of peyotl.
"""
from __future__ import absolute_import, print_function, division

__version__ = '0.0.1a'  # sync with setup.py

from .git_repo import ConstGitRepo


__all__ = ['git_repo', 
           'test', 
           ]
'''

if __name__ == "__main__":
    unittest.main()
