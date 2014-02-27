######################
Runtime linking on Mac
######################

**********************
Some files for testing
**********************

With thanks to https://dev.lsstcorp.org/trac/wiki/LinkingDarwin

Create files ``a.cc`` through ``d.cc``

::

    mkdir \$HOME/dyldtest
    cd \$HOME/dyldtest

    cat << EOF > a.cc
    #include <iostream>
    void a() { std::cout << "a()" << std::endl; }
    EOF

    cat > b.cc << EOF
    #include <iostream>
    void a();
    void b() { std::cout << "b()" << std::endl; a(); }
    EOF

    cat > c.cc << EOF
    #include <iostream>
    void b();
    void c() { std::cout << "c()" << std::endl; b(); }
    EOF

    cat > d.cc << EOF
    void c();
    int main(int, char**) { c(); return 0; }
    EOF

Compile them to object files::

    clang++ -c a.cc b.cc c.cc d.cc

Create libraries from a.o and b.o::

    clang++ -o liba.dylib -dynamiclib a.o
    clang++ -o libb.dylib -dynamiclib b.o -L. -la

***************************************************
Using ``otool -L`` to show linked library locations
***************************************************

Notice the ``otool -L`` output for these libraries::

    liba.dylib:
        liba.dylib (compatibility version 0.0.0, current version 0.0.0)
        /usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 120.0.0)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1197.1.1)

    libb.dylib:
        libb.dylib (compatibility version 0.0.0, current version 0.0.0)
        liba.dylib (compatibility version 0.0.0, current version 0.0.0)
        /usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 120.0.0)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1197.1.1)

Link another library against these libraries::

    clang++ -o libc.dylib -dynamiclib c.o -L. -lb -la
    clang++ -o test-lib d.o -L. -lc
    export DYLD_PRINT_LIBRARIES=y
    ./test-lib
    unset DYLD_PRINT_LIBRARIES

This gives, among other output::

    dyld: loaded: /Users/mb312/dyldtest/./test-lib
    dyld: loaded: libc.dylib
    dyld: loaded: /usr/lib/libc++.1.dylib
    dyld: loaded: /usr/lib/libSystem.B.dylib
    dyld: loaded: libb.dylib
    dyld: loaded: liba.dylib
    dyld: loaded: /usr/lib/libc++abi.dylib

``otool -L`` on ``libc.dylib``::

    libc.dylib:
        libc.dylib (compatibility version 0.0.0, current version 0.0.0)
        libb.dylib (compatibility version 0.0.0, current version 0.0.0)
        liba.dylib (compatibility version 0.0.0, current version 0.0.0)
        /usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 120.0.0)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1197.1.1)

********************
The ``install_name``
********************

So -- the ``install_name`` is two things:

#. The name / location that a library *provides* to something that links against
   it. This is also the install name ``id`` (see man page for
   ``install_name_tool``).  The ``install_name`` ``id`` in a library you are
   linking to only matters at link time
#. The name that the linking application uses to say where it should find a
   library.  The ``install_name`` values stored in your linking application or
   library matter at run time - because they tell the application or library
   where to find the library.

***************************************************
Install names and static absolute or relative paths
***************************************************

So far we've used library paths that are relative paths - in fact they are
relative to the current directory from which we are executing our commands.

We can try moving our library::

    mkdir a
    mv liba.dylib a

Of course now our application fails::

    \$ ./test-lib
    dyld: Library not loaded: liba.dylib
    Referenced from: /Users/mb312/dyldtest/libc.dylib
    Reason: image not found
    Trace/BPT trap: 5

From the ``otool -L`` output above, we have to change the ``install_name`` in
``libb.dylib``, and ``libc.dylib``::

    install_name_tool -change liba.dylib a/liba.dylib libb.dylib
    install_name_tool -change liba.dylib a/liba.dylib libc.dylib

Then, sure enough, ``test-lib`` works again::

    \$ ./test-lib
    c()
    b()
    a()

Now move the other libraries to a new directory::

    mkdir libs
    mv libb.dylib libc.dylib libs

Obviously we first have to tell ``test-lib`` where ``libc.dylib`` went::

    install_name_tool -change libc.dylib libs/libc.dylib test-lib

But - oh dear - now ``libc.dylib`` is confused::

    \$ ./test-lib
    dyld: Library not loaded: libb.dylib
    Referenced from: /Users/mb312/dyldtest/libs/libc.dylib
    Reason: image not found
    Trace/BPT trap: 5

So we need to tell ``libc.dylib`` where ``libb.dylib`` is::

    install_name_tool -change libb.dylib libs/libb.dylib libs/libc.dylib

``test-lib`` then runs OK.

************
@loader_path
************

At the moment all our ``install_name`` values are relative to the current
directory. That's not satisfying because it means if we run our command from
anywhere but the current directory, the paths will be wrong.  ``@loader_path``
is one way to fix this.  Here we tell ``test-lib`` that it should look for
``libc.dylib`` in the ``lib`` directory relative to itself::

    install_name_tool -change libs/libc.dylib @loader_path/libs/libc.dylib test-lib

Note the use of ``@loader_path``.  This will be the directory containing the loading
application or library - in our case the directory containing ``test-lib``. We
can do the same trick to tell ``libc.dylib`` where to find ``libb.dylib``,
relative to itself::

    install_name_tool -change libs/libb.dylib @loader_path/libb.dylib libs/libc.dylib

Note ``@loader_path`` again.  See `_rpath etc`_ and `linking and install
names`_ for more explanation. In this case ``@load_path`` will be the path of
``libc.dylib`` - the library doing the loading of ``libb.dylib``.  Now all's
good::

    \$ ./test-lib
    c()
    b()
    a()

We wanted to make it possible to call our executable from any directory, so we
try that::

    mkdir nice-place
    cd nice-place
    ../test-lib

This gives::

    dyld: Library not loaded: a/liba.dylib
    Referenced from: /Users/mb312/dyldtest/libs/libc.dylib
    Reason: image not found
    Trace/BPT trap: 5

Why?  Because ``libc.dylib`` is still looking for ``liba.dylib`` at
``a/liba.dylib`` -- *starting at the current working directory*. How to fix?  Of
course::

    install_name_tool -change a/liba.dylib @loader_path/../a/liba.dylib \
        ../libs/libc.dylib
    install_name_tool -change a/liba.dylib @loader_path/../a/liba.dylib \
        ../libs/libb.dylib

******
@rpath
******

Another option is to use ``@rpath`` -- see `rpath etc`_::

    install_name_tool -change @loader_path/../a/liba.dylib @rpath/liba.dylib \
        ../libs/libc.dylib
    install_name_tool -change @loader_path/../a/liba.dylib @rpath/liba.dylib \
        ../libs/libb.dylib

This won't work yet because we haven't told anything what ``@rpath`` is::

    \$ ../test-lib
    dyld: Library not loaded: @rpath/liba.dylib
    Referenced from: /Users/mb312/dyldtest/libs/libc.dylib
    Reason: image not found
    Trace/BPT trap: 5

We can set ``@rpath`` in our executable::

    install_name_tool -add_rpath @loader_path/a ../test-lib

That works.  Or in the libraries doing the loading::

    # delete rpath we just set in executable
    install_name_tool -delete_rpath @loader_path/a ../test-lib
    # put into the library instead
    install_name_tool -add_rpath @loader_path/../a ../libs/libc.dylib

All good again.

One advantage of ``@rpath`` is that you can put several different search paths
into the the library or executable ``@rpath``.  For example, you could set the
``@rpath`` so that the library or executable looks for its libraries in a
relative path and also an absolute system path.

*********************************************
@loader_path and @rpath make code relocatable
*********************************************

Now notice this entire stack is relocatable (and has been since we started using
``@loader_path``::

    cd
    cp -r dyldtest dyldtest2
    ./dyldtest2/test-lib

All is still good.  You are ready for great things related to OSX run-time
loading.

.. _rpath etc: https://wincent.com/wiki/@executable_path,_@load_path_and_@rpath
.. _linking and install names:
   https://www.mikeash.com/pyblog/friday-qa-2009-11-06-linking-and-install-names.html
