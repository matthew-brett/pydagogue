##########################
Windows DLLs - information
##########################

Exploring where to put Windows DLLs for load-time or run-time discovery.

* Commentary `shared libraries in windows
  <https://ghc.haskell.org/trac/ghc/wiki/SharedLibraries/Management#OnWindows>`_
  on the Glasgow Haskell Compiler wiki.  See discussion of side-by-side
  assemblies.
* Microsoft documentation on `SetDllDirectory
  <http://msdn.microsoft.com/en-us/library/ms686203.aspx>`_. From those docs:

     The SetDllDirectory function affects all subsequent calls to the
     LoadLibrary and LoadLibraryEx functions. It also effectively disables safe
     DLL search mode while the specified directory is in the search path.


  So this call might have unexpected conseequences for unrelated DLL loading
  afterwards.
* Microsoft documentation on the `LoadLibraryEx
  <http://msdn.microsoft.com/en-us/library/windows/desktop/ms684179.aspx>`_
  call. On ``SetDllDirectory``:

    However, be aware that using SetDllDirectory effectively disables safe DLL
    search mode while the specified directory is in the search path and it is
    not thread safe. However, be aware that using SetDllDirectory effectively
    disables safe DLL search mode while the specified directory is in the search
    path and it is not thread safe.  If possible, it is best to use
    AddDllDirectory to modify a default process search path.

* Microsoft documentation on `AddDllDirectory
  <http://msdn.microsoft.com/en-us/library/windows/desktop/hh310513.aspx>`_
* Microsoft documentation on the `Standard DLL search order
  <http://msdn.microsoft.com/en-us/library/ms682586.aspx#standard_search_order_for_desktop_applications>`_
  for desktop applications.
* The `alternate DLL search order
  <http://msdn.microsoft.com/en-us/library/windows/desktop/ms682586.aspx#alternate_search_order_for_desktop_applications>`_
  that is triggered by calling DLL loading with the flag
  `LOAD_WITH_ALTERED_SEARCH_PATH`.
* Python loads extensions with::

    hDLL = LoadLibraryEx(pathname, NULL,
                         LOAD_WITH_ALTERED_SEARCH_PATH);

  See: `dynload_win.c line 195
  <http://hg.python.org/cpython/file/3a1db0d2747e/Python/dynload_win.c#l195>`_
  in Python 2.7 - for example.
* Microsoft documentation on `Private side by side assemblies
  <http://msdn.microsoft.com/en-us/library/windows/desktop/ff951638.aspx>`_
