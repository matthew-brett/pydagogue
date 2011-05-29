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
    sudo apt-get install ruby ruby-dev # for command-t
    make command-t
    make links

**********************
Setting up virtualenvs
**********************

* Install virtualenv_, and virtualenvwrapper_.  I did this with::

    sudo apt-get install python-setuptools
    sudo easy_install virtualenvwrapper

  I did this because there is was an incompatibility with Maverick Python 2.7
  and Maverick virtualenv_ - see `this bug report
  <https://bitbucket.org/ianb/virtualenv/issue/63/now-python27-requires-_weakrefset>`_.
  For Natty (next after Maverick), you can probably use::

    sudo apt-get install virtualenvwrapper

  instead.

* If you are using my config (above), you probably want my default environment
  cleanup for virtualenvs::

    cd myconfig
    make virtualenvs

* Make some good virtualenvs, with commands like::

    mkvirtualenv python25 --python=python2.5

  If you have to do something really bare, consider the ``no-site-packages``
  flag to the ``mkvirtualenv`` command.

  You'll probably want other versions of python for your virtualenvs.  This::

    sudo apt-get install python2.7 python2.7-dev

  works on Ubuntu Maverick (10.10). You might want to use the `old and new
  python versions`_ repository to get e.g python 2.5 on new Ubuntus::

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python2.5 python2.5-dev

  You may have to compile numpy and scipy from source for your non-system python
  versions::

    sudo apt-get build-dep python-numpy
    mkdir code
    cd code
    git clone git://github.com/numpy/numpy.git
    cd numpy
    git co v1.5.1 # a tag
    sudo python2.5 setup.py install
    sudo rm -rf build
    sudo python2.7 setup.py install
    cd ..
    # This will soon become a real git repo rather than an svn mirror
    git clone --origin svn git://github.com/scipy/scipy-svn.git scipy
    cd scipy
    git co svn/tags/v0.9.0rc4 # a tag
    sudo python2.5 setup.py install
    sudo rm -rf build
    sudo python2.7 setup.py install

  For the remaining packages, we can use setuptools.  As per the instructions on
  `old and new python versions`_ ::

    sudo apt-get install python-setuptools-deadsnakes

  then (e.g.)::

    sudo easy_install-2.5 nose


.. include:: links_names.inc
