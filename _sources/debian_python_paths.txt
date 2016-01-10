######################################
Debian and Ubuntu Python package paths
######################################

Debian and Ubuntu have some special rules for where Python packages go.  See
: https://wiki.debian.org/Python

The main point of interest to us, is that Python packages that you install for
the Debian / Ubuntu packaged Python go into different directories than would
be the case for a non-Debian Python installation.

A non-Debian Python installation, such as Python compiled from source, will
install Python packages into ``/usr/local/lib/pythonX.Y/site-packages`` by
default, where X.Y is your Python version (such as ``2.7``).

For Debian Python, package files go into different directories depending on
whether you installed the package from standard Debian packages, or using
Python's own packaging mechanisms, such as ``pip``, ``easy_install`` or
``python setup.py install``.

Debian Python packages installed via ``apt`` or ``dpkg`` go into a folder
``/usr/lib/pythonX.Y/dist-packages``.  You can see where files would go for
any Debian / Ubuntu package with ``apt-file list <package-name>``

``pip``, ``easy_install`` or ``python setup.py install`` installs go into a
folder ``/usr/local/lib/pythonX.Y/dist-packages``.

.. include:: links_names.inc
