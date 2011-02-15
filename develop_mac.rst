#################
Developing on mac
#################

Sketch of the steps to get up and running on a mac to make binary releases for
python packages.  This is my personal setup.

**********
My systems
**********

* Macbook air first generation running Snow Leopard. ``uname -a`` gives ``Darwin
  Kernel Version 10.6.0``.

***********
Basic setup
***********

* Xcode_, obviously
* git_ - see the `github osx installation`_
* editor.  I like vim_ - via macvim_
* For every python version you want to support, download the "Mac installer disk
  image" ``dmg`` file via the links from the `Python.org releases`_.  Run the
  installation.
* Check in your ``~/.bash_profile`` to see what version of python will reach
  your path first.  Adapt to taste.  Python.org installs go in directories like
  ``/Library/Frameworks/Python.framework/Versions/2.6``. You need this directory
  with ``/bin`` appended on your path.
* For each version of python you want to support:

    * install distribute_
    * install numpy_
    * install scipy_

* Install personal setup::

    git clone git@github.com:matthew-brett/myconfig.git
    cd myconfig
    make dotfiles
    cd ..

  Then edit ``~/.bash_profile`` to add the commented lines at the top of your new
  ``~/.bash_personal`` file.  Then set up vim::

    git clone git@github.com:matthew-brett/myvim.git
    cd myvim
    make command-t
    make links

* For your favorite python version, install virtualenv_, and virtualenvwrapper_
* If you are using my config (above), you probably want my default environment
  cleanup for virtualenvs::

    cd myconfig
    make virtualenvs

* For packaging, download and unpack the source distribution for bdist_mpkg_. I
  unpacked it into ``~/stable_trees/bdist_mpkg-0.4.4``.

* Make some good virtualenvs, with commands like::

    mkvirtualenv --python=/Library/Frameworks/Python.framework/Versions/2.5/bin/python python25
    mkvirtualenv --python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python python26
    mkvirtualenv --python=/Library/Frameworks/Python.framework/Versions/2.7/bin/python python27

  If you have to do something really bare, consider the ``no-site-packages``
  flag to the ``mkvirtualenv`` command.

* For each virtualenv you're going to use (to taste)::

    workon python25
    easy_install ipython
    cd ~/stable_trees/bdist_mpkg-0.4.4
    python setup.py install

  Maybe also (this is for dipy installs)::

    easy_install nibabel
    easy_install cython

****************************************
Building windows release files with wine
****************************************

This trick comes to you courtesy of the numpy release managers - see the `numpy
release howto`_.  The suggestion in that howto, as of February 2010 - was to use
the `OSX wine builder`_ scripts. I'm using revision 107 of this script.
Eventually I used this incantation::

    ./osxwinebuild.sh --devel

for something that more or less worked - as below.  With this option we get wine
1.3.13.  Without the ``--devel`` option, we get wine 1.2.2 - this crashed for me
when trying to build some extension modules.  I also tried following the
instructions on the `Wine HQ OSX building`_ page for a minimal up to date build
using git SHA1 commit hash ``9e6de30f8feb8eb0a5fbbfd88f34c7358f7d6e6b``.  This
worked OK but I went back to the full ``osxwinebuild.sh --devel`` version
because it was annoying to have bad fonts and font warnings from the bare build.

After installing with ``osxwinebuild.sh``, source the suggested environment
variables, and then maybe you'll have a working system ahead of you - as below.

Thence, download the python windows binary ``msi`` installers and::

    msiexec /i python-2.7.1.msi
    msiexec /i python-2.6.6.msi
    msiexec /i python-2.5.4.msi

I then installed setuptools for each python::

    wine setuptools-0.6c11.win32-py2.7.exe
    wine setuptools-0.6c11.win32-py2.6.exe
    wine setuptools-0.6c11.win32-py2.5.exe

Then the mingw_ tools::

    wine mingw-get-inst-20110211.exe

I selected to install the mingw_ development tools - these include the Msys_
minimal development system.

Similarly numpy and scipy for each version of python::

    wine numpy-1.5.1-win32-superpack-python2.7.exe
    wine numpy-1.5.1-win32-superpack-python2.6.exe
    wine numpy-1.5.1-win32-superpack-python2.5.exe
    wine scipy-0.9.0rc2-win32-superpack-python2.7.exe
    wine scipy-0.8.0-win32-superpack-python2.6.exe
    wine scipy-0.8.0-win32-superpack-python2.5.exe

I used scipy 0.9.0rc2 because it was the closest to a released version that
worked with python 2.7 at the time (Feb 2011).

I put python 2.6 (my current favorite) on the path by::

    wine regedit

then adding string values for ``PATH`` in ``HKEY_CURRENT_USER/Environment`` - as
suggested in the `numpy release howto`_.  Actually, I also added the mingw tools
to the path, so my ``HKEY_CURRENT_USER/Enviromnment/PATH`` string value is::

    c:\Python26;C:\Python26\Scripts;C:\mingw\bin;C:\mingw\msys\1.0\bin

I also set ``HKEY_CURRENT_USER/Enviromnment/HOME`` to ``C:\users\mb312`` (where
``mb312`` is my username).

Now, you may be as lucky as me, and this::

    wineconsole bash

gives you a perfectly reasonable bash shell operating in a windows-like
environment.  It's a little bit flaky, but for example, I can build python
installers with ``wineconsole bash`` followed by::

    cd package_dir
    python setup.py bdist_egg

or similar.  You will probably also need to tell distutils to use the
instructions at :ref:`win-compile-tools`.

I was also using virtualenvs.  In wineconsole bash::

    cd /c/
    mkdir virtualenvs
    cd virtualenvs
    easy_install virtualenvs
    virtualenv python27 --python=C:\\Python27\\python.exe

and so on.

.. _git: http://git-scm.com
.. _github osx installation: http://help.github.com/mac-git-installation
.. _xcode: http://developer.apple.com/TOOLS/xcode
.. _vim: http://www.vim.org
.. _macvim: https://github.com/b4winckler/macvim
.. _python.org releases: http://www.python.org/download/releases
.. _distribute: http://pypi.python.org/pypi/distribute
.. _numpy: http://sourceforge.net/projects/numpy/files
.. _scipy: http://sourceforge.net/projects/scipy/files
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper
.. _bdist_mpkg: http://pypi.python.org/pypi/bdist_mpkg
.. _numpy release howto: https://github.com/numpy/numpy/blob/master/doc/HOWTO_RELEASE.rst.txt
.. _osx wine builder: http://code.google.com/p/osxwinebuilder/
.. _wine hq osx building: http://wiki.winehq.org/MacOSX/Building
.. _freetype: http://www.freetype.org
.. _macports: http://www.macports.org
.. _mingw: http://www.mingw.org
.. _msys: http://www.mingw.org/wiki/MSYS
