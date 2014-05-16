.. Don't forget to escape $ when not using math

#####################
Developing on windows
#####################

This is a sketch of the steps that I (MB) went through setting up a
semi-standard development environment for python_ packaging on windows.

************
My system(s)
************

* A standard XP installation booted directly into (My Computer -> Properties)
  XP version 2002, service pack 3.
* An XP running via Parallels_ on my Macbook Air with version 2002 SP3 also.
* Windows 7 professional 64 bit installed on a first generation MacBook Air.
  Currently on SP1.

***********
Basic setup
***********

* If you have Windows XP, install windows powershell_ (it is standard for
  Windows 7). I find powershell a lot more convenient than the standard windows
  ``cmd`` shell; it has good command and filename completion, ``ls`` for
  directory listing, a less idiosyncratic ``cd``, and a scripting language that
  is a lot less painful than ``cmd`` bat scripting. I believe I've used version
  1 and version 2. ``\$Host.version`` is ``1 0 0 0`` on my standard XP
  installation. Don't forget to enable `quickedit mode
  <http://support.microsoft.com/kb/282301>`_ for much nicer right click copy and
  paste.
* Install msysgit_. In the installation, set ``git`` to be on the command path,
  but not the git bash utilities.  I set the repo to have LF endings, but the
  checked out files to have system endings. You'll see this setting offered in
  the installation GUI - it sets ``core.autocrlf=input`` in your global git
  config.

*********
SSH setup
*********

msysgit has ssh, but for various reasons I wanted to be able to use powershell
with git.  In order to do this I need to get git SSH authentication working via
the windows tools:

* Install putty_.  Well, in fact, install all the putty utilities via the
  windows installer - including *plink* and *pageant*.  These are utilities we
  need for handling ssh authentication for git and other tools.
* You might consider putting the Putty directory on the path. Something like::

    \$my_path = [Environment]::GetEnvironmentVariable("PATH","User")
    \$my_path += ";C:\Program files (x86)\Putty" # (x86) on my windows 7 system
    [Environment]::SetEnvironmentVariable("PATH", \$my_path, "User")

* I have ssh keys I use on unix and mac.  I got the necessary ssh keys via sftp
  (installed by Putty installer). These went into ``\$HOME/.ssh``. I then ran
  *PUTTYgen* (installed by the Putty installer) to import the Unix ssh key into
  putty ``.ppk`` format.  Save ``.ppk`` in ``\$HOME/.ssh``.
* Start *pageant* (installed by putty installer).  Add ``.ppk`` key file.
* If you've got the putty utilities on the path, check you can get authenticated
  e.g. into github with ``plink git@github.com``.  If you don't have putty etc
  on the path, you'll need the full path to plink, as in: ``"c:\Program files
  (x86)\Putty\plink git@github.com"``.
* Set a couple of environment variables from powershell - see
  `powershell environment variables`_.  First set ``\$GIT_SSH`` to pick up
  *plink* as the ssh executable::

    [Environment]::SetEnvironmentVariable("GIT_SSH", "C:\Program files\Putty\plink.exe", "User")

  Next we make sure that ``\$HOME`` is set for safety.  For example, setuptools_
  appears to need it set correctly - see the `example pypi`_ page for the
  assertion at least::

    [Environment]::SetEnvironmentVariable("HOME", \$env:USERPROFILE, "User")

  Restart powershell after doing this to pick up the ``GIT_SSH`` environment
  variable in particular.  We should now be able to do something like ``git
  clone git@github.com:my-name/my-repo.git`` without being asked our password
  (pageant handles this).  The first time you use this combination with a
  particular host you may get an error like this::

    The server's host key is not cached in the registry. You
    have no guarantee that the server is the computer you
    think it is.

  If so, run *plink* manually to cache the key::

    & 'C:\Program Files (x86)\PuTTY\plink.exe' git@github.com

  and press ``y`` when asked.
* I run pageant at startup.  I first set up a desktop shortcut with the
  following command::

    "C:\Program Files (x86)\PuTTY\pageant.exe" c:\Users\mb312\.ssh\id_dsa.ppk

  I move this shortcut into my startup folder to start at login.  On windows 7
  my startup folder is::

    C:\Users\mb312\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

  where ``mb312`` is my username.
* For using ssh inside the msysgit bash shell, I like to add the keychain-like
  script, by including this in my ``~/.bashrc`` file::

    # Source personal definitions
    if [ -f "\$HOME/.bash_keychain_lite" ]; then
        . "\$HOME/.bash_keychain_lite"
    fi

  where the ``.bash_keychain_lite`` file arises from the ``make.py dotfiles``
  command above.

Miscellaneous
=============

* I got used to the mac keyboard way of using the command key for things like
  making new tabs in the browser (command-t), copy, paste (command-c, command-v)
  and so on. I can't replicate all of this on windows, but as a first pass, I
  use an autohotkey_ script.  Putting this ``remap.ahk`` script file into my
  Windows start menu startup folder caused it to be loaded at login::

    ; From: http://superuser.com/questions/241889/macbook-pro-windows-7-remap-cmd-key-to-ctrl-except-cmdtab-to-alttab
    ; See also : http://www.autohotkey.com/docs/Hotkeys.htm
    ; # usually means Windows key.
    #SingleInstance force ; but sometimes # introduces a command
    #r::Send ^r ;reload
    #z::Send ^z ; undo
    #y::Send ^y ; redo
    #f::Send ^f ; find inside apps
    #g::Send ^g ; repeat find inside apps
    #c::Send ^c ; copy
    #x::Send ^x ; cut
    #v::Send ^v ; paste
    #a::Send ^a ; select all
    #t::Send ^t ; new tab in browser (IE, Safari, Firefox, etc)
    #s::Send ^s ; save inside apps
    LWin & Tab::AltTab ; the motherlode, alt-tab!

    #Up::Send {PgUp} ; PgUp
    #Down::Send {PgDn} ; PgDown
    #Left::Send {home} ; Home
    #Right::Send {end} ; End
    #LButton::^LButton

* I depend heavily on knowing which branch I am on when using git.  This is the
  what the ``git-completion`` bash routines do; posh-git_ does the equivalent
  for powershell.

Other programs
==============

* Install editor.  I use vim_.  With a 64 bit python (below), I needed a `64 bit
  vim`_
* Install python_ - the current version.  I need this for the scripts installing
  the personal configuration below.  For the convenience of using python at the
  command line you could do something like::

    \$my_path = [Environment]::GetEnvironmentVariable("PATH","User")
    \$my_path += ";C:\Python27;C:\Python27\Scripts"
    [Environment]::SetEnvironmentVariable("PATH", \$my_path, "User")

* Set up personal configuration.  For me this is::

    cd c:\
    mkdir code
    cd code
    mkdir dev_trees
    cd dev_trees
    git clone git@github.com:matthew-brett/myconfig.git
    git clone git@github.com:matthew-brett/myvim.git
    cd myconfig
    python make.py dotfiles
    cd ..\myvim
    python make.py vimfiles

* I am trying out virtualenvwrapper-powershell_ . Install with the standard
  ``python setup.py install``.  You then need ``import-module
  virtualenvwrapper`` from the powershell prompt.  Maybe it goes better in a
  `powershell profile`_.
* As for any other environment, the nose-ipdb_ ipython debugger for nose_ makes
  debugging easier for nose tests.  Easiest route is ``easy_install
  ipdbplugin``.

.. _win-compile-tools:

********************************
Windows compiler and build tools
********************************

* Download and install the mingw_ windows compiler.  I used the
  ``mingw-get-inst`` automated installation route.  Select the options giving
  you c++, fortran, and the msys build environment.  I didn't directly add these
  to the path, but made a script ``c:\Mingw\mingwvars.ps1``::

    # convenience script to add mingw to path
    echo "Adding mingw to PATH..."
    \$mingw = [System.IO.Path]::GetDirectoryName(\$MyInvocation.MyCommand.Definition)
    \$env:path = "\$mingw\bin;\$mingw\msys\1.0\bin;\$env:path"

  Then in powershell - ``. c:\Mingw\mingwvars.ps1`` to add the msys and
  mingw tools to the path.

* Using mingw, you might get this kind of error::

    error: Setup script exited with error: Unable to find vcvarsall.bat

  Of course you've already tried the standard solution to this, of the form::

    python setup.py build --compiler=mingw32

  If that doesn't work, you might have hit a `mingw distutils bug`_.  One
  suggested fix is to make a ``distutils.cfg`` file in your Python distutils
  directory (e.g.  ``C:\Python26\Lib\distutils``) with the following content::

    [build]
    compiler=mingw32

****
SWIG
****

Download the swig version for windows, ``swigwin``, from `swig downloads`_,
unpack into, say, ``C:\``, then::

    \$my_path = [Environment]::GetEnvironmentVariable("PATH","User")
    \$my_path += ";C:\swigwin-2.0.10"
    [Environment]::SetEnvironmentVariable("PATH", \$my_path, "User")
    [Environment]::SetEnvironmentVariable("PYTHON_INCLUDE", "C:\Python27\include", "User")
    [Environment]::SetEnvironmentVariable("PYTHON_LIB", "C:\Python27\libs\python27.lib", "User")


.. _powershell environment variables: http://technet.microsoft.com/en-us/library/ff730964.aspx
.. _mingw distutils bug: http://bugs.python.org/issue2698
.. _64 bit vim: http://code.google.com/p/vim-win3264/wiki/Win64Binaries
.. _mdesktop: http://code.google.com/p/mdesktop/
.. _sharpkeys: http://www.randyrants.com/sharpkeys/
.. _posh-git: https://github.com/dahlbyk/posh-git
.. _virtualenvwrapper-powershell: https://bitbucket.org/guillermooo/virtualenvwrapper-powershell
.. _powershell profile: http://msdn.microsoft.com/en-us/library/windows/desktop/bb613488%28v=vs.85%29.aspx
.. _lifehacker post: http://lifehacker.com/5807358/how-to-get-mac-os-xs-best-features-on-windows
.. _autohotkey: http://ahkscript.org/
.. _swig downloads: http://www.swig.org/download.html

.. include:: links_names.inc
