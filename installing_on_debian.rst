############################
Using Pip on Debian / Ubuntu
############################

In the old days, it was hard and error-prone to use Python tools rather than
your Debian / Ubuntu package manager to install Python packages.

One of the big problems was the `easy_install`_ program, that installed
packages in a way that could make them particularly difficult to uninstall
(see :ref:`un-easy-install`).

Things started to improve as Pip_ took over from ``easy_install`` as the
standard Python package installer.

They got better still when Pip got a binary installer format |--| wheels_.

The combination of virtualenv_, Pip and wheels makes it much easier to
maintain a set of Python environments to develop and test code.

This page is a recipe for setting up these environments on your Debian or
Ubuntu machine.

******************************
Do you really want to do this?
******************************

Debian and Ubuntu package maintainers put a lot of effort into maintaining
binary ``.deb`` installers for common Python packages like numpy_, scipy_ and
matplotlib_.  For example, to get the standard versions of these for your
Debian / Ubuntu distribution, you can do this::

    sudo apt-get install python-numpy python-scipy python-matplotlib

Standard ``apt-get`` installation may well be all you need.  The versions of
numpy, scipy, matplotlib for your distribution can be a little behind the
latest version available from pypi_ (the Python package index).  If you want a
more recent version of common Python packages, you might also consider
installing Debian / Ubuntu packages from NeuroDebian_.  Again, you can use the
standard Debian tools like ``apt-get`` to do your installs.

The advantage of always using standard Debian / NeuroDebian packages, is that
the packages are carefully tested to be compatible with each other.
The Debian packages record dependencies with other libraries so you will
always get the libraries you need as part of the install.

If you use Pip to install packages, then you don't get these guarantees.  If
you use Pip and run into problems with your Python installation, it will be
harder for you to get support from the Debian / Ubuntu community, because you
are using an installation method that they do not support, and that is more
fragile.

So, consider whether you can get away with the package versions in your
distribution, maybe by using the most recent packages from NeuroDebian. If
you can use these, then you probably should not use the Pip installs I'm
describing below.

*****************************
Why you might want to use Pip
*****************************

Although Pip installs are more fragile than Debian / Ubuntu package installs,
they do have several advantages.  With Pip you can:

* get the latest version of the package;
* install specific packages into virtualenvs;
* install packages that have not yet been built for your distribution.

**********************************************************
If you do want Pip installs on your Debian / Ubuntu system
**********************************************************

The recipe I propose is this:

* if you have any `easy_install` installations, :doc:`remove them
  <un_easy_install>`;
* install Pip and virtualenvwrapper_ into your user directories (rather than
  the system directories);
* use ``pip install --user`` to install packages into your day-to-day default
  Python environment;
* install Python packages via Pip, and let Pip wheel caching take care of
  keeping a binary wheel ready for the next time you install this package;
* have a very low threshold for using virtualenvs, via virtualenvwrapper.

I suggest you never use Pip to change your system-wide packages |--| so you
never use Pip with ``sudo``.  This makes sure your Pip-installed packages do
not break your system.  To avoid ``sudo`` you should always install into your
user directories (via ``pip install --user``) or within virtualenvs (see
below).

********************************************************
Use Pip ``--user`` installs for your default environment
********************************************************

The ``--user`` flag to ``pip install`` tells Pip to install packages in some
specific directories within your home directory.  This is a good way to have
your own default Python environment that adds to the packages within your
system directories, and therefore, does not affect the system Python
installation.

So, if you install a package like this::

    pip install --user mypackage

then ``mypackage`` will be installed into a special user-specific directory,
that, by default, is on your Python module search path.  For example, outside
any virtualenv, here is what I get for the Python module search path
(``sys.path``) (after I have done a ``--user`` install as above)::

    $ python
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

(For an explanation of the ``dist-packages`` entries, see
:doc:`debian_python_paths`).

Notice the line ``/home/vagrant/.local/lib/python2.7/site-packages``. This is
the path containing packages that have been installed with the Pip ``--user``
option.

Python packages often install scripts (executables) as well as Python modules.
To get full use of ``--user`` installed packages, you may also want to put the
matching executable path onto your system.  I do this with the following lines
in my ``~/.bashrc`` file::

    export PY_USER_BIN=$(python -c 'import site; print(site.USER_BASE + "/bin")')
    export PATH=$PY_USER_BIN:$PATH

These lines work on Linux or OSX.

If you do this, then you can use the command line scripts installed by
packages like `ipython`_.  When using virtualenvs, you may want to make sure
you aren't getting the ``--user`` installed scripts, by taking this directory
off the path.  If you are using :ref:`virtualenvwrapper
<install-virtualenvwrapper>` (see below) you can do this automatically, with
something like this in a ``~/.virtualenvs/postactivate`` file::

    # Clear user Python binary path when using virtualenvs
    export PATH=$(echo $PATH | sed "s|${PY_USER_BIN}:\{0,1\}||")

************************************************
Install, update Pip using ``pip install --user``
************************************************

For these steps to work, you will need the Pip ``--user`` install binary
directory on your path.  See above for how to do this. Check that your
``--user`` binary directory is on the path with::

    echo $PATH

The output should contain something like ``/home/your-user/.local/bin``.

You will need Pip version >= 6.0 in order to get `Pip wheel caching
<https://pip.pypa.io/en/latest/reference/pip_install/#caching>`_. This is a
killer Pip feature, that means that you only build wheels from source once,
the first time you install a package.  Pip then caches the wheel so you use
the cached version next time you do an install.

First install the latest version of Pip into your user account by following
the instructions at `install Pip with get-pip.py`_::

    curl -LO https://bootstrap.pypa.io/get-pip.py
    python get-pip.py --user

If you are using both python 2 and python 3 versions, do the installation for
both versions, installing last for the Python version that you want to own the
``Pip`` command, e.g::

    # Intall pip for Python 2 installs
    python get-pip.py --user
    # Upgrade Pip for Python 3 installs (this one owns "pip" now)
    python3 get-pip.py --user

Now check the Pip version is >= 6.0::

    pip --version

If you installed for both Python 2 and Python 3::

    pip2 --version
    pip3 --version

Check you are picking up the ``--user`` Pip by looking at the output of::

    which pip
    which pip2
    which pip3

This should give you outputs like ``/home/your-user/.local/bin/pip``.

.. _install-virtualenvwrapper:

*********************************
Install, update virtualenvwrapper
*********************************

virtualenvwrapper_ is a very useful |--| er |--| wrapper around |--| er |--|
``virtualenv``, that makes it easier and neater to have a library of virtual
Python environments.  First install the Debian packaged version to your system
directories.  This sets up bash shell integration::

    sudo apt-get install virtualenvwrapper

Now upgrade your user installation to the latest virtualenvwrapper::

    pip install --user --upgrade virtualenvwrapper

The ``--upgrade`` in the installation is important because virtualenv
(installed by virtualenvwrapper) contains its own copy of Pip.  We need the
latest version of virtualenv to make sure we will get a recent version of Pip
in our virtualenvs.

Check you are getting your new ``--user`` installed version, with::

    which virtualenv

This should you something like ``/home/your-user/.local/bin/virtualenv``.

The ``virtualenvwrapper`` apt package puts useful aliases into the default
bash shell environment.  To get these aliases loaded up in your current shell,
this one time you should do::

    source ~/.bashrc

Check you have the virtualenvwrapper aliases loaded with::

    mkvirtualenv

This should give you the help for the ``mkvirtualenv`` virtualenvwrapper
command.

**************************************************
Set up your system to build binary Python packages
**************************************************

This will install the tools that Python needs to build any binary package::

    # For Python 2
    sudo apt-get install -y python-dev

    # For Python 3
    sudo apt-get install -y python3-dev

Pip will need these tools when installing Python packages that do not already
have binary packages for your platform (see below).

**********************************************
Build or install wheels by installing with Pip
**********************************************

Many standard Python packages have binary `manylinux`_ `wheels`_. These binary
installers will work for almost any Intel-based Linux, including Debian /
Ubuntu.  If your platform is compatible, Pip will download and install the
binary package when you do a simple::

    pip install --user numpy

where `numpy` is the package to install.

Start up a new virtualenv for Python::

    mkvirtualenv venv

Install numpy and cython.  If you are on an Intel platform, this will download
binary wheels for the latest numpy and cython.  If you are not on Intel, Pip
will download the source packages, then build and cache the wheels
[#building-wheels]_::

    pip install numpy cython

Now you can install (and, if not on Intel, build and cache) other wheels you
might need::

    pip install scipy matplotlib h5py

Finish up by deactivating the virtualenv::

    deactivate

This is the same sequence using Python 3::

    mkvirtualenv --python=/usr/bin/python3 venv-py3
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
and cached, by adding the ``--no-index`` flag to Pip::

    # Make another clean virtual environment
    mkvirtualenv --python=/usr/bin/python3 testing-offline
    pip install numpy scipy matplotlib h5py --no-index
    # install anything else you want
    # run your tests
    deactivate

.. _new-wheels:

******************************
Adding new packages and wheels
******************************

Adding new wheels is usually as simple as::

    # Switch to relevant virtualenv to build, cache, install wheel
    workon venv
    pip install my-package

Sometimes the Python package you are installing has nasty binary dependencies.
In this case, usually your easiest path is to install the build dependencies
for the corresponding Debian / Ubuntu package, and then continue as before::

    sudo apt-get build-dep pillow
    workon venv
    pip install pillow

*********************************
Sometimes, it's a package too far
*********************************

There are some Python packages that have heavy binary dependencies, or use
complicated build systems, so that it is not practical to build a wheel with
Pip.  Examples I know of are VTK and ITK.  For those cases, your best option
is to install the Python package using ``apt-get``, and then make your
virtualenv with the ``--system-site-packages`` flag, so that it will pick up
the installed packages::

    sudo apt-get install python-vtk
    mkvirtualenv --system-site-packages an-env-including-vtk

*********************************************
Doesn't work for you?  Help improve this page
*********************************************

If you try the instructions here, and you can't get a particular package or
set-up to work, then why not make an `issue <pydagogue issues>`_ for the
repository hosting these pages, and I'll see if I can work the fix into this
page somewhere.

.. rubric:: Footnotes

.. [#building-wheels] If you need to build common packages such as Numpy (for
   example, on platforms like ARM), you should first install the Debian /
   Ubuntu packages with the build dependencies for these packages. For example
   you might want to run something like this::

     sudo apt-get build-dep python-numpy python-scipy matplotlib h5py

   This will take a fairly long time.  See :ref:`new-wheels`.

.. include:: links_names.inc
