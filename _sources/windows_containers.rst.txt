###########################
Notes on Windows containers
###########################

See: `Windows containers overview
<https://msdn.microsoft.com/en-us/virtualization/windowscontainers/about/about_overview>`_.

There are two types of Windows containers:

* Windows Server containers - uses host kernel, similar to Linux docker
  container.  These containers can only run on a host with matching kernel.
* `Hyper-V containers
  <https://msdn.microsoft.com/en-us/virtualization/windowscontainers/management/hyperv_container>`_
  - has own kernel, more like an optimized virtual machine.

Windows containers use Windows API calls, so a Windows host can only support
Windows containers.

One way of using these containers is via a Windows implementation of Docker.

See this `blog post
<https://azure.microsoft.com/en-us/blog/containers-docker-windows-and-trends/>`_
for more detailed background on Windows containers.

***************************
Set up for using containers
***************************

To use either type of container on Windows, you will need container host
support in your OS.  This `started with Windows 2016 technical preview 3
<http://weblogs.asp.net/scottgu/announcing-windows-server-2016-containers-preview>`_.
You will need:

* A real or virtual machine with an OS that can support containers, and
* Container support installed on the OS;

See `installing a container host
<https://msdn.microsoft.com/en-us/virtualization/windowscontainers/quick_start/container_setup>`_
for instructions on setting up a virtual machine with container support, and
`inplace setup
<https://msdn.microsoft.com/en-us/virtualization/windowscontainers/quick_start/inplace_setup>`_
for instructions on installing the container host services into a real or
virtual machine running Windows server 2016 tech preview.

I followed the `inplace setup`_ instructions on a real machine running server
2016.

.. _container-images:

****************
Container images
****************

Containers run from OS "images".  If the container corresponds to a running operating
system, then the image corresponds to the hard disk of the OS.  See `Windows
container images
<https://msdn.microsoft.com/virtualization/windowscontainers/management/manage_images>`_
for instructions on downloading images for use in Windows containers.

************************
Using Windows containers
************************

There are two standard ways to use Windows containers:

* using `powershell
  <https://msdn.microsoft.com/en-us/virtualization/windowscontainers/deployment/docker_windows>`_.
  See also `managing containers
  <https://msdn.microsoft.com/en-us/virtualization/windowscontainers/management/manage_containers>`_;
* using Docker.

************************************
Using Windows containers with Docker
************************************

Docker gives a nice interface to starting and using Windows containers.

Installing the container host features does not install docker, so, to use
Docker, you will need to `install Docker
<https://msdn.microsoft.com/en-us/virtualization/windowscontainers/deployment/docker_windows>`_.

Then see:

* `Docker containers
  <https://msdn.microsoft.com/en-us/virtualization/windowscontainers/quick_start/manage_docker>`_.
* `managing containers`_.

In what follows I'm running in a powershell with admin privileges.

To see a list of images that you have installed::

    docker images

On my system, after installing the :ref:`container-images`, I had::

    PS C:\WINDOWS\system32> docker images
    REPOSITORY              TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    windowsservercore       10.0.10586.0        6801d964fda5        5 months ago        0 B
    nanoserver              10.0.10586.0        8572198a60f1        5 months ago        0 B

``windowsservercore`` is an image containing a minimal Windows Server core
instance.  ``nanoserver`` contains a `nanoserver
<https://technet.microsoft.com/en-us/library/mt126167.aspx>`_ instance.

For convenience, you might like to tag the ``windowsservercore`` and
``nanoserver`` images as being the ``latest``.  ``latest`` is the default tag
that docker uses when selecting a version of the image, so when you ask for
``windowsservercore``, it implies (image name:tag)
``windowsservercore:latest``.  If you don't add these tags, you will need to
give the tag explicitly, as in ``windowservercore:10.0.10586.0``.  Add the
``latest`` tags with::

    docker tag windowsservercore:10.0.10586.0 windowsservercore:latest
    docker tag nanoserver:10.0.10586.0 nanoserver:latest

You might then get something like this::

    PS C:\WINDOWS\system32> docker images
    REPOSITORY              TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    windowsservercore       10.0.10586.0        6801d964fda5        5 months ago        0 B
    windowsservercore       latest              6801d964fda5        5 months ago        0 B
    nanoserver              10.0.10586.0        8572198a60f1        5 months ago        0 B
    nanoserver              latest              8572198a60f1        5 months ago        0 B

To play with a Docker container, you might do something like this::

    docker run -ti --rm windowsservercore powershell

This will open a new powershell session inside the container.  Exit the
session to exit the container.

Notice that, if we had not done the ``docker tag`` commands above, we would
have to give the tag in the docker command, as in ``docker run -ti --rm
windowsservercore:10.0.10586.0 powershell``.

If you are on Windows server, and you want to use the nanoserver images, you
will need to force docker to use these via Hyper-V containers.  This is
because nanoserver and Windows server 2016 do not have the same kernel, and
Windows server containers need to share a kernel with the host.

To force the creation of Hyper-V containers instead of Windows server
containers, use the ``--isolation=hyperv`` flag to Docker, as in::

    docker run -ti --rm --isolation=hyperv nanoserver cmd

See `Docker containers`_ for more detail.

**************************************
Example of installing into a container
**************************************

Here I am installing three versions of Python and the MSVC command line tools
for Python 2.7 into a container::

    docker run -ti --rm -v c:\Users\mb312\Downloads:c:\downloads windowsservercore powershell

Then (in the container)::

    cd c:/downloads
    .\build_container.ps1

Where ``build_container.ps1`` is::

    # Set environment variable for correct code page on Python 2
    # http://stackoverflow.com/questions/35176270/python-2-7-lookuperror-unknown-encoding-cp65001#35177906
    [Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "UTF-8", "Machine")
    $env:PYTHONIOENCODING="UTF-8"
    cd c:/downloads
    # See:
    # https://www.python.org/download/releases/2.5/msi/
    # https://msdn.microsoft.com/en-us/library/windows/desktop/aa367988(v=vs.85).aspx
    cmd /c msiexec /qn /i VCForPython27.msi ALLUSERS=1
    cmd /c msiexec /qn /i python-2.7.11.amd64.msi TARGETDIR=c:\Python27-x64
    cmd /c msiexec /qn /i python-2.7.11.msi
    cmd /c msiexec /qn /i python-3.4.4.amd64.msi TARGETDIR=c:\Python34-x64
    cmd /c msiexec /qn /i python-3.4.4.msi TARGETDIR=c:\Python34
    # See:
    # https://docs.python.org/3.5/using/windows.html#installing-without-ui
    cmd /c python-3.5.1-amd64.exe /quiet InstallAllUsers=1 TargetDir=c:\Python35-x64
    cmd /c python-3.5.1.exe /quiet InstallAllUsers=1 TargetDir=c:\Python35
