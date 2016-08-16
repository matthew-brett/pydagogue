#######################################
Notes on Python compiled with MinGW-w64
#######################################

Python.org releases binaries compiled with Microsoft Visual C++ (MSVC) - see
:doc:`python_msvc`.

The MSVC runtimes are not compatible one with another.  That means, that if Python is compiled with version X of MSVC, then you will have to compile all your extension with that same version X, in order to use the same run-time. 

`MinGW-w64`_ links against ``MSVCRT.DLL``.  Quoting from
https://msdn.microsoft.com/en-us/library/abx4dbyh(VS.80).aspx

    What is the difference between msvcrt.dll and msvcr80.dll?

    The msvcrt.dll is now a "known DLL," meaning that it is a system component
    owned and built by Windows. It is intended for future use only by
    system-level components.

See also :ref:`MSVCRT notes <msvcrt-notes>`.  MinGW-w64 also has its own
C runtime for functions not available in ``MSVCRT.DLL``.

In the past, the CPython has resisted supporting MinGW compilation of Python:

* thread on `Support for MinGW Open Source Compiler
  <https://groups.google.com/forum/#!topic/comp.lang.python/xq-R7QILSgU%5B1-25%5D>`_;
* thread on `Reasons not to support MinGW for official Python builds
  <https://groups.google.com/forum/#!topic/comp.lang.python/F1WK28BT8m0>`_;
* a particular `issue building extensions for MinGW
  <https://bugs.python.org/issue4709>`_, with many general comments later in
  the thread.  From that thread, see the `summary by Paul Moore
  <https://bugs.python.org/issue4709#msg243531>`_ `reply by Ruben Van Boxem
  <https://bugs.python.org/issue4709#msg243563>`_ and `notes by Nathaniel Smith
  <https://bugs.python.org/issue4709#msg256897>`_.  For example (Paul Moore
  |--| Python packing authority): "My personal view is that if the scientific
  community comes up with a mingw/gcc toolchain that they are happy with, and
  willing to support, then I would see that as a reasonable target to be "the"
  supported mingw toolchain for distutils."

The `MSYS2`_ project provides patched Python builds (patches for `Python
2 <https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-python2>`_
and `Python
3 <https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-python3>`_).

.. include:: links_names.inc
