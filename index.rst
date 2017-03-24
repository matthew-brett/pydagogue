.. pydagogue documentation master file, created by
   sphinx-quickstart on Mon Sep  7 21:34:05 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pydagogue
====================

Pydagogue is a collection of tutorials that came to me while working on python
things like nipy_.

Some pages that started here, have moved to their own sites:

* `the curious coder's guide to git <curious git_>`_ - understanding git from
  ideas to practice;
* `pages about developing on macOS <docosx_>`_;


Contents:

.. toctree::
    :maxdepth: 2

    python
    git
    computing

.. the hidden toctree is to avoid warnings during the build.  The
   gh-pages-intro should probably be retired, `ghp-import` is easier.

.. toctree::
    :hidden:

    README
    booting_macs
    develop_mac
    gh-pages-intro
    legacy_package_redux
    mac_runtime_link

.. include:: links_names.inc
