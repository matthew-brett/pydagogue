#########################
Installing python scripts
#########################

This here is to explain to myself how Python distutils_, distribute_ /
setuptools_ and pip_ install scripts on Unix and Windows.

The repository at http://github.com/matthew-brett/myscripter has some worked
running examples of script installation in different situations.

****************
The main problem
****************

As we will see, the main problem is that the standard python installation
mechanism, ``distutils``, uses the first line of a script to get the Python
interpreter that will run the script.  A first line of a typical python script
in Unix might look like this::

    #!/usr/local/bin/python

This is called the `shebang <http://en.wikipedia.org/wiki/Shebang_(Unix)>`_
line, from "hash-bang" - referring to the hash (#) and exclamation (!)
characters. The shebang line tells Unix : "Run the rest of this script via the
interpreter ``/usr/local/bin/python``".

When you install python scripts with a certain python interpreter,
say ``/usr/local/bin/python2.6``, distutils changes this line in the installed
script, to::

    #!/usr/local/bin/python2.6

(See: http://docs.python.org/2/distutils/setupscript.html#installing-scripts)

That way we can associate the script with the installing version of Python.

Now the problem; *there is no shebang mechanism in Windows*.  That means that
distutils' trick for Unix will have no useful effect on Windows.

**********************
The problem by example
**********************

In standard distutils, you tell your ``setup.py`` that some files are scripts. Let's make a
trivial ``setup.py``::

    from os.path import join as pjoin
    from distutils.core import setup

    setup(
        name = 'myscripter',
        version = '0.1',
        scripts=[pjoin('bin', 'myscript')]
        )

and a script ``bin/myscript``::

    #!/usr/local/bin/python
    import sys
    print("Python starts at " + sys.prefix)

Note the shebang line pointing to ``/usr/local/bin/python``.

Install into a virtualenv_::

    virtualenv venv
    . venv/bin/activate # on Unix
    python setup.py install
    deactivate

The contents of ``./venv/bin/myscript`` are (in my case)::

    #!/Users/mb312/dev_trees/myscripter/venv/bin/python
    import sys
    print("Python starts at " + sys.prefix)

Note the new shebang line, imported from the python doing the installation.

Here is the contents of the installed script on Windows, after running the
equivalent steps::

    #!C:\repos\myscripter\venv\Scripts\python.exe
    import sys
    print("Python starts at " + sys.prefix)

Again, disutils has modified the Python path in the shebang line.  But this
time, the shebang is useless, because::

    (venv) C:\repos\myscripter>myscript
    'myscript' is not recognized as an internal or external command,
    operable program or batch file.
    (venv) C:\repos\myscripter>venv\Scripts\myscript
    'venv\Scripts\myscript' is not recognized as an internal or external command,
    operable program or batch file.

We could make the script executable on Windows by adding a ``.py`` extension.
This will associate the file with the *default* system python, not the Python
doing the installation; it is the python doing the installation that we want::

    (venv) C:\repos\myscripter>copy venv\Scripts\myscript venv\Scripts\myscript.py
            1 file(s) copied.

    (venv) C:\repos\myscripter>venv\Scripts\myscript.py
    Python starts at C:\Python26

This could be very confusing, because scripts installed in virtualenv, or by
another python (such as Python3) will nevertheless run via the default system
python.

Thus far, not good for us on Windows.

****************************
setuptools - scripts in eggs
****************************

In "setuptools" I include installation methods using setuptools or its variants,
meaning pip_ and distribute_ and setuptools_ itself.

With the ``setup.py`` above, setuptools variants will do the same thing as
``distutils``, modifying the shebang line, but nothing else of interest in
solving our Windows problems.  We can run the same code as above through
setuptools::

    virtualenv venv
    . venv/bin/activate # on Unix
    python setupegg.py install
    deactivate

``setupegg.py`` just imports setuptools and runs our original ``setup.py`` script::

    import setuptools

    if __name__ == '__main__':
        exec(open('setup.py', 'rt').read(), dict(__name__='__main__'))

This results in the code being installed into its own ``egg``.  Thus:

* All code and the scripts go into a zip file
  ``venv/lib/python2.7/site-packages/myscripter-1.0-py2.7.egg``.
* Our actual script as above is now installed into this zip file as item
  ``EGG-INFO/scripts/myscript``, with shebang line modified as for the standard
  distutils install.
* The script that goes onto the path, ``venv/bin/myscript`` (on Unix) now has to
  find the script in the egg and run that.  In this case it has the obscure contents::

    #!/Users/mb312/dev_trees/myscripter/venv/bin/python
    # EASY-INSTALL-SCRIPT: 'myscripter==1.0','myscript'
    __requires__ = 'myscripter==1.0'
    import pkg_resources
    pkg_resources.run_script('myscripter==1.0', 'myscript')

  Note the modified shebang line.

******************************************
Setuptools and console_script entry_points
******************************************

There is another way to define scripts using setuptools, and that is by
using ``entry_points`` pointing to ``console_scripts`` (see:
http://packages.python.org/distribute/setuptools.html#automatic-script-creation
for detail). To use this mechanism, we move the script code into a library. We
make a new library directory ``myscripter``, add an empty file
``myscripter/__init__.py`` to identify this as a package directory, and move the
code for a script into a file ``myscripter/commands.py`` like this::

    import sys

    def my_console_script():
        print("Console python starts at " + sys.prefix)

Then we modify our ``setup.py``::

    import setuptools
    from distutils.core import setup

    setup(
        name='myscripter',
        version='1.0',
        packages = ['myscripter'],
        entry_points = {
            'console_scripts': [
                'my_console_script = myscripter.commands:my_console_script']
        }
        )


Notice we import setuptools at the top.  This modifies (monkey-patches)
disutils, imported below that.  We now depend on setuptools at install time to
write the console script stuff and at run time in finding the installed scripts
via ``pkg_resources`` (see above and below).  We run an install into a
virtualenv (Unix again)::

    virtualenv venv
    . venv/bin/activate
    python setup.py install

Our console script got installed::

    (venv)\$ my_console_script
    Console python starts at /Users/mb312/dev_trees/myscripter/venv/bin/..

The actual ``venv/bin/my_console_script`` file is just a wrapper for setuptools::

    #!/Users/mb312/dev_trees/myscripter/venv/bin/python
    # EASY-INSTALL-ENTRY-SCRIPT: 'myscripter==1.0','console_scripts','my_console_script'
    __requires__ = 'myscripter==1.0'
    import sys
    from pkg_resources import load_entry_point

    sys.exit(
    load_entry_point('myscripter==1.0', 'console_scripts', 'my_console_script')()
    )

So far it just seems confusing for no gain.  But, on Windows, we do get an
executable script::

    C:\repos\myscripter>virtualenv venv
    C:\repos\myscripter>venv\Scripts\activate
    (venv) C:\repos\myscripter>python setup.py install
    (venv) C:\repos\myscripter>my_console_script
    Console python starts at C:\repos\myscripter\venv

How did this happen? The installation put two files in ``venv\Scripts``, which
are ``my_console_script.exe`` and ``my_console_script-script.py``. We recognize
the contents of ``my_console_script-script.py``::

    #!C:\repos\myscripter\venv\Scripts\python.exe
    # EASY-INSTALL-ENTRY-SCRIPT: 'myscripter==1.0','console_scripts','my_console_script'
    __requires__ = 'myscripter==1.0'
    import sys
    from pkg_resources import load_entry_point

    sys.exit(
    load_entry_point('myscripter==1.0', 'console_scripts', 'my_console_script')()
    )

This is the same (bar the shebang line) as the Unix script.  The new thing is
the ``my_console_script.exe`` file.  This is a verbatim copy of a compiled
windows binary file called ``cli.exe`` from the setuptools distribution - see
`Python wrappers for Windows
<http://svn.python.org/projects/sandbox/branches/setuptools-0.6/setuptools/tests/win_script_wrapper.txt>`_.
This ``exe`` binary detects its own name (in this case
``my_console_script.exe``) and looks for a file ``<my-name>-script.py``
in the same directory.  So in this case it looks for
``my_console_script-script.py``.  The ``exe`` file then finds the Python to use
via the shebang line at the beginning of the ``..-script.py`` file, and runs the
``..-script.py`` file using that python.  In effect the ``cli.exe`` copy
``my_console_script.exe`` implements the Unix shebang logic over
``my_console_script-script.py``.

This gets us executable scripts on windows, but it means we have an install
time and a run time dependency on setuptools.  The run-time dependency is
because of the ``from pkg_resources ...`` line in the script file
(``pkg_resources`` is from setuptools).  Personally, I find the
``console_script`` mechanism more obscure than having script files.

**********************************************************************
Making Windows script wrappers via the distutils install-scripts phase
**********************************************************************

An alternative to using setuptools entry points, is to create your own windows
script wrappers when you install the package.  That is, you hook into the
distutils install-scripts phase, identify the scripts that have been installed
by the normal distutils means, and write out Windows script wrappers for each
file.

Overriding the default distutils install-scripts phase
======================================================

The way to hook into the distutils install is to subclass the distutils
``install_scripts`` command like this::

    from os.path import join as pjoin
    from distutils.core import setup
    from distutils.command.install_scripts import install_scripts

    class my_install_scripts(install_scripts):
        def run(self):
            install_scripts.run(self)
            print("Doing something in install")


    setup(
        name='myscripter',
        version='1.0',
        scripts=[pjoin('bin', 'myscript')],
        cmdclass = {'install_scripts': my_install_scripts}
        )

This gets run during ``install`` obviously::

    \$ python setup.py install
    running install
    running build
    running build_scripts
    ...
    changing mode of build/scripts-2.6/myscript from 644 to 755
    running install_scripts
    copying build/scripts-2.6/myscript -> /Users/mb312/dev_trees/myscripter/venv/bin
    changing mode of /Users/mb312/dev_trees/myscripter/venv/bin/myscript to 755
    Doing something in install
    ...

Less obviously, it gets run making a binary installer such as an egg::

    \$ python setupegg.py bdist_egg
    running bdist_egg
    running egg_info
    ...
    running install_lib
    ...
    running install_scripts
    running build_scripts
    creating build/scripts-2.6
    copying and adjusting bin/myscript -> build/scripts-2.6
    changing mode of build/scripts-2.6/myscript from 644 to 755
    creating build/bdist.macosx-10.5-i386/egg/EGG-INFO/scripts
    copying build/scripts-2.6/myscript -> build/bdist.macosx-10.5-i386/egg/EGG-INFO/scripts
    changing mode of build/bdist.macosx-10.5-i386/egg/EGG-INFO/scripts/myscript to 755
    Doing something in install
    ...

Different ways the installer can be run
=======================================

To get some general mechanism working, it's good to review all the possible ways
that your script could get installed on Windows or Unix.  These are:

* Direct installation from the source repository
* Installation from a source archive (``zip`` or ``tar.gz``)
* Installation by double click from a binary ``exe`` installer (Windows) or
  ``mpkg`` installer (OSX).
* Installation by ``easy_install`` from binary ``exe`` installer (Windows) or
  an ``egg`` binary file (any platform)

Let's consider the binary ``egg`` install.  Here you've made a binary egg using
``python setup.py bdist_egg``.  You upload this to pypi_ or some other good
place.  Someone then downloads it, and installs with the equivalent of
``easy_install my_package_version.egg``.

How to know the install-time python for a binary installer?
===========================================================

If we hook into the distutils install-scripts phase (not the ``easy_install``
phase), we saw above that this is run *when we build the binary egg*.  That
means, that the only python we know about, during the distutils install-scripts
phase, is the python with which we build the egg.  However, the python called
within ``easy_install`` on the user's computer, may well be at a different path,
or in a virtualenv.  So we can't know, at the distutils install phase, what
the eventual python path will be.  There is `no way
<http://stackoverflow.com/questions/250038/how-can-i-add-post-install-scripts-to-easy-install-setuptools-distutils>`_
of making a post-install hook for the ``easy_install`` phase on the egg file in
particular.  However, we can rely on the shebang line of the script being set
correctly by the ``easy_install`` phase.

That means that, in order for our distutils install trick to work, we need to
make a windows wrapper like the ``cli.exe`` wrapper from setuptools, that can
analyze the shebang line of the installed script and call python from that.

A fairly simple Windows bat file solution
=========================================

Luckily that is not very hard using some simple windows batch programing.  Here
then is a ``setup.py`` that works with simple script files, and writes out a
Windows wrapper to analyze the script file shebang line::

    from __future__ import with_statement
    import os
    from os.path import join as pjoin, splitext, split as psplit
    from distutils.core import setup
    from distutils.command.install_scripts import install_scripts
    from distutils import log

    BAT_TEMPLATE = \
    r"""@echo off
    set mypath=%~dp0
    set pyscript="%mypath%{FNAME}"
    set /p line1=<%pyscript%
    if "%line1:~0,2%" == "#!" (goto :goodstart)
    echo First line of %pyscript% does not start with "#!"
    exit /b 1
    :goodstart
    set py_exe=%line1:~2%
    call %py_exe% %pyscript% %*
    """


    class my_install_scripts(install_scripts):
        def run(self):
            install_scripts.run(self)
            if not os.name == "nt":
                return
            for filepath in self.get_outputs():
                # If we can find an executable name in the #! top line of the script
                # file, make .bat wrapper for script.
                with open(filepath, 'rt') as fobj:
                    first_line = fobj.readline()
                if not (first_line.startswith('#!') and
                        'python' in first_line.lower()):
                    log.info("No #!python executable found, skipping .bat "
                                "wrapper")
                    continue
                pth, fname = psplit(filepath)
                froot, ext = splitext(fname)
                bat_file = pjoin(pth, froot + '.bat')
                bat_contents = BAT_TEMPLATE.replace('{FNAME}', fname)
                log.info("Making %s wrapper for %s" % (bat_file, filepath))
                if self.dry_run:
                    continue
                with open(bat_file, 'wt') as fobj:
                    fobj.write(bat_contents)


    setup(
        name='myscripter',
        version='1.0',
        packages=['myscripter'],
        scripts=[pjoin('bin', 'myscript')],
        cmdclass = {'install_scripts': my_install_scripts}
        )

See the ``master`` branch of https://github.com/matthew-brett/myscripter for the
full example.  This seems to work for all of the installation methods above,
without requiring setuptools.

.. include:: links_names.inc
