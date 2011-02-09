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

* Make some good virtualenvs, with commands like::

    mkvirtualenv --distribute --python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python python26

  If you have to do something really bare, consider the ``no-site-packages``
  flag to the ``mkvirtualenv`` command.


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
