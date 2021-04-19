# peyutil
[![Build Status](https://secure.travis-ci.org/OpenTreeOfLife/git_wrap_opentree.png)](http://travis-ci.org/OpenTreeOfLife/git_wrap_opentree)

git_wrap_opentree
=================


<code>git_wrap_opentree</code> is a package of basic utility functions
for interacting with git used by the [Open Tree of Life][1] project.
It is one of the packages that used to make up a part of
[peyotl](https://github.com/OpenTreeOfLife/peyotl).
This package probably not of great use to external developers by itself, it
is a prerequisite for the Open Tree of Life softward. 

Instructions
------------

::

    python3 -mvenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop
    python setup.py test

performs the basic installation and test.

Thanks
------

Thanks to [NSF][3] and [HITS][4] for funding support.

git_wrap_opentree is primarily written by Mark Holder, and Emily Jane McTavish
but see the [CONTRIBUTORS][2] file for a more complete list
of people who have contributed code. 




****************

[1]: https://opentreeoflife.github.io/
[2]: https://raw.githubusercontent.com/OpenTreeOfLife/peyutil/master/CONTRIBUTORS.txt
[3]: https://www.nsf.gov
[4]: https://www.h-its.org/institute/
