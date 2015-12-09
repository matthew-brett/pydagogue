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
14.0          1900     Visual Studio 2015  See notes       See notes
============  ======== ==================  =============   =============

For a discussion of the generic ``MSVCRT.DLL`` compared to the DLLs specific
to the VC version, see `this blog post
<https://kobyk.wordpress.com/2007/07/20/dynamically-linking-with-msvcrtdll-using-visual-c-2005>`_.
See also `these comments on using MSVCRT.DLL from Mingw-w64
<http://sourceforge.net/p/mingw-w64/wiki2/The%20case%20against%20msvcrt.dll>`_.

For 2015, MS split the C runtime into several component libraries.  See:

* http://blogs.msdn.com/b/vcblog/archive/2014/06/10/the-great-crt-refactoring.aspx
* https://msdn.microsoft.com/en-us/library/abx4dbyh.aspx

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

If you are only compiling for 32 bit, you can use the Visual Studio Express
package (2008==9.0, 2010==10.0).

For 64 bit compilation, you'll need the matching SDK, and you don't need Visual
Studio Express - see:
https://github.com/cython/cython/wiki/64BitCythonExtensionsOnWindows

Here are some useful links:

* `VS downloads <http://www.visualstudio.com/downloads/download-visual-studio-vs>`_
* `VS 2010 SDK <http://www.microsoft.com/en-us/download/details.aspx?id=2680>`_
* `How to configure VS 10.0 for 64 bit
  <http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.100%29.aspx>`_
* `VS 2008 download <http://go.microsoft.com/?linkid=7729279>`_
* Some `relevant instructions from a MATLAB user
  <http://www.mathworks.com/matlabcentral/answers/98351-how-can-i-set-up-microsoft-visual-studio-2008-express-edition-for-use-with-matlab-7-7-r2008b-on-64>`_
  for getting the VS 2008 SDK set up (the default downloads will refuse to install onto the VS express).
* `How to configure VS 9.0 for 64 bit <http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.90%29.aspx>`_

It's useful to be able to mount the downloaded ISO images directly for
installation.  I had good success with `Virtual clone drive
<http://www.slysoft.com/en/virtual-clonedrive.html>`_.
