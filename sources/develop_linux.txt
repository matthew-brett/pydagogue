###################
Developing on linux
###################

Sketch of the steps to get up and running on linux to make binary releases for
python packages.  This is my personal setup.

**********
My systems
**********

* Many. Currently I'm working on an Ubuntu Lucid 64 bit system::

    $ uname -a
    Linux angela 2.6.32-28-generic #55-Ubuntu SMP Mon Jan 10 23:42:43 UTC 2011 x86_64 GNU/Linux

***********
Basic setup
***********

::

    sudo apt-get install git-core
    sudo apt-get install python-dev python-numpy python-scipy

* Install personal setup::

    git clone git@github.com:matthew-brett/myconfig.git
    cd myconfig
    make dotfiles
    cd ..

  Then edit ``~/.bashrc`` to add the commented lines at the top of your new
  ``~/.bash_personal`` file.  Then set up vim::

    git clone git@github.com:matthew-brett/myvim.git
    cd myvim
    make command-t
    make links

* Install virtualenv_, and virtualenvwrapper_::

    sudo apt-get install python-virtualenv

  Then download virtualenvwrapper_ and install thus (in the system, not to $HOME
  somewhere)::

    cd virtualenvwrapper
    sudo python setup.py install

  The obvious reason being that if you want to run virtualenvwrapper scripts,
  and you're unsetting pointers to your local setup, then we'll lose
  virtualenvwrapper and get errors.

* If you are using my config (above), you probably want my default environment
  cleanup for virtualenvs::

    cd myconfig
    make virtualenvs

* Make some good virtualenvs, with commands like::

    mkvirtualenv --distribute --python=/Library/Frameworks/Python.framework/Versions/2.6/bin/python python26

  If you have to do something really bare, consider the ``no-site-packages``
  flag to the ``mkvirtualenv`` command.


.. _git: http://git-scm.com
.. _vim: http://www.vim.org
.. _python.org releases: http://www.python.org/download/releases
.. _distribute: http://pypi.python.org/pypi/distribute
.. _numpy: http://sourceforge.net/projects/numpy/files
.. _scipy: http://sourceforge.net/projects/scipy/files
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper
