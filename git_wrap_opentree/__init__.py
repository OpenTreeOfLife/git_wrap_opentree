#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple utility functions used by Open Tree python code.

These function are used by packages that descend from peyotl, but
do not depend on any part of peyotl.
"""
from __future__ import absolute_import, print_function, division

__version__ = '0.0.1a'  # sync with setup.py

import pygit2
import os

from .git_repo import ConstGitRepo



def path_blob_pairs_in_tree(tree):
    r = []
    for e in tree: 
        if e.filemode == pygit2.GIT_FILEMODE_TREE:
            r.extend([(os.path.join(e.name, i[0]), i[1]) for i in path_blob_pairs_in_tree(e)])
        elif not e.filemode == pygit2.GIT_FILEMODE_COMMIT:
            r.append((e.name, e))
    return r

def path_blob_pairs_in_commit(commit):
    return path_blob_pairs_in_tree(commit.tree)


__all__ = ['git_repo', 
           'test', 
           ]
