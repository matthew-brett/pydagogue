##########################
OSX legacy packaging redux
##########################

This is a summary of the information on older (buundle-type) OSX installers in
the `software delivery legacy guide`_.

This redux might help reading the original document, because I found the
original hard to digest.

***************************************************
Packaging has changed from bundles to flat packages
***************************************************

The world the legacy guide describes is for standard packaging up to and
including OSX 10.4.

In this world, all installation packages were *bundles*.  To quote from the
glossary of the legacy guide:

    bundle
        A structured directory hierarchy that stores files in a way that
        facilitates their retrieval.

This means all installation package types before OSX 10.5 are directories with
a particular structure.  These are the package types described in the legacy
guide, and this document.  Newer OSX will still install from these packages.

In the new world (OSX 10.5 and above), the standard package formats are
*flat*, meaning that the packages are archived up into single file ``xar``
archives.  There are two types of packages in this new world of flat:

* flat *component packages* (built by ``pkgbuild`` utility) (see `flat package
  format`_, `unpacking flat packages`_ and the ``pkgbuild`` man page).
* flat *product archives* (built by the ``productbuild`` utility) (see the
  ``productbuild`` man page).  These contain component packages, but can
  customize the install experience with a XML  `Distribution definition file`_
  called ``Distribution``. The ``Distribution`` file may contain javascript
  code for checking installation requirements and customizing install options.

See :doc:`flat_packages` for details.

Now we forget about flat packages and go back to the world where all installer
packages are bundles.

***************************
Manual and managed installs
***************************

The software delivery guide distinguishes between:

Manual installs
  You provide a single directory or file that the user drags to their hard
  disk.  This is a typical install for an OSX ``*.app`` bundle, where the user
  drags the ``*.app`` folder (bundle) to ``/Applications``

Managed installs
  Installs via a ``.pkg`` or ``.mpkg`` installer.  The install is "managed"
  because the installer automates the task of checking for dependencies,
  getting Administrator authentication from the user, and moving files to
  different parts of the file system.

The rest of this document is about *managed installs*.

**************************************
Component and multi-component packages
**************************************

There are two categories of installers, *single component* installers and
*multi-component* installers.  A single component installer can only have one
component, but the multi-component installers can contain more than one
component.

I will use *installer* and *package* to mean the same thing in this document.
Both single and multi-component packages can be used as installers.

There is only one type of single-component installer -- the *component
package*.

There are two types of multi-component installers; *metapackages* and
*distribution packages* (see below).

Therefore there are three types of installers / packages:

* component package (single component)
* metapackage (multi-component, older format)
* distribution package (multi-component, newer format)

Component package
=================

The Apple term for a package / installer for a single component is a
*component package*.  Component packages can be used as installers, or as
units for building multi-component packages.

A component package carries information and data for installing one particular
component. A component package:

* has a ``.pkg`` directory extension for the package bundle;
* installs on any version of OSX;
* usually contains a *payload* - directories and files to be installed at one
  particular location on disk;
* has a bundle structure where the  ``.pkg`` directory contains a top-level
  ``Contents`` directory, which in turn contains files ``Archive.bom``,
  ``Archive.pax.gz``, ``Info.plist``, ``PkgInfo``, and directory
  ``Resources``.

This is one ``.pkg`` compoenent bundle from the Python.org installer:

.. _python-unix-tools-image:

.. image:: images/python_unix_tools.png

Multi-component packages
========================

There are two types of multi-component packages, the *metapackage* and the
(newer) *distribution package*.

Metapackage
-----------

A metapackage:

* has a ``.mpkg`` directory extension for the package bundle;
* installs on OSX 10.2 or later;
* has a bundle structure where the ``.mpkg`` directory contains a top-level
  ``Contents`` directory, which in turn contains files ``Info.plist``,
  ``PkgInfo``, and directories ``Resources``, ``Packages``.

Here's is the ``.mpkg`` bundle for the Python.org installer:

.. image:: images/python_mpkg.png

Each of the listed ``.pkg`` component packages is also a bundle.  In fact the
:ref:`example component bundle contents <python-unix-tools-image>` is the
contents of ``PythonUnixTools-2.7.pkg`` from the Python.org ``.mpkg`` bundle
here.

Distribution package
--------------------

A distribution package:

* has a ``.mpkg`` directory extension for the package bundle;
* installs on OSX 10.4 or later;
* can customize install messages and options using XML elements and javascript
  code in the ``distribution.dist`` file.
* has a bundle structure where the ``.mpkg`` directory contains a top-level
  ``Contents`` directory, which in turn contains file ``description.dist``,
  and directories ``Resources``, ``Packages``.

This is the contents of a distribution package I had lying around on my hard
drive:

.. image:: images/nosleep_mpkg.png

.. _hybrid-package:

Hybrid package
--------------

Confusingly, it is also possible to make a package that is *both* a
metapackage *and* a distribution package.  These packages have the contents of
a metapackage, but with the extra ``distribution.dist`` file.  The installer
runs as a metapackage on OSX < 10.4, and as a distribution package for OSX >=
10.4.  For example, this is why the metapackage and distribution package
directory listings shown in the `MacTech flat package article`_ have the same
files.

********************************
Information in all package types
********************************

Apple distinguishes four types of information any package can contain:

* Product information : e.g. description, readme, license
* Package information : e.g. package identifier, package version
* Installation properties : e.g. system requirements, whether the installer
  requires Administrator permissions
* Install operations : one of pre-flight, pre-install, pre-upgrade,
  post-install, post-upgrade, post-flight (see :ref:`install-operations`).

.. _install-steps:

*******************
Steps in an install
*******************

* Requirements check : the installer checks if the system and target
  installation volumes meet any requirements for the install
* Preinstall : installer runs pre-flight and pre-install / pre-upgrade
  operations; these may cancel the install.
* Install / payload drop: installer copies payload(s) to target volume
* Save receipt : "Installer copies the component package file (with its
  payload stripped) to the ``/Library/Receipts`` directory in the installation
  volume." (`software delivery legacy guide`_).
* Postinstall : installer runs post-install / post-upgrade and post-flight
  operations.

.. _install-operations:

******************
Install operations
******************

Install operations are operations run during the *steps* of an install, that
can customize the behavior of the installer.

I'll also call these *pre / post operations*.

The operations are run in the following order (see :ref:`install-steps`).

* Pre-flight : operation run after requirements check step.  Implemented by
  `preflight` executable. Return value other than 0 cancels the install.
* Pre-install : operation run for a system on which there is no pre-existing
  receipt (see "Save receipt" step above). Implemented by `preinstall`
  executable.  Return value other than 0 cancels the install.
* Pre-upgrade : operation run for a system on which there is a pre-existing
  receipt. Implemented by `preupgrade` executable. Return value other than 0
  cancels the install.

There follows the *install / payload drop* step (above), then:

* Post-install : operation run for a system on which there is a pre-existing
  receipt. Implemented by `postinstall` executable.
* Post-upgrade : operation run after payload drop, for a system on which there
  is no pre-existing receipt. Implemented by `postupgrade` executable script.
* Post-flight : Implemented by `postflight` executable.

All these operations are optional.

The executables can be scripts or binaries, but must have their executable bit
set.

See "Specifying install operations" in the `software delivery legacy guide`_.

*******************************************
How the package types implement the install
*******************************************

Component packages, metapackages and distribution packages differ in their
behaior when isntalling. They differ in the way they implement requirement
checks and which operation executables they run.

Component package
=================

Requirements check
------------------

A component package can have none or more of the following executables:

* ``InstallationCheck``
* ``VolumeCheck``

These scripts implement requirement checking for the "requirements check" step
(:ref:`install-steps`).

If ``InstallationCheck`` is present, it should return 0 if the system is
suitable for the install. If not, it should return another number, where the
number identifies a message to display (see the `software delivery legacy
guide`_ for details).

If ``VolumeCheck`` is present, it should return 0 for any volume that is
suitable for the install.  If a particular volume is not suitable, it should
return another number, where the number identifies a message to display (see
the `software delivery legacy guide`_ for details).  The installer will run
``VolumeCheck`` on each available volume at install-time.

An install using a component package also runs these (optional) operations /
executables:

pre / post operations
---------------------

* ``preflight``
* ``preinstall`` or ``preupgrade`` (depending on whether a receipt is present)
* ``postinstall`` or ``postupgrade`` (depending on whether a receipt is present)
* ``postflight``

Metapackage
===========

A metapackage can contain:

* component packages
* metapackages

I will call the containing metapackage the "top metapackage".

Requirements check
------------------

* ``InstallationCheck`` for each component package.
* ``VolumeCheck`` for each component package and each available volume.

The metapackage cannot implement its own installation or volume requirement
checking, and only uses the checks of the component packages.

Pre-post operations
-------------------

* ``preflight`` for top metapackage
* ``preflight`` for each component package
* ``preinstall`` or ``preupgrade`` for top metapackage
* ``preinstall`` or ``preupgrade`` for each component package
* ``postinstall`` or ``postupgrade`` for each component package
* ``postinstall`` or ``postupgrade`` for top metapackage
* ``postflight`` for top metapackage
* ``postflight`` for each component package

Distribution package
====================

Distribution packages can only contain component packages, not metapackages or
other distribution packages.

Requirements check
------------------

Distribution packages implement their requirement checks with javascript code
embedded in an XML file called ``distribution.dist``.  This file can contain
javascript code for checking whether the system is suitable for the install
(the *Installation Check script*) and code for checking whether a volume is
suitable for install (the *Volume Check script*).  The requirements check
process is therefore:

* Run Installation Check javascript.
* Run Volume Check javascript on every volume.

Pre-post operations
-------------------

* ``preflight`` for each component package
* ``preinstall`` or ``preupgrade`` for each component package
* ``postinstall`` or ``postupgrade`` for each component package
* ``postflight`` for each component package

Unlike the metapackage, the distribution package cannot itself specify
pre-post operations with scripts (they will be ignored if present).

.. include:: links_names.inc
