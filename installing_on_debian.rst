#######################################
Python installations on Debian / Ubuntu
#######################################

In the old days, installation of Python packages was badly messed up.

One of the big problems was the `easy_install`_ program, that installed
packages in a way that could make them particularly difficult to uninstall (see
:ref:`un-easy-install`).

Things started to improve as pip_ took over from ``easy_install`` as the
standard Python package installer.

They got better still when ``pip`` got a binary installer format |--| wheels_.

The combination of virtualenv_, ``pip`` and wheels makes it much easier to
maintain a set of Python environments to develop and test code.

This page is a recipe for setting up these virtualenvs on your Debian or
Ubuntu machine.

The recipe I propose is this:

* if you have any `easy_install` installations, remove them;
* build Python wheels for all the packages you use, and install from those;
* have a very low threshold for using virtualenvs, via virtualenvwrapper_;
* Use ``pip install --user`` to install packages into your day to day default
  Python environment.

.. _un-easy-install:

***********************************
Clean out old easy_install installs
***********************************

If you are starting from scratch or you have never used `easy_install` on your system, you can ignore this section.

A note on Debian and Ubuntu Python
==================================

Debian and Ubuntu have some special rules for where Python packages go.  See
: https://wiki.debian.org/Python

The main point of interest to us, is that Python packages that you install for
the Debian / Ubuntu packaged Python go into different directories that would
be the case for a non-Debian Python installation.

A non-Debian Python installation, such as Python compiled from source, will
install Python packages into ``/usr/local/lib/pythonX.Y/site-packages`` by
default, where X.Y is your Python version (such as ``2.7``).

For Debian Python, package files go into different directories depending on
whether you installed the package from standard Debian packages, or using
Python's own packaging mechanisms, such as ``pip``, ``easy_install`` or
``python setup.py install``.

Debian Python packages installed via ``apt`` or ``dpkg`` go into
a folder ``/usr/lib/pythonX.Y/dist-packages`` [#apt-installs]_

``pip``, ``easy_install`` or ``python setup.py install`` installs go into a
folder ``/usr/local/lib/pythonX.Y/dist-packages``.

Removing easy-install installs
==============================

First you need to find the easy_install installs.  To do this, display the
file ``/usr/local/lib/pythonX.Y/dist-packages/easy-install.pth`` (where
``X.Y`` is the relevant Python version, such as ``2.7``).  If this file
doesn't exist, lucky you, skip this section.

If the file does exist, look for the packages listed in the file.  The file
will look something like::

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

etc.  When you have finished deleting these directories, delete the
``easy-install.pth`` file.  Phew, all done.

*******************
Install, update pip
*******************

You will need pip version >= 6.0 in order to get `pip wheel caching
<https://pip.pypa.io/en/latest/reference/pip_install/#caching>`_. This is a
killer pip feature, that means that you only build wheels from source once,
the first time you install a package.  Pip then caches the wheel so you use
the cached version next time you do an install.

We recommend you uninstall any Debian versions of pip, if you have them::

    sudo apt-get remove python-pip python3-pip

Then install pip using the `standard instructions
<https://pip.pypa.io/en/latest/installing/#install-pip>`_::

    wget https://bootstrap.pypa.io/get-pip.py
    sudo python get-pip.py

Now check the pip version is >= 6.0::

    pip --version

You can do the same for Python3::

    sudo python3 get-pip.py

This will make ``pip``, by default, install into Python 3.  If you prefer the
``pip`` command to install into Python 2 by default, you could run ``python
get-pip.py --ignore-installed`` again to make ``pip`` be the Python 2 pip
by default.  You can always run ``pip2`` and ``pip3`` explicitly if you need
the Python 2 or Python 3 versions.

*********************************
Install, update virtualenvwrapper
*********************************

``virtualenvwrapper`` is a very useful |--| er |--| wrapper around |--| er
|--| ``virtualenv``, that makes it easier and neater to have a library of
virtual Python environments::

    sudo pip install --upgrade virtualenvwrapper

The ``--upgrade`` is important because virtualenv (installed by
virtualenvwrapper) contains its own copy of pip.  We need the latest version
of virtualenv to make sure we will get a recent version of pip in our
virtualenvs.

To insert various useful aliases into your shell environment, this one time
you should do::

    source ~/.bashrc

****************
Install Python 3
****************

If you want to make virtualenvs using Python 3, you will need to install
Python 3 from the Debian / Ubuntu repositories.

::

    sudo apt-get install python3

*********************************
Set up the system to build wheels
*********************************

Install standard build dependencies for common libraries::

    sudo apt-get build-dep python-numpy python-scipy matplotlib h5py

This will take about 20 minutes (at least, it did on my virtualbox / Vagrant
Debian instance).

***********************************
Build wheels by installing with pip
***********************************

Now you have pip > 6.0, building wheels is just a matter of installing the
package for the first time.

Start up a new virtualenv for Python 2::

    mkvirtualev python2

Install numpy and cython.  This will build and cache wheels for the latest
numpy and cython::

    pip install numpy cython

Now you can install (therefore, build and cache) other wheels you might need::

    pip install scipy matplotlib h5py

Finish up by deactivating the virtualenv::

    deactivate

You might want to do the same with Python 3::

    mkvirtualenv --python=/usr/bin/python3 python3
    pip install numpy cython
    pip install scipy matplotlib h5py
    deactivate

*********************************
Now you are in virtualenv nirvana
*********************************

It's often good to use virtualenvs to start a development session.  Doing so
means that you can install exactly the requirements that you need, without
causing changes to your other virtualenvs.

You can now make virtualenvs for your testing development quickly.  Say you
want to test something out for Python 3::

    # Make clean virtual environment
    mkvirtualenv --python=/usr/bin/python3 testing-something
    pip install numpy scipy matplotlib h5py
    # install anything else you want
    # run your tests
    deactivate

Nice.

Even if you are offline, you can always install things you have already built
and cached, by adding the ``--no-index`` flag to pip::

    # Make another clean virtual environment
    mkvirtualenv --python=/usr/bin/python3 testing-offline
    pip install numpy scipy matplotlib h5py --no-index
    # install anything else you want
    # run your tests
    deactivate

****************************************************
Use ``--user`` installs for your default environment
****************************************************

Sometimes you may want a default environment, that has a set of packages that
you commonly use.

This is a good role for pip ``--user`` installs.  If you install a package
like this::

    pip install --user mypackage

then ``mypackage`` will be installed into a special user-specific directory,
that, by default, is on your Python module search path.  For example, outside
any virtualenv, here is what I get for the Python module search path
(``sys.path``) (after I have done a ``--user`` install as above)::

    \$ python
    Python 2.7.9 (default, Mar  1 2015, 12:57:24)
    [GCC 4.9.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sys
    >>> print('\n'.join(sys.path))

    /usr/lib/python2.7
    /usr/lib/python2.7/plat-x86_64-linux-gnu
    /usr/lib/python2.7/lib-tk
    /usr/lib/python2.7/lib-old
    /usr/lib/python2.7/lib-dynload
    /home/vagrant/.local/lib/python2.7/site-packages
    /usr/local/lib/python2.7/dist-packages
    /usr/lib/python2.7/dist-packages
    /usr/lib/python2.7/dist-packages/PILcompat
    /usr/lib/python2.7/dist-packages/gtk-2.0
    /usr/lib/pymodules/python2.7
    /usr/lib/python2.7/dist-packages/wx-3.0-gtk2

Notice the line ``/home/vagrant/.local/lib/python2.7/site-packages``. This is
the path containing packages that have been installed with the pip ``--user``
option.

Python packages often install scripts (executables) as well as Python modules.
To get full use of ``--user`` installed packages, you may also want to put the
matching executable path onto your system.  I do this with the following lines
in my ``~/.bashrc`` file::

    export PY_USER_BIN=\$(python -c 'import site; print(site.USER_BASE + "/bin")')
    export PATH=\$PY_USER_BIN:\$PATH

These lines work on Linux or OSX.

If you do this, then you can use the command line scripts installed by
packages like `ipython`_.  When using virtualenvs, you may want to make sure
you aren't getting the ``--user`` installed scripts, by taking this directory
off the path.  To do this, I have the following in my
``~/.virtualenvs/postactivate`` file::

    # Clear user Python binary path when using virtualenvs
    export PATH=\$(echo $PATH | sed "s|\${PY_USER_BIN}:\{0,1\}||")

******************************
Adding new packages and wheels
******************************

Adding new wheels is usually as simple as::

    # Switch to relevant virtualenv to build, cache, install wheel
    workon python2
    pip install my-package

Sometimes the Python package you are installing has nasty binary dependencies.
In this case, usually your easiest path is to install the build dependencies
for the corresponding Debian / Ubuntu package, and then continue as before::

    sudo apt-get build-dep pillow
    workon python2
    pip install pillow

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
    mkvirtualenv --system-site-packages an-env-including-vtk

*********************
Another good approach
*********************

Another good approach that can get you the at-or-near-latest packages quickly,
is to install packages from NeuroDebian_.  Here, you rely on the NeuroDebian
packages, which install, like other Debian packages, into
``/usr/lib/pythonX.Y/dist-packages``.  You can either use Python or
Python3 without a virtualenv, or do::

    mkvirtualenv --system-site-packages my-venv

to pick up all the packages installed in
``/usr/lib/pythonX.Y/dist-packages``.

*********************************************
Doesn't work for you?  Help improve this page
*********************************************

If you try the instructions here, and you can't get a particular package or
set-up to work, then why not make an `issue <pydagogue issues>`_ for the
repository hosting these pages, and I'll see if I can work the fix into this
page somewhere.

.. rubric:: Footnotes

.. [#apt-installs] You can see where files would go for any Debian / Ubuntu
   package with ``apt-file list <package-name>``

.. include:: links_names.inc
