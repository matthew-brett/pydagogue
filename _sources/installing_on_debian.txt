############################
Using pip on Debian / Ubuntu
############################

In the old days, it was hard and error-prone to use Python tools rather than
your Debian / Ubuntu package manager to install Python packages.

One of the big problems was the `easy_install`_ program, that installed
packages in a way that could make them particularly difficult to uninstall (see
:ref:`un-easy-install`).

Things started to improve as pip_ took over from ``easy_install`` as the
standard Python package installer.

They got better still when pip got a binary installer format |--| wheels_.

The combination of virtualenv_, pip and wheels makes it much easier to
maintain a set of Python environments to develop and test code.

This page is a recipe for setting up these virtualenvs on your Debian or
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

If you use pip to install packages, then you don't get these guarantees.
If you use pip and run into problems with your Python installation, it will be
harder for you to get support from the Debian / Ubuntu community, because you
are using an installation method that they do not support, and that is
considerably more fragile.

So, consider whether you can get away with the package versions in your
distribution, maybe by using the most recent packages from NeuroDebian. If
you can use these, then you probably should not use the pip installs I'm
describing below.

*****************************
Why you might want to use pip
*****************************

Although pip installs are a lot more fragile than Debian / Ubuntu pacakge
installs, they do have sevaral advantages.  With pip you can:

* get the latest version of the package;
* install specific packages into virtualenvs;
* install packages that have not yet been built for your distribution.

**********************************************************
If you do want pip installs on your Debian / Ubuntu system
**********************************************************

The recipe I propose is this:

* if you have any `easy_install` installations, :doc:`remove them
  <un_easy_install>`;
* install the various Debian / Ubuntu packages containing dependencies for
  common Python packages like numpy, scipy, matplotlib;
* make sure you have updated pip to a version that uses wheel caching;
* install Python packages via pip, and let wheel caching take care of keeping
  a binary wheel ready for the next time you install this package;
* have a very low threshold for using virtualenvs, via virtualenvwrapper_;
* Use ``pip install --user`` to install packages into your day to day default
  Python environment.

*******************
Install, update pip
*******************

You will need pip version >= 6.0 in order to get `pip wheel caching
<https://pip.pypa.io/en/latest/reference/pip_install/#caching>`_. This is a
killer pip feature, that means that you only build wheels from source once,
the first time you install a package.  Pip then caches the wheel so you use
the cached version next time you do an install.

First install Debian versions of pip::

    sudo apt-get install python-pip python3-pip

Next upgrade your pip, using pip itself.  If you are using both python 2 and
python 3 versions, upgrade the one you want to own the pip command last::

    # Upgrade pip for Python 3 installs
    sudo pip3 install --upgrade pip
    # Upgrade pip for Python 2 installs (this one owns "pip" now)
    sudo pip2 install --upgrade pip

Now check the pip version is >= 6.0::

    pip --version
    pip3 --version

*********************************
Install, update virtualenvwrapper
*********************************

``virtualenvwrapper`` is a very useful |--| er |--| wrapper around |--| er
|--| ``virtualenv``, that makes it easier and neater to have a library of
virtual Python environments::

    # Get basic version with shell integration
    sudo apt-get install virtualenvwrapper
    # Upgrade to latest
    sudo pip install --upgrade virtualenvwrapper

The ``--upgrade`` is important because virtualenv (installed by
virtualenvwrapper) contains its own copy of pip.  We need the latest version
of virtualenv to make sure we will get a recent version of pip in our
virtualenvs.

The ``virtualenvwrapper`` apt package puts useful aliases into the default
bash shell environment.  To get these aliases loaded up in your current shell,
this one time you should do::

    source ~/.bashrc

*********************************************
Set up the system to build some common wheels
*********************************************

Install standard build dependencies for common libraries::

    sudo apt-get build-dep python-numpy python-scipy matplotlib h5py

This may take about 10-20 minutes (at least, it did on my virtualbox / Vagrant
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
the path containing packages that have been installed with the pip ``--user``
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
off the path.  To do this, I have the following in my
``~/.virtualenvs/postactivate`` file::

    # Clear user Python binary path when using virtualenvs
    export PATH=$(echo $PATH | sed "s|${PY_USER_BIN}:\{0,1\}||")

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

*********************************************
Doesn't work for you?  Help improve this page
*********************************************

If you try the instructions here, and you can't get a particular package or
set-up to work, then why not make an `issue <pydagogue issues>`_ for the
repository hosting these pages, and I'll see if I can work the fix into this
page somewhere.

.. include:: links_names.inc
