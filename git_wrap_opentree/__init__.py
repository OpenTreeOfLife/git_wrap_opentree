#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple utility functions used by Open Tree python code.

These function are used by packages that descend from peyotl, but
do not depend on any part of peyotl.
"""
from __future__ import absolute_import, print_function, division

__version__ = '0.0.1a0'  # sync with setup.py

import pygit2
import os

from .git_repo import ConstGitRepo


__all__ = ['git_repo', 
           'test', 
           ]
