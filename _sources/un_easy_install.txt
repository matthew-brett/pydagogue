.. _un-easy-install:

##############################################
Clean out packages installed with easy_install
##############################################

If you have never used easy_install_ on your system you don't need to read
any further - congratulations!

If you have used easy_install in the past, you might run into some
difficult-to-diagnose installation problems.  To avoid these, we suggest you
remove any packages you previously installed with easy_install.

First you need to find the packages installed with easy_install.  To do this,
find the ``site-packages`` or ``dist-packages`` directory to which
easy_install will have installed. You can check the location of installation
directories by looking at the contents of ``sys.path`` at the Python prompt::

    $ python
    >>> import sys
    >>> print("\n".join(sys.path))

Some common ``site-packages`` / ``dist-packages`` directory locations follow.
The ``X.Y`` in ``pythonX.Y`` refers to your Python version, so ``pythonX.Y``
corresponds to ``python2.7`` for Python 2.7 etc.

* Debian / Ubuntu system installation:
  ``/usr/local/lib/pythonX.Y/dist-packages`` (see:
  :ref:`debian-python-places`);
* Fedora system installation for pure Python packages:
  ``/usr/lib/pythonX.Y/site-packages``;
* Fedora 64-bit system installation for packages with compiled extensions:
  ``/usr/lib64/pythonX.Y/site-packages``;
* Linux home installation:
  ``$HOME/.local/lib/pythonX.Y/site-packages``
* OSX Python.org installation:
  ``/Library/Frameworks/Python.framework/Versions/X.Y/lib/pythonX.Y/site-packages``;
* OSX Python user installation:
  ``$HOME/Library/Python/X.Y/lib/python/site-packages``;

Look in your site-packages / dist-packages directory for a file called
``easy-install.pth``.  If no such file exists, you have no easy_install
installs in that directory.

If the file does exist, look for the packages listed in the file.  The file
will look something like::

    import sys; sys.__plen = len(sys.path)
    ./requests-0.12.1-py2.7.egg
    ./oauthlib-0.1.3-py2.7.egg
    ./certifi-0.0.8-py2.7.egg
    ./rsa-3.0.1-py2.7.egg
    ./pyasn1-0.1.3-py2.7.egg
    import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)

Delete each directory listed. For example, if your package directory
containing the ``easy-install.pth`` file was
``/usr/local/lib/python2.7/dist-packages`` then::

    rm -rf /usr/local/lib/python2.7/dist-packages/requests-0.12.1-py2.7.egg
    rm -rf /usr/local/lib/python2.7/dist-packages/oauthlib-0.1.3-py2.7.egg

etc.  When you have finished deleting these directories, delete the
``easy-install.pth`` file.  Repeat for each potential package directory.

If you need these packages, then you can re-install them using `pip`_.

.. include:: links_names.inc
