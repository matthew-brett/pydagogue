#########################
Installing python scripts
#########################

This here is to explain to myself how Python distutils_, distribute_ /
setuptools_ and pip_ install scripts on Unix and Windows.

*******************
Your basic disutils
*******************

See: http://docs.python.org/2/distutils/setupscript.html#installing-scripts

You just tell your ``setup.py`` that some files are scripts. Let's make a
trivial ``setup.py``::

    from os.path import join as pjoin
    from distutils.core import setup

    setup(
        scripts=[pjoin('bin', 'myscript')]
        )

and a script ``bin/myscript``::

    #!/usr/bin/env python
    print("Oh what a giveaway!")

Note the shebang line pointing to ``/usr/bin/env python``. 

Put into a virtualenv::

    virtualenv apython
    cd apython
    . bin/activate # on Unix
    # back to the little script
    cd ~/tmp/scripter
    python setup.py install

Gives::

    running install
    running build
    running build_scripts
    creating build/scripts-2.7
    copying and adjusting bin/myscript -> build/scripts-2.7
    changing mode of build/scripts-2.7/myscript from 644 to 755
    running install_scripts
    copying build/scripts-2.7/myscript -> /home/mb312/tmp/apython/bin
    changing mode of /home/mb312/tmp/apython/bin/myscript to 755
    running install_egg_info
    Writing /home/mb312/tmp/apython/lib/python2.7/site-packages/UNKNOWN-0.0.0-py2.7.egg-info

The contents of ``/home/mb312/tmp/apython/bin/myscript`` are::

    #!/home/mb312/tmp/apython/bin/python
    print("Oh what a giveaway!")

Note the new shebang line, imported from the python doing the installation.

Here is the contents of the installed script on Windows, installing with
``C:\Python26\python.exe``::

    #!C:\Python26\python.exe
    print("Oh what a giveaway!")

*************************************
But - shebang doesn't work on windows
*************************************

The top line in the script above::

    #!C:\Python26\python.exe

is more or less useless because Windows does not pay attention to the ``#!``
first line of scripts.  In fact there is no way of executing this script in
windows except via ``python scripts\myscript``.  We have a few options to solve
this, by post-processing in the install step of a disutils run:

* Rename ``myscript`` to ``myscript.py``.  Use the windows default extension
  association mechanism to associate this ``.py`` file with whichever Python is
  the default opener for ``.py`` files. This will of course ignore the Python
  executable on the first line, and use the Python associated with ``.py``
  files.  For example, if you tried to install the scripts into a virtualenv::

        PS C:\tmp\scripter> virtualenv ../myvenv
        New python executable in ../myvenv\Scripts\python.exe
        Installing setuptools................done.
        Installing pip...................done.
        PS C:\tmp\scripter> ..\myvenv\Scripts\activate
        (myvenv) PS C:\tmp\scripter> get-command python

        CommandType     Name                                                Definition
        -----------     ----                                                ----------
        Application     python.exe                                          C:\tmp\myvenv/Scripts\python.exe
        Application     python.exe                                          C:\Python26\python.exe


        (myvenv) PS C:\tmp\scripter> python setup.py install
        running install
        running build
        running build_scripts
        creating build
        creating build\scripts-2.6
        copying and adjusting bin\myscript -> build\scripts-2.6
        running install_scripts
        copying build\scripts-2.6\myscript -> C:\tmp\myvenv\Scripts
        running install_egg_info
        Writing C:\tmp\myvenv\Lib\site-packages\UNKNOWN-0.0.0-py2.6.egg-info
        (myvenv) PS C:\tmp\scripter> cat ..\myvenv\Scripts\myscript
        #!C:\tmp\myvenv\Scripts\python.exe
        print("Oh what a giveaway!")

  If I run the installed script by the command line, I'm going to invoke the
  default python not the virtualenv python, as I might have expected.
* Make something that is executable to wrap round the script.  For example, I
  might make a wrapper for ``myscript`` called ``myscript.bat``, like this::

    @C:\tmp\myvenv\Scripts\python.exe c:\tmp\myvenv\Scripts\myscript

  Now executing ``myscript`` will find ``myscript.bat`` which will run the file.
  This leaves us with one remaining problem; binary installs.  What if we want
  to make a windows ``.exe`` installer via ``setuptools``.  We just add ``import
  setuptools`` to the top of the ``setup.py`` script above, then run ``python
  setup.py bdist_wininst`` - hey presto, we get a windows installer,
  ``bdist\scripter-1.0.win32.exe`` (say).  That has all the processed ``.bat``
  files in it.  But the processing, which was fine for the python from which we
  made the installer, may well not be right for a python that does the install,
  via ``easy_install scripter-1.0.win32.exe``.

**************************************************
pip, easy_install, setuptools and windows shebangs
**************************************************


.. include:: links_names.inc
