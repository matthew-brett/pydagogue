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
the `OSX wine builder`_ scripts. I've followed the instructions om the `Wine HQ
OSX building`_ page for a minimal up to date build. After cloning the wine git
repository as per the `Wine HQ OSX building`_ page::

    cd wine-git
    ./configure

I was compiling the code as of SHA1 hash
``9e6de30f8feb8eb0a5fbbfd88f34c7358f7d6e6b``.

Then the normal::

    make
    sudo make install

``make`` took over an hour on my Macbook Air.

Thence, download the python windows binary ``msi`` installers and::

    msiexec /i ~/Downloads/python-2.7.1.msi

For each version of python.  Similarly numpy and scipy::

    wine ~/Downloads/numpy-1.5.1-win32-superpack-python2.7.exe

I put python 2.6 (my current favorite) on the path by::

    wine regedit

then adding string values for ``PATH`` in ``HKEY_CURRENT_USER/Environment`` - as
suggested in the `numpy release howto`_.

Building python installers then can be::

    wine cmd
    cd package_dir
    python setup.py bdist_egg

or similar.

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
