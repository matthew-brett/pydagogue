#######################################
Python installations on Debian / Ubuntu
#######################################

In the old days, installation of Python packages was badly messed up.

One of the big problems was the `easy_install`_ program, that installed
packages in a way that could make them particularly difficult to uninstall (see :ref:`un-easy-install`).

Things started to improve as pip_ took over from ``easy_install`` as the standard Python package installer.

They got better still when ``pip`` got a binary installer format |--| wheels_.

The combination of virtualenv_, ``pip`` and wheels makes it much easier to maintain a set of Python environments to develop and test code.

This page is a recipe for setting up these virtualenvs on your Debian or Ubuntu machine.

************************
Debian and Ubuntu Python
************************

Debian and Ubuntu have some special rules for where Python packages go.  See : https://wiki.debian.org/Python

The main point of interest to us, is that Python packages that you install for
the Debian / Ubuntu packaged Python using ``apt`` or ``pip`` or ``python
setup.py install`` go into a folder ``/usr/local/lib/pythonX.Y/dist-packages``
where X.Y is your Python version (such as ``2.7``).  This is different from
Python as compiled from the raw Python source code, which expects by default
to install to a folder ``/usr/local/lib/pythonX.Y/site-packages``.

.. _un-easy-install:

***********************************
Clean out old easy_install installs
***********************************

I highly recommend you nuke any old easy_install installations.  If you have
never used easy_install on this system, you don't need to read this section.

First you need to find the easy_install installs.  To do this, display the file ``/usr/local/lib/pythonX.Y/dist-packages/easy-install.pth`` (where ``X.Y`` is the relevant Python version, such as ``2.7``).  If this file doesn't exist, lucky you, skip this section.

If the file does exist, look for the packages listed in the file.  The file will look something like::

    import sys; sys.__plen = len(sys.path)
    ./requests-0.12.1-py2.7.egg
    ./oauthlib-0.1.3-py2.7.egg
    ./certifi-0.0.8-py2.7.egg
    ./rsa-3.0.1-py2.7.egg
    ./pyasn1-0.1.3-py2.7.egg
    import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)

Delete each directory listed, e.g.::

    rm -rf /usr/local/lib/python2.7/dist-packages/requests-0.12.1-py2.7.egg
    rm -rf /usr/local/lib/python2.7/dist-packages/oauthlib-0.1.3-py2.7.egg

etc.  When you have finished deleting these directories, delete the ``easy-install.pth`` file.  Phew, all done.

*************************
Install virtualenvwrapper
*************************

``virtualenvwrapper`` is a very useful |--| er |--| wrapper around ``virtualenv``, that makes it easier and neater to have a library of virtual Python environments::

    sudo pip install virtualenvwrapper

To insert various useful aliases into your shell environment, this one time you should do::

    source ~/.bashrc

****************
Install Python 3
****************

If you want to make virtualenvs using Python 3, you will need to install Python 3 from the Debian / Ubuntu repositories.

::

    sudo apt-get install python3 python3-pip

******************************
Prepare a wheelhouse directory
******************************

In this step you build wheels that you can install in virtualenvs.

First install build dependencies for common libraries::

    sudo apt-get build-dep python-numpy python-scipy matplotlib h5py

This will take about 20 minutes (at least, it did on my virtualbox / Vagrant
Debian instance).

Next make a directory to contain the wheels::

    mkdir ~/wheelhouse

Tell pip that it can install wheels from this directory, by creating a file ``~/.pip/pip.conf`` something like this::

    [global]
    find-links = /home/<your-user-name>/wheelhouse
    use-wheel = True

Obviously you need to replace ``<your-user-name>`` with your user name.

************
Build wheels
************

Start up a new virtualenv for Python 2::

    mkvirtualev python2

Make sure the ``wheel`` utility is installed::

    pip install wheel

Build and install wheels for numpy and cython::

    pip wheel -w ~/wheelhouse numpy cython
    pip install numpy cython

Now build any other wheels you are likely to use, e.g.::

    pip wheel -w ~/wheelhouse scipy matplotlib h5py

Finish up by deactivating the virtualenv::

    deactivate

You might want to do the same with Python 3::

    mkvirtualenv --python=/usr/bin/python3 python3
    pip install wheel
    pip wheel -w ~/wheelhouse numpy cython
    pip install numpy cython
    pip wheel -w ~/wheelhouse scipy matplotlib h5py
    deactivate

*********************************
Now you are in virtualenv nirvana
*********************************

You can now make virtualenvs for your testing development quickly, even when
you are offline.  Say you want to test something out for Python 3::

    # Make clean virtual environment
    mkvirtualenv --python=/usr/bin/python3 testing-something
    pip install numpy scipy matplotlib h5py
    # install anything else you want
    # run your tests
    deactivate

Nice.

*****************
Adding new wheels
*****************

Adding new wheels is usually as simple as::

    # Switch to relevant virtualenv
    workon python2
    pip wheel -w ~/wheelhouse my-package

Sometimes the Python package you are installing has nasty binary dependencies.  In this case, usually your easiest path is to install the build dependencies for the corresponding Debian / Ubuntu package, and then continue as before::

    sudo apt-get build-dep pillow
    workon python2
    pip wheel -w ~/wheelhouse pillow

*********************************
Sometimes, it's a package too far
*********************************

There are some Python packages that have heavy binary dependencies, or use
complicated build systems, so that it is not practical to build a wheel with
pip.  Examples I know of are vtk and itk.  For those cases, your best option
is to install the Python package using ``apt-get``, and then make your
virtualenv with the ``--system-site-packages`` flag, so that it will pick up
the installed packages::

    sudo apt-get install python-vtk
    mkvirtualenv --system-site-packages with-vtk

*********************
Another good approach
*********************

Another good approach that can get you the at-or-near-latest packages quickly,
is to install packages from NeuroDebian_.  Here, you rely on the NeuroDebian
packages, which install, like other Debian packages, into
``/usr/local/lib/pythonX.Y/site-packages``.  You can either use Python or Python3 without a virtualenv, or do::

    mkvirtualenv --system-site-packages my-venv

to pick up all the packages installed in
``/usr/local/lib/pythonX.Y/site-packages``.

*********************************************
Doesn't work for you?  Help improve this page
*********************************************

If you try the instructions here, and you can't get a particular package or set-up to work, then why not make an `issue <pydagogue issues>`_ for the repository hosting these pages, and I'll see if I can work the fix into this page somewhere.

.. include:: links_names.inc
