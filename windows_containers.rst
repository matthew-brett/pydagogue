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

* A real or virtual machine with an OS that can support containers;
* Container support installed on the OS;

See `installing a container host
<https://msdn.microsoft.com/en-us/virtualization/windowscontainers/quick_start/container_setup>`_
for instructions on setting up a virtual machine with container support, and
`inplace setup
<https://msdn.microsoft.com/en-us/virtualization/windowscontainers/quick_start/inplace_setup>`_
for instructions on installing the container host services into Windows server
2016 tech preview.

I followed the `inplace setup`_ instructions on a real machine running server
2016.

****************
Container images
****************

Containers run inside OS "images". See `Windows container images
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

***********************************e
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

To play with a Docker container, you might do something like this, in a
powershell session with admin privileges:

    docker images  # review available images
    docker run -ti --rm windowsservercore powershell

This will open a new powershell session inside the container.  Exit the
session to exit the container.

If you are on Windows server, and you want to use the nano server images with
Docker, you will need to force docker to use these via Hyper-V containers.
This is because nano server and Windows server 2016 do not have the same
kernel, and Windows server containers need to share a kernel with the host.

To force the creation of Hyper-V containers instead of Windows server
containers, use the ``--isolation=hyperv`` flag to Docker, as in::

    docker run -ti --rm --isolation=hyperv nanoserver cmd

See `Docker containers`_ for more detail.
