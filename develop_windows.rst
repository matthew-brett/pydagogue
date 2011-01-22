#####################
Developing on windows
#####################

This is a sketch of the steps that I (MB) went through setting up a
semi-standard development environment for python_ packaging on windows.

************
My system(s)
************

* A standard XP installation currently running (My Computer -> Properties)
  version 2002, service pack 3.
* An XP running via Parallels_ on my Macbook Air

***********
Basic setup
***********

* Install windows powershell_ . I find this a lot more convenient than the
  standard windows ``cmd`` shell; it has good command and filename completion,
  ``ls`` for directory listing, a less idiosyncratic ``cd``, and a scripting
  language that is a lot less painful than ``cmd`` bat scripting. I believe
  I've used version 1 and version 2 (``$Host.version``` is ``1 0 0 0`` on my
  standard XP installation.
* Install msysgit_. In the installation, set ``git`` to be on the command path,
  but not the git bash utilities.  I set the repo to have LF endings, but the
  checked out files to have system endings. You'll see this setting offered in
  the installation GUI - it sets ``core.autocrlf=input`` in your global git
  config.
* Install putty_.  Well, in fact, install all the putty utilities via the
  windows installer - including *plink* and *pageant*.  These are utilities we
  need for handling ssh authentication for git and other tools.
* Get necessary ssh keys via sftp (installed by Putty installer)
* Run *PUTTYgen* (installed by the Putty installer) to import the Unix ssh key
  into putty ``.ppk`` format.  Save ``.ppk`` in ``$HOME/.ssh``.
* Start *pageant* (installed by putty installer).  Add ``.ppk`` key file.
* Check we can get authenticated e.g. into github with ``"c:\Program
  files\Putty\plink git@github.com"``.
* Set a couple of environment variables from powershell - see
  `powershell environment variables`_.  First set ``$GIT_SSH`` to pick up
  *plink* as the ssh executable::

    [Environment]::SetEnvironmentVariable("GIT_SSH", "C:\Program files\Putty\plink.exe", "User")

  Next we make sure that ``$HOME`` is set for safety.  For example, setuptools_
  appears to need it set correctly - see the `example pypi`_ page for the
  assertion at least::

    [Environment]::SetEnvironmentVariable("HOME", $env:USERPROFILE, "User")

  Restart powershell after doing this to pick up the ``GIT_SSH`` environment
  variable in particular.  We should now be able to do something like ``git
  clone git@github.com:my-name/my-repo.git`` without being asked our password
  (pageant handles this).
* Install editor.  I use vim_.  Actually, I used vim_ with command-t_, requiring
  (at the moment) vim 7.2.  See below for more command-t_ goodness.
* Install python_ - the current version.  I need this for the scripts installing the
  personal configuration below.
* Set up personal configuration.  For me this is something like::

    cd c:\
    mkdir code
    cd code
    mkdir dev_trees
    cd dev_trees
    git clone git@github.com:matthew-brett/myconfig.git
    git clone git@github.com:matthew-brett/myvim.git
    cd myconfig
    c:\Python26\python make.py dotfiles
    cd ..\myvim
    c:\Python26\python make.py vimfiles

* (For my own vim comfort) Install command-t.  See the `command-t README`_.
  Because of ruby incompatibility problems, we need to use vim_ 7.2.  Because
  we're using this old version of vim, we also need python 2.4 installed (not
  necessarily as default).  As of Jan 2011, we need ruby 1.8.7, and the ruby
  devkit.  Set the install option to add ruby to the path when running the ruby
  installer.  Unpack the devkit to ``c:\devkit``.  Start powershell and source
  the devkit variables with ``c:\devkit\devkitvar.ps1``.  Then::

    cd ~\vimfiles\bundle\command-t\ruby\command-t
    ruby extconf.rb
    make

.. _python: http://www.python.org
.. _parallels: http://www.parallels.com
.. _powershell: http://www.microsoft.com/powershell
.. _mysysgit: http://code.google.com/p/msysgit
.. _putty: http://www.chiark.greenend.org.uk/~sgtatham/putty
.. _powershell environment variables: http://technet.microsoft.com/en-us/library/ff730964.aspx
.. _example pypi: http://packages.python.org/an_example_pypi_project/setuptools.html#intermezzo-pypirc-file-and-gpg
.. _vim: http://www.vim.org
.. _command-t: https://wincent.com/products/command-t
.. _command-t README: http://git.wincent.com/command-t.git/blob_plain/master:/README.txt
