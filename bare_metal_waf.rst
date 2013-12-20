##############
Bare metal WAF
##############

waf_ is a configure / build / install system.

It can do the jobs of ``autotools`` and ``make``, so instead of typing (say)::

    ./configure
    make
    make install

you can type (say)::

    ./waf configure
    ./waf build
    ./waf install

You don't need ``autotools`` or ``make`` installed.  The full ``waf`` binary is
90K and usually sits in your source code repository.

waf uses a Python configuration file so you can use Python code to define your
configure, build and install rules rather than the obscure ``make`` syntax and
funny variable names.

Among other projects, SAMBA uses waf for its entire configure / build / install system.

There is a comprehensive waf manual.

What's the downside?  The waf build system (like - say - ``make``) works at a
fairly high and abstract level, so it can be hard to understand the flow of
control.  It can sometimes be hard to find the part of waf that you want.

This page has notes to myself about how waf works.

********
Overview
********

The heart of the waf process is of course the build.

We're likely going to do this to build our project::

    ./waf configure
    ./waf build

We use the configure step to check for dependencies and set up any variables we
need to define for the build step.

The build step receives the result of the configure step, and sets up build
rules.  The build rules form a directed acyclic graph.  At the end of the build
step waf will execute the build steps using the dependency information from the
DAG to execute the build steps in an efficient order.

********
A taster
********

Let's say you have a project ``myproject``.  It's a directory called
``myproject``.  It has a single C file ``myprogram.c``.

Download the ``waf`` binary to the ``myproject`` from the waf_ site.

You invoke waf thus::

    cd myproject
    ./waf

and you'll get this::

    Waf: Run from a directory containing a file named 'wscript'

* the ``waf`` program loads a configuration file called ``wscript``

waf loads the wscript file, and executes the code inside in order to do stuff.

Let's pretend our project creates a file called ``foo`` and then copies it to
``bar``.  The wscript might look like this::

    # the whole wscript
    def configure(conf_ctx):
        # Check we have 'touch'
        conf_ctx.find_program('touch', VAR='TOUCH')
        # And 'cp'
        conf_ctx.find_program('cp', VAR='CP')

    def build(build_ctx):
        # Touch foo
        build_ctx(rule='${TOUCH} ${TGT}', target='foo')
        # Copy foo to bar
        build_ctx(rule='${CP} ${SRC} ${TGT}', source='foo', target='bar')

We run the checks with ``./waf configure``, and the build with ``./waf build``.

It isn't easy to see exactly how this works, and rest of this page will try to
do that.

************
waf commands
************

You execute a waf command with ``.waf command-name [options]``

You can define any command you like with something like this in the wscript
file::

    # the whole wscript file
    def mycommand(ctx):
        print('hello')

and::

    ./waf mycommand

giving::

    hello
    'mycommand' finished successfully (0.000s)

What happened?  waf loaded the wscript file, looked for a callable object called
``mycommand``, created a ``Context`` instance ``ctx``, and passed it to the
callable thing as the first and only argument.

The ``ctx`` instance contains information about the current waf run.
We investigate with a print in the wscript::

    # the whole wscript file
    def mycommand(ctx):
        print(ctx)

giving::

    <waflib.Context.Context object at 0x1011b60d0>
    'mycommand' finished successfully (0.000s)

Special commands
================

The following commands are special to waf:

* options
* configure
* distclean
* clean
* build
* install
* uninstall
* dist
* list
* step

(there may be others I don't know).

If you define functions (callables) with these names, they have default and
specialized behavior.  For example, each of these commands receives its own
specialized Context object. We can show that for the the ``options`` command.

::

    # the whole wscript
    def options(opt_ctx):
        print(opt_ctx)

gives::

    $ waf options
    <waflib.Options.OptionsContext object at 0x1011b53d0>

Let's make each of the commands print their context instance::

    # the whole wscript
    from __future__ import print_function

    for command_name in (
        'options',
        'configure',
        'distclean',
        'clean',
        'build',
        'install',
        'uninstall',
        'dist',
        'list',
        'step',
        ):
        exec('{0} = lambda ctx : print("In: {0} with", ctx)'.format(command_name))

Executing 'options' again::

    $ waf options
    In: options with <waflib.Options.OptionsContext object at 0x1011b55d0>

We can execute all these command in order by concatenating them at the command
line to show they each get an instance of their own specialized Context::

    $ waf options configure distclean clean build install uninstall dist list step
    In: options with <waflib.Options.OptionsContext object at 0x1011b6750>
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    In: configure with <waflib.Configure.ConfigurationContext object at 0x1011b6a50>
    'configure' finished successfully (0.017s)
    In: distclean with <waflib.Context.Context object at 0x1011b6c10>
    'distclean' finished successfully (0.000s)
    In: build with <waflib.Build.CleanContext object at 0x1011b6d50>
    'clean' finished successfully (0.008s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    In: build with <waflib.Build.BuildContext object at 0x1011b6f50>
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.002s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    In: build with <waflib.Build.InstallContext object at 0x1011c0210>
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'install' finished successfully (0.002s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    In: build with <waflib.Build.UninstallContext object at 0x1011c04d0>
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'uninstall' finished successfully (0.013s)
    In: dist with <waflib.Scripting.Dist object at 0x1011c07d0>
    New archive created: noname-1.0.tar.bz2 (sha='38a85b35879a5b0703142c3c27e765bafb7fd4b6')
    'dist' finished successfully (0.051s)
    In: build with <waflib.Build.ListContext object at 0x1011dcfd0>
    'list' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    In: build with <waflib.Build.StepContext object at 0x1011e9550>
    Add a pattern for the debug build, for example "waf step --files=main.c,app"
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'step' finished successfully (0.002s)

Some commands use the build callable instead of their own callable
==================================================================

You can see from the printout above that all of (clean, build, install,
uninstall, list, step) end up executing the 'build' command not their own
commands.  If you want to specialize behavior of these commands, you'll need to
put code in the ``build`` function (callable) to check the ``cmd`` attribute of
the build context to find which of these commands the ``build`` function is
running. See "More build commands" in the waf book for more detail.

More on the configure command
=============================

Executing the ``configure`` command will:

* call the options command
* set some default path information

This happens before your own ``configure`` command gets executed, and even if
there is no ``configure`` command defined.  For example, if wscript is an empty
file::

    $ waf configure
    <waflib.Options.OptionsContext object at 0x1011b53d0>
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    No function configure defined in /Users/mb312/dev_trees/myproject/wscript

The default configure machinery has set the default 'source' (*top*) directory
and the 'build' (*out*) directory.  *top* is the (by default) the directory
containing the wscript file, and *out* is (by default) a subdirectory of *top*
called ``build``.  You can customize these directories if you want, for example
by using the ``top`` and ``out`` global variables at the top of the wscript.

************************
How the build gets built
************************

See the waf book chapter called "Builds".

A build consists of tasks.  Tasks are instances of subclasses of the
``waflib.Task.Task`` class.  But - where is ``waflib``?

Where is the waf code?
======================

See "Local waflib folders" in the waf book.

The most way to use waf is to download the ``waf`` binary to your source code
tree, maybe checking the binary into your source control.

In this case, executing the ``./waf`` binary will automatically unpack the waf
code from within the binary to a specially named folder in the same directory as
the binary, with a name beginning with ``.waf-``. For example, after I have run
``./waf configure`` in the test project folder I get::

    $ ls -A1
    .lock-waf_darwin_build
    .waf-1.7.13-5a064c2686fe54de4e11018d22148cfc
    build
    waf
    wscript

The ``waflib`` code is in this special ``.waf-*`` directory:

    $ ls .waf-1.7.13-5a064c2686fe54de4e11018d22148cfc/
    waflib

As the waf book explains, it's also possible to run waf with ``waflib`` as a
standard folder in the source tree or elsewhere.

High level API for creating tasks
=================================

Usually we create tasks using a high-level API called *task generators*.  You
already saw these in first wscript towards the top of this page. The task
generator creates the task instances for us::

    # the whole wscript
    def configure(conf_ctx):
        pass

    def build(build_ctx):
        build_ctx(rule='touch ${TGT}', target='foo')

See :ref:`variable-substitution` below for more on the ``${TGT}`` string
substitution form.

The ``rule`` is a system command that we can run, and the ``target`` in this
case is a filename of a file we generate with the command.

From here on in, I'll use the invocation ``waf distclean configure build`` to
run the waf build.  ``distclean`` deletes all the generated build targets,
clearing the outputs of any previous waf run.

So::

    $ waf distclean configure build
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    [1/1] foo:  -> build/foo
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.024s)

The script generates an empty file ``build/foo``.

The call to ``build_ctx()`` above is a very short piece of code that ends up
creating an instance of ``waflib.TaskGen.task_gen``.  In due course this will
generate all the relevant ``Task`` instances.  Adpapting an example from the waf
book::

    # the whole wscript
    from __future__ import print_function

    def configure(conf_ctx):
        pass

    def build(build_ctx):
        tg = build_ctx(rule='touch ${TGT}', target='foo')
        # This will show that ``tg`` is a ``task_gen`` instance
        print('Type of tg is:', type(tg))
        # ``tg.tasks`` is empty because the generator has not run yet
        print('Task list before tg.post()', tg.tasks)
        # ``tg.post()`` runs the generator and fills the task list
        tg.post()
        # The task list now contains a single task
        print('Task list after tg.post()', tg.tasks)
        print('Type of tg.tasks[0] is:', type(tg.tasks[0]))

so::

    $ waf distclean configure build
    'distclean' finished successfully (0.002s)
    Setting top to                           : /Users/mb312/dev_trees/myproject 
    Setting out to                           : /Users/mb312/dev_trees/myproject/build 
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    Type of tg is: <class 'waflib.TaskGen.task_gen'>
    Task list before tg.post() []
    Task list after tg.post() [
        {task 4313537616: foo  -> foo}]
    Type of tg.tasks[0] is: <class 'waflib.Task.foo'>
    [1/1] foo:  -> build/foo
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.019s)

Nodes
=====

Before we do some low-level API examples, we need some explanation of the waf
concept of 'nodes'.

'nodes' are waf objects representing files or directories on the filesystem.
The files or directories may or may not exist at the time you create the node.

The waf book has a chapter devoted to "Node objects".

Two node objects get automatically created and attached to the 'Context' of
every command - 'path' and 'root'.  Here we use a custom command which receives
an instance of the base ``Context`` class.  All command contexts will have these
node objects::

    # the whole wscript
    from __future__ import print_function

    def mycommand(base_ctx):
        print(type(base_ctx.path), repr(base_ctx.path))
        print(type(base_ctx.root), repr(base_ctx.root))

giving::

    $ waf mycommand
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject
    <class 'waflib.Node.Nod3'> /
    'mycommand' finished successfully (0.000s)

``base_ctx.path`` is a node pointing to the directory containing the executed
wscript file. ``base_ctx.root`` is a node pointing to the root directory of the
filesystem containing the wscript.

Node objects contain various useful methods::

    # the whole wscript
    from __future__ import print_function

    def mycommand(base_ctx):
        # Show the attributes that are not private
        print([attr for attr in dir(base_ctx.path) if not attr.startswith('_')])

gives::

    $ waf mycommand
    ['abspath', 'ant_glob', 'ant_iter', 'bld_base', 'bld_dir', 'bldpath',
    'cache_abspath', 'cache_isdir', 'cache_sig', 'change_ext', 'children',
    'chmod', 'ctx', 'delete', 'evict', 'find_dir', 'find_node',
    'find_or_declare', 'find_resource', 'get_bld', 'get_bld_sig', 'get_src',
    'height', 'is_bld', 'is_child_of', 'is_src', 'listdir', 'make_node',
    'mkdir', 'name', 'nice_path', 'parent', 'path_from', 'read', 'relpath',
    'search', 'search_node', 'sig', 'srcpath', 'suffix', 'write']
    'mycommand' finished successfully (0.001s)

The waf book goes into more detail about these methods.

One interesting method is ``abspath()``.  It gives the absolute path to the
node as a string::

    # the whole wscript
    from __future__ import print_function

    def mycommand(base_ctx):
        print(base_ctx.path.abspath())

for output::

    $ waf mycommand
    /Users/mb312/dev_trees/myproject
    'mycommand' finished successfully (0.000s)

Creating nodes
==============

Here are some useful ordinary methods for creating nodes.  By 'ordinary' I mean
methods that work for all command contexts (base ``Context``, ``BuildContext``,
``OptionContext`` etc).

* ``.search(path)`` : search for an already-created node for ``path``
* ``.find_node(path)`` : create a node for ``path`` if it exists on the
  filesystem, return None otherwise
* ``.make_node(path)`` : create a node for ``path`` whether ``path``
  exists on the filesystem or not.
* ``.find_dir(dirname)``: create a node for ``dirname`` if it exists on the
  filesystem and is a directory, return None otherwise. This is just
  ``.find_node(path)`` with an extra check that ``path`` is in fact a
  directory.

waf creates some nodes automatically, but not many
==================================================

When waf creates ``path`` and ``root`` nodes, it also creates some nodes for
other parts of the system file tree, but not all. This is in order not to waste
time reading the file system for nodes that may not be needed.  Call this lazy
node creation.

Lazy node creation may come up in two situations.  The first is when using
``.search(path)`` (above).  This will only find nodes that are already
defined.  For example, if you do ``build_ctx.path.search('waf')`` at the
beginning of your build command, you will usually get None, even if the file
``waf`` does exist in the folder referred to by the ``path`` node.  You probably
want ``.find_node(path)`` instead, which will read the filesystem and create
a node if the file exists.

Another place where lazy node creation is relevant is interpreting the
``children`` attribute of a directory node. ``children`` is a dictionary giving
nodes corresponding to the contents of a directory. For efficiency, waf doesn't
alaways read the filesystem to fill this structure, so you may need to create
nodes manually if they have not been read from the filesystem already::

    # the whole wscript
    from __future__ import print_function

    import os

    def mycommand(base_ctx):
        # The children of the root directory
        print('root node children', base_ctx.root.children)
        # There are many more directories than found in the children
        print('ls of root directory', os.listdir('/'))

This gives::

    $ waf mycommand
    root node children {'Users': /Users}
    ls of root directory ['.dbfseventsd', '.DS_Store', '.file', '.fseventsd',
    '.hotfiles.btree', '.Spotlight-V100', '.Trashes', '.vol', 'Applications',
    'bin', 'cores', 'dev', 'Developer', 'etc', 'home', 'Library', 'mach_kernel',
    'net', 'Network', 'opt', 'private', 'sbin', 'System', 'tmp', 'User Guides
    And Information', 'Users', 'usr', 'var', 'Volumes']
    'mycommand' finished successfully (0.000s)


Specialized noding for builds
=============================

This describes node stuff that only applies to the ``BuildContext`` - the
context object passed to a ``build`` command.

build and source nodes
----------------------

The build context is a special context passed to the ``build`` command.

The build also needs to know about the location of the directory containing the
source files, and the output directory to put the target files. To solve this,
the build context contains two extra nodes, ``bldnode`` and ``srcnode``::

    # the whole wscript
    from __future__ import print_function

    def configure(conf_ctx):
        pass

    def build(build_ctx):
        print(type(build_ctx.path), repr(build_ctx.path))
        print(type(build_ctx.root), repr(build_ctx.root))
        print(type(build_ctx.srcnode), repr(build_ctx.srcnode))
        print(type(build_ctx.bldnode), repr(build_ctx.bldnode))

so::

    $ waf distclean configure build
    'distclean' finished successfully (0.003s)
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject
    <class 'waflib.Node.Nod3'> /
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject/build
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.005s)

The source node path may differ from the 'path' if you've customized the *top*
or *out* directories::

    # the whole wscript
    from __future__ import print_function

    top = 'tmp2'
    out = 'tmp2/build2'

    def configure(conf_ctx):
        pass

    def build(build_ctx):
        print(type(build_ctx.path), repr(build_ctx.path))
        print(type(build_ctx.root), repr(build_ctx.root))
        print(type(build_ctx.srcnode), repr(build_ctx.srcnode))
        print(type(build_ctx.bldnode), repr(build_ctx.bldnode))

We need to create the ``tmp2`` directory in the project directory in order for
this not to raise an error::

    mkdir tmp2

then::

    $ waf distclean configure build
    'distclean' finished successfully (0.002s)
    Setting top to                           : /Users/mb312/dev_trees/myproject/tmp2
    Setting out to                           : /Users/mb312/dev_trees/myproject/tmp2/build2
    Are you certain that you do not want to set top="." ?
    'configure' finished successfully (0.004s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/tmp2/build2'
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject
    <class 'waflib.Node.Nod3'> /
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject/tmp2
    <class 'waflib.Node.Nod3'> /Users/mb312/dev_trees/myproject/tmp2/build2
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/tmp2/build2'
    'build' finished successfully (0.025s)

Iff you have a build context ``bldnode``, you can get the source node with
``get_src``; if you have the build context ``srcnode`` you can get the build
node with ``get_bld``::

    # the whole wscript
    from __future__ import print_function

    top = 'tmp2'
    out = 'tmp2/build2'

    def configure(conf_ctx):
        pass

    def build(build_ctx):
        print(repr(build_ctx.srcnode.get_bld()))
        print(repr(build_ctx.bldnode.get_src()))

Output::

    $ waf distclean configure build
    'distclean' finished successfully (0.002s)
    Setting top to                           : /Users/mb312/dev_trees/myproject/tmp2 
    Setting out to                           : /Users/mb312/dev_trees/myproject/tmp2/build2 
    Are you certain that you do not want to set top="." ?
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/tmp2/build2'
    /Users/mb312/dev_trees/myproject/tmp2/build2
    /Users/mb312/dev_trees/myproject/tmp2
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/tmp2/build2'
    'build' finished successfully (0.005s)

Careful with these methods - if you call them on nodes other than ``bldnode`` or
``srcnode``, you may well not get what you expect.

Where's my node - build or source?
----------------------------------

During the build, we may want to create nodes that might refer to the source
tree or to the build tree.  For example you could imagine a command
``my_find_node_build_source(path)`` which would look for ``path`` in the
source tree, then in the build tree.  There are a couple of node methods that
look both in the source tree and the build tree.  These both only work for build
contexts:

* ``.find_resource(path)``: first look for an existing node in the build node
  tree, return if found.  Then look for ``path`` in the source filesystem,
  create a node and return if found.  Otherwise return None.
* ``.find_or_declare(path)``:

  1. look for an existing node in the build node tree. Return that node if it
     exists.
  2. look for corresponding path in the source filesystem, make a node for the
     path and return it if the path exists.
  3. Make a new node in the build node tree for this path and return that node.

  In each case, if the file corresponding to the node does not already exist,
  create the path to that file if the path does not yet exist on the filesystem.

Low-level API for tasks
=======================

As we saw above, the high-level API generates 'task' instances.

The low-level API creates task instances directly.

See the "Direct task declaration" in the waf book for details.

Here's an example of the high level interface.  Then we'll do the same with the
low-level interface::

    # the whole wscript
    def configure(conf_ctx):
        pass

    def build(build_ctx):
        # create empty 'foo' file
        build_ctx(rule='touch ${TGT}', target='foo')
        # copy 'foo' to 'bar'
        build_ctx(rule='cp ${SRC} ${TGT}', source='foo', target='bar')

Thence::

    $ waf distclean configure build
    'distclean' finished successfully (0.002s)
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    [1/2] foo:  -> build/foo
    [2/2] bar: build/foo -> build/bar
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.035s)

The low level interface defines the tasks and dependencies directly::

    # the whole wscript
    from waflib.Task import Task

    def configure(conf_ctx):
        pass

    def build(build_ctx):
        # Declare the tasks
        class TouchFile(Task):
            def run(self):
                ret_code = self.exec_command(
                    'touch {0}'.format(self.outputs[0].abspath()))
                return ret_code

        class CopyFile(Task):
            def run(self):
                ret_code = self.exec_command(
                    'cp {0} {1}'.format(self.inputs[0].abspath(),
                                        self.outputs[0].abspath()))
                return ret_code
        # Instantiate tasks
        touch_task = TouchFile(env=build_ctx.env)
        touch_task.set_outputs(build_ctx.path.find_or_declare('foo'))
        cp_task = CopyFile(env=build_ctx.env)
        cp_task.set_inputs(build_ctx.path.find_resource('foo'))
        cp_task.set_outputs(build_ctx.path.find_or_declare('bar'))
        # Add them to a run group to schedule them
        build_ctx.add_to_group(touch_task)
        build_ctx.add_to_group(cp_task)
        # Build machinery will submit and run these defined tasks

giving output::

    $ waf distclean configure build
    'distclean' finished successfully (0.002s)
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    [1/2] TouchFile:  -> build/foo
    [2/2] CopyFile: build/foo -> build/bar
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.040s)

We can also define tasks using the slightly higher-level ``run_str`` attribute
instead of the ``run`` method.  waf translates the ``run_str`` attribute to a
``run`` method automatically on execution, to give the same result::

    # the whole wscript
    from waflib.Task import Task

    def configure(conf_ctx):
        pass

    def build(build_ctx):
        # Declare the tasks
        class TouchFile(Task):
            run_str = 'touch ${TGT}'

        class CopyFile(Task):
            run_str = 'cp ${SRC} ${TGT}'

        # Instantiate tasks
        touch_task = TouchFile(env=build_ctx.env)
        touch_task.set_outputs(build_ctx.path.find_or_declare('foo'))
        cp_task = CopyFile(env=build_ctx.env)
        cp_task.set_inputs(build_ctx.path.find_resource('foo'))
        cp_task.set_outputs(build_ctx.path.find_or_declare('bar'))
        # Add them to a run group to schedule them
        build_ctx.add_to_group(touch_task)
        build_ctx.add_to_group(cp_task)
        # Build machinery will submit and run these defined tasks

.. _variable-substitution:

*****************************
run_str Variable substitution
*****************************

As we've seen, a Task can define a system command by defining a ``run`` method,
or a ``run_str``, which will be compiled into a ``run`` method.

If you pass a string using the ``rule=`` keyword argument to the high-level API,
this also becomes the ``run_str`` of the task.

As you can see from the examples above, the run_str has some extra rules of
variable substitution.

For example, ``${SRC}`` and ``${TGT}`` get substituted for the ``source`` and
``target`` filenames.  Other variable names that work in this mode
(``${VARIABLE_NAME}``) are any attribute of ``build_ctx.env``.

See *Scriptlet expressions* in the waf book for more substitutions. Here I've
copied from the book::

    1. If the value starts by env, gen, bld or tsk, a method call will be made
    2. If the value starts by SRC[n] or TGT[n], a method call to the
       input/output node n will be made
    3. SRC represents the list of task inputs seen from the root of the build directory
    4. TGT represents the list of task outputs seen from the root of the build directory

For example::

    # whole wscript
    def configure(conf_ctx):
        conf_ctx.env.MYVAR = 'my variable'

    def build(build_ctx):
        build_ctx(rule='echo ${MYVAR}', always=True)
        build_ctx(rule='echo ${bld.bldnode.abspath()}', always=True)
        build_ctx(rule='echo ${bld.srcnode.abspath()}', always=True)

gives::

    $ waf configure build
    Setting top to                           : /Users/mb312/dev_trees/myproject
    Setting out to                           : /Users/mb312/dev_trees/myproject/build
    'configure' finished successfully (0.003s)
    Waf: Entering directory `/Users/mb312/dev_trees/myproject/build'
    [2/3] echo ${MYVAR}:
    [2/3] echo ${bld.bldnode.abspath()}:
    my variable
    [3/3] echo ${bld.srcnode.abspath()}:
    /Users/mb312/dev_trees/myproject/build
    /Users/mb312/dev_trees/myproject
    Waf: Leaving directory `/Users/mb312/dev_trees/myproject/build'
    'build' finished successfully (0.030s)

************************
IPython debugging in waf
************************

As of the IPython development tree of Christmas 2013, this works to drop you
into the IPython shell from waf::

    # the whole wscript
    def configure(conf_ctx):
        pass

    def build(build_ctx):
        from IPython import embed
        from IPython.core.interactiveshell import DummyMod
        wscript_module = DummyMod()
        wscript_module.__dict__ = locals()
        wscript_module.__name__ = 'wscript'
        embed(user_module=wscript_module)

.. _waf: http://code.google.com/waf
