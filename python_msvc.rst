####################################
Using Microsoft Visual C with Python
####################################

*******************************
Visual studio compiler versions
*******************************

Here is a list of Visual Studio / `Visual C++
<http://en.wikipedia.org/wiki/Visual_C%2B%2B>`_ version numbers, the value of
the defined ``_MSC_VER`` during compilation, the alternative year-based name,
and the C / C++ runtime library.

For sources on version numbers / ``_MSC_VER``:

* `a stackoverflow table
  <http://stackoverflow.com/questions/3592805/detecting-compiler-versions-during-compile-time>`_;
* a `sourceforge wiki page on compilers
  <http://sourceforge.net/p/predef/wiki/Compilers>`_;
* `stackoverflow answer on VC and Python
  <http://stackoverflow.com/questions/2676763/what-version-of-visual-studio-is-python-on-my-computer-compiled-with>`_.

For VC runtime libraries:

* a `list of VS versions / CRTS
  <https://support.microsoft.com/en-us/kb/154753>`_;
* a `history of the MS CRTS
  <http://yuhongbao.blogspot.com/2014/10/the-history-of-ms-c-runtime-dll.html>`_;
* the MS `C runtime library pages
  <https://msdn.microsoft.com/en-us/library/abx4dbyh(v=vs.100).aspx>`_;

============  ======== ==================  =============   =============
VC++ version  _MSC_VER Alternative name    C runtime       C++ runtime
============  ======== ==================  =============   =============
1.0           800                          MSVCRT10.DLL
2.0           900                          MSVCRT20.DLL
4.0           1000                         MSVCRT40.DLL
4.2           1020                         MSVCRT.DLL
5.0           1100     Visual Studio 97    MSVCRT.DLL      MSVCP50.DLL
6.0           1200                         MSVCRT.DLL      MSVCP60.DLL
7.0           1300     Visual Studio 2002  MSVCR70.DLL     MSVCP70.DLL
7.1           1310     Visual Studio 2003  MSVCR71.DLL     MSVCP71.DLL
8.0           1400     Visual Studio 2005  MSVCR80.DLL     MSVCP80.DLL
9.0           1500     Visual Studio 2008  MSVCR90.DLL     MSVCP90.DLL
10.0          1600     Visual Studio 2010  MSVCR100.DLL    MSVCP100.DLL
11.0          1700     Visual Studio 2012  MSVCR110.DLL    MSVCP110.DLL
12.0          1800     Visual Studio 2013  MSVCR120.DLL    MSVCP120.DLL
14.0          1900     Visual Studio 2015  See notes       MSVCP140.DLL
============  ======== ==================  =============   =============

For a discussion of the generic ``MSVCRT.DLL`` compared to the DLLs specific
to the VC version, see `this blog post
<https://kobyk.wordpress.com/2007/07/20/dynamically-linking-with-msvcrtdll-using-visual-c-2005>`_.
See also `these comments on using MSVCRT.DLL from Mingw-w64
<http://sourceforge.net/p/mingw-w64/wiki2/The%20case%20against%20msvcrt.dll>`_.

For 2015, MS split the C runtime into two component libraries.  See:

* blog post on the `the universal CRT
  <http://blogs.msdn.com/b/vcblog/archive/2015/03/03/introducing-the-universal-crt.aspx>`_
* Steve Dower's first blog post: `Python 3.5 extensions part 1
  <http://stevedower.id.au/blog/building-for-python-3-5>`_;
* Steve's second blog post: `Python 3.5 extensions part 2
  <http://stevedower.id.au/blog/building-for-python-3-5-part-two>`_;

The CRT components are:

* ``ucrtbase.dl``: "The Universal CRT (UCRT) contains the functions and
  globals exported by the standard C99 CRT library. The UCRT is now a Windows
  component, and ships as part of Windows 10." (see `CRT 2015
  <https://msdn.microsoft.com/en-us/library/abx4dbyh.aspx>`_).
* ``vcruntime140.dll`` : "The vcruntime library contains Visual C++ CRT
  implementation-specific code, such as exception handling and debugging
  support, runtime checks and type information, implementation details and
  certain extended library functions. This library is specific to the version
  of the compiler used." (`CRT 2015`_);

The C++ runtime for VS2015 is ``MSVCP140.dll`` (`CRT 2015`_).

******************************************************************
Visual Studio versions used to compile distributed Python binaries
******************************************************************

See:
http://stackoverflow.com/questions/12028762/what-version-of-visual-studio-and-or-mingw-do-i-need-to-build-extension-modules

and: http://stackoverflow.com/questions/9047072/windows-python-version-and-vc-redistributable-version

The version of Visual Studio is described in ``readme.txt`` in the ``PCBuild``
folder of the source distribution.  The full Visual C++ version number is in
either ``release.vsprops`` or ``release.props``.  I read these files from the
`CPython Hg web interface <http://hg.python.org/cpython/tags>`_ for each tagged
release.

============== ============
Python version VC++ version
============== ============
2.5.6          7.1
2.6.9          9.0
2.7.6          9.0
3.2.3          9.0
3.3.5          10.0
3.4.0          10.0
3.5.0          14.0
============== ============

****************************************************
Installing free versions of Microsoft Visual C / C++
****************************************************

Pythons 2.7 (and 3.2)
=====================

If you are compiling for Python 2.7, you should first try the installer at
http://aka.ms/vcpython27.  I installed this for all users from a ``cmd``
Window opened with "run as administrator", like this::

    msiexec /i VCForPython27.msi ALLUSERS=1

This command line comes from the "Install instructions" on the download page.
For me, the installer runs but closes without showing any signs that it has
finished.  The compilers seem to work fine nevertheless.  If this standalone
Python 2.7 compiler set works for you, you should be able to compile both 32
and 64 bit extensions without further configuration.  If not, see
:ref:`other-options`.

Pythons 3.3 and 3.4
===================

For Pythons 3.3 and 3.4 I recommend you get your compilers via the Window 7.1
SDK.  This includes the VS 10 / 2010 command line compilers you need to
compile Python extensions.  I found that I needed to install from the `offline
ISO files <https://www.microsoft.com/en-us/download/details.aspx?id=8442>`_.
As you will see in the "Install Instructions", choose ``GRMSDK_EN_DVD.iso``
for 32-bit compilation and / or ``GRMSDKX_EN_DVD.iso`` for 64-bit compiles.

I believe Windows 8, 10 and server 2012 can mount ISO files from explorer.
For Windows 7 / server 2008 I used `Virtual clone drive
<http://www.slysoft.com/en/virtual-clonedrive.html>`_ to mount the ISO files.

Finally, for 64-bits, I needed to apply this patch to avoid a distutils
compilation error ending in ``ValueError: ['path']``::

  echo "C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\SetEnv.cmd" /x64 > "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\bin\amd64/vcvars64.bat"

See `this MSVC 2010 SO post
<http://stackoverflow.com/questions/32091593/cannot-install-windows-sdk-7-1-on-windows-10>`_
for details on installing the Windows 7.1 SDK, and `this SO answer
<http://stackoverflow.com/questions/26473854/python-pip-has-issues-with-path-for-ms-visual-studio-2010-express-for-64-bit-ins>`_
for specifics on the 64-bit distutils error that can be fixed with the
``echo`` command above.

Python 3.5
==========

For Python 3.5 32-bit and 64-bit extensions you need MSVC 14 / 2015. `VS 2015
community edition
<https://www.visualstudio.com/products/visual-studio-community-vs>`_ is free
as in beer.  It's a huge 11GB install which took more than an hour on my
machine.

.. _other-options:

***********************************
Other options for MSVC installation
***********************************

If the VS for Python 2.7 installer doesn't work for you, or you can't get VS
2010 compilation working for 3.3 / 3.4, see the links below.

In overview, you may be able to find the free Visual Studio express download
that you need on the Microsoft site, but until VS 2015, these do not compile
64-bit extensions by default.   The instructions above give the easiest way to
get 64-bit compiles working, but you can also try the other methods given in
the links below.

***********************************
Some older links on installing MSVC
***********************************

Here are some links that were useful at some point:

* `Cython windows wiki page
  <https://github.com/cython/cython/wiki/CythonExtensionsOnWindows#using-microsoft-visual-c-compiler-for-python-only-for-python-27x>`_.
  This has more on configuration for 64-bit in particular.
* `VS downloads <http://www.visualstudio.com/downloads/download-visual-studio-vs>`_
* `VS 2010 SDK <http://www.microsoft.com/en-us/download/details.aspx?id=2680>`_
* `How to configure VS 10.0 for 64 bit
  <http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.100%29.aspx>`_
* `VS 2008 download <http://go.microsoft.com/?linkid=7729279>`_
* Some `relevant instructions from a MATLAB user
  <http://www.mathworks.com/matlabcentral/answers/98351-how-can-i-set-up-microsoft-visual-studio-2008-express-edition-for-use-with-matlab-7-7-r2008b-on-64>`_
  for getting the VS 2008 SDK set up (the default downloads will refuse to
  install onto VS express).
* `How to configure VS 9.0 for 64 bit
  <http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.90%29.aspx>`_
