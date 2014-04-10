##############################
Windows extensions with Python
##############################

*******************************
Visual studio compiler versions
*******************************

Here is a list of Visual Studio / Visual C++ version numbers, the value of the
defined ``_MSC_VER`` during compilation, and the alternative year-based name.

See: http://stackoverflow.com/questions/3592805/detecting-compiler-versions-during-compile-time

and: http://stackoverflow.com/questions/2676763/what-version-of-visual-studio-is-python-on-my-computer-compiled-with

and: http://en.wikipedia.org/wiki/Visual_C%2B%2B

============  ======== ================
VC++ version  _MSC_VER Alternative name
============  ======== ================
Version 1.0    800
Version 2.0    900
Version 2.x    900
Version 4.0    1000
Version 5.0    1100
Version 6.0    1200
Version 7.0    1300    Visual Studio 2002
Version 7.1    1310    Visual Studio 2003
Version 8.0    1400    Visual Studio 2005
Version 9.0    1500    Visual Studio 2008
Version 10.0   1600    Visual Studio 2010
Version 11.0   1700    Visual Studio 2012
Version 12.0   1800    Visual Studio 2013
============  ======== ================

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
============== ============

***********************************************
Installing Visual Studio Express (free edition)
***********************************************

You'll need the Visual Studio Express package (2008==9.0, 2010==10.0).

For 64 bit compilation, you'll also need the matching SDK.

See: https://github.com/cython/cython/wiki/64BitCythonExtensionsOnWindows

* `VS downloads <http://www.visualstudio.com/downloads/download-visual-studio-vs>`_
* `VS 2010 SDK <http://www.microsoft.com/en-us/download/details.aspx?id=2680>`_
* `How to configure VS 10.0 for 64 bit
  <http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.100%29.aspx>`_
* `VS 2008 download <http://go.microsoft.com/?linkid=7729279>`_
* Some `good instructions
  <http://www.mathworks.com/matlabcentral/answers/98351-how-can-i-set-up-microsoft-visual-studio-2008-express-edition-for-use-with-matlab-7-7-r2008b-on-64>`_
  for getting the VS 2008 SDK set up (the default downloads will refuse to install onto the VS express).
* `How to configure VS 9.0 for 64 bit <http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.90%29.aspx>`_

Virtual clone drive http://www.slysoft.com/en/virtual-clonedrive.html

http://www.microsoft.com/en-us/download/details.aspx?id=7873

How to configure VS 9.0 for 64 bit: http://msdn.microsoft.com/en-us/library/9yb4317s%28v=vs.90%29.aspx



