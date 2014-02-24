############
Booting Macs
############

I've tried to install Linux on maybe 4 or 5 Mac machines.  It was very tiring
and difficult to get the machines to boot.  One problem that came back each time
was that I did not spend enough energy trying to understand the boot process.

This is a tutorial to remind myself of the stuff I did understand, and collect
links to useful information.

***************
Naming of parts
***************

Boot manager
    See rEFInd_ page for background.  A *boot manager* is a program that allows
    you to choose which of several programs to start when you boot the machine.
    Distinguish this from the *boot loader*.

Boot loader
    This is the software that, after booting, loads a program into memory that
    can start an operating system. GRUB_ is one example of software that
    provides both a *boot manager* and a *boot loader*.

EFI
    The extensible firmware interface.  First released as a specification by
    Intel, then revised by a group of vendors and released as UEFI.  EFI often
    in fact refers to UEFI. See `Intel EFI / UEFI`_.  EFI and UEFI replace the
    old BIOS_ firmware standard. EFI specs have versions beginning 1.x - for
    example, the last Intel-only EFI spec was 1.10 (2005).

UEFI
    Unified extensible firmware interface - see UEFI_.  Designed and released by
    the `Unified EFI forum`_. UEFI specs have release numbers of form 2.x.
    Release 2.1 was in January 2007, release 2.4 was in July 2013.  Apple has a
    representative on the unified EFI forum.

As for the rEFInd_ pages, I'll use EFI to refer to both of EFI and UEFI unless
there's some reason to distinguish the two, in which case I'll make that clear.

***********
EFI vs BIOS
***********

The EFI / UEFI system *replaces* the BIOS_ firmware standard.
Software that expects access the BIOS system calls will get upset and stop
working when trying to run on top of EFI and vice-versa.  This comes up for us
Mac owners because older operating systems such as Windows XP need a BIOS to
work against, and therefore there are some hoops to jump through getting XP to
boot on an EFI system like the Mac.

Like the BIOS system, the EFI system provides:

* Boot services: services that operate only when the system is booting
* Runtime services: services that the OS can use to query hardware and so on
  while the OS is running.

**********************************
EFI and GUID partition table disks
**********************************

The EFI specifications include the specifications for the `GUID Partition
table`_ format. The GPT format is a way of laying out the partition table on a
disk.  It is an alternative to the older `Master Boot Record`_ partition table
format.  Most EFI boot systems only read GPT partition tables, but some also
read MBR tables.  Some BIOS booting systems use GPT tables because of their
technical advantages.

****************************
The standard EFI / UEFI boot
****************************

#. There is a boot manager in firmware (*not* on disk)

   * firmware must also be able to read partition tables and FAT file systems.

#. The firmware boot manager reads an `EFI system partition`_ - a partition on
   disk with a particular `partition ID`_ code. It uses the FAT file system.
#. The boot manager can load *EFI executable programs* from the EFI system
   partition.  EFI executable programs are programs that can run with no
   operating system support, using only EFI firmware service calls. These
   programs are frequently boot loaders (see above) but can also be other useful
   programs like diagnostic utilities.
#. The choice of possible EFI executable programs can be explicit or implicit,
   controlled by a defined variable ``BootOrder`` stored in `Non-volatile RAM`_
   (NVRAM):

   * If the ``BootOrder`` variable is defined, the boot options are explicit.
     The ``BootOrder`` variable contains a list of further EFI NVRAM variables,
     each defining the EFI executable program to run and any parameters to pass
     to that program. Each EFI variable pointed to by ``BootOrder`` corresponds
     to a choice the user should see when the boot manager starts.  The boot
     manager then runs the chosen program with the given options.

   * If ``BootOrder`` is not defined, then the boot options are implicit, in
     that the boot manager should search all the disks on the system for a
     runnable EFI executable. The boot manager searches EFI system partitions on
     fixed disks, and assumes there is only one partition for removable disks.
     In either case, the boot manager looks for files with names of form:
     ``\EFI\BOOT\BOOT{machine type short-name}.EFI``, where ``{machine type
     short-name}`` matches the CPU architecture. The short name can be one of
     ``IA32`` (32-bit Intel), ``X64`` (64-bit), ``IA64`` (Itanium) ``ARM``,
     ``AA64`` (ARM 32 and 64 bit). For example ``\EFI\BOOT\BOOTX64.EFI`` matches
     the 64 bit standard Intel architecture.

**********
EFI on Mac
**********

The boot process on the Mac is highly non-standard for EFI (see
`efi-boot-process
<http://homepage.ntlworld.com/jonathan.deboynepollard/FGA/efi-boot-process.html>`_
and `rEFIt myths and facts <http://refit.sourceforge.net/myths>`_).

Specializations in Apple EFI
============================

Apple does not boot straight into a standard EFI boot sequence, but instead
loads its own non-standard boot manager.

The Apple EPI firmware understands HFS+ (the standard Apple disk format) as well
as the standard required FAT file format.

Apple can also enable BIOS-compatibility mode when booting.  BIOS compatibility
mode makes BIOS system calls available to the booting operating system to
emulate booting in a standard BIOS firmware setup.  The BIOS emulation comes
from a compatibility support module (CSM) - see `EFI and Ubuntu`_ and `Intel CSM
docs`_.

I can't see the conditions that enable BIOS emulation from the docs in front of
me.  The `bless manpage online`_ lists a flag ``--legacy`` that appears to
activate BIOS emulation in subsequent boot. Quoting from `EFI and Ubuntu`_:

    As far as I can tell, BIOS emulation mode only works when a hybrid MBR is present on the hard disk or when a BIOS-bootable optical disk is inserted in the optical drive. 

See `hybrid MBR`_ for more detail.  In brief, there is a hack to a GUID
partition table that can make the GPT also appear to be an MBR.  The Apple
"Bootcamp" utilities make this hybrid-MBR when making a partition to install
Windows XP, but you can also do this with Rod Smith's `GPT fdisk`_ (``gdisk``)

The boot process
================

#. On boot, an Apple boot manager starts.
#. The Apple boot manager uses the results of previous ``bless`` commands to
   select how to boot. The ``bless`` commands may have pointed to:

   * A file containing an ``.efi`` file to execute
   * A folder containing a file ``boot.efi`` file to execute
   * A partition from which to boot (in the ``efi-boot-device`` NVRAM variable)

   ``bless`` sets necessary NVRAM variables.  In certain modes, ``bless`` also
   writes the location of the boot efi file into the HFS+ volume header, so that
   the location of the boot file persists if the disk is moved to another
   machine or the NVRAM gets cleared (see ``man bless`` or the `bless manpage
   online`_).
#. Somehow the BIOS compatibility mode can get activated.  See above.

The EFI system partition on Mac
===============================

The Mac does indeed have an EFI partition, but it doesn't use it for booting. On
my laptop::

    \$ diskutil list

    /dev/disk0
    #:                       TYPE NAME                    SIZE       IDENTIFIER
    0:      GUID_partition_scheme                        *121.3 GB   disk0
    1:                        EFI EFI                     209.7 MB   disk0s1
    2:                  Apple_HFS Macintosh HD            120.5 GB   disk0s2
    3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3

We can mount the EFI partition, but it hasn't got any defined BOOTable EFI
programs.  (Please be careful, you can mess up your system by writing into the
EFI partition)::

    \$ diskutil mount /dev/disk0s1

    Volume EFI on /dev/disk0s1 mounted

    \$ ls /Volumes/EFI/EFI/

    APPLE

Unmount the file system to avoid accidental damage::

    \$ diskutil unmount /Volumes/EFI

    Volume EFI on disk0s1 unmounted

.. _GRUB: http://www.gnu.org/software/grub
.. _BIOS: http://en.wikipedia.org/wiki/BIOS
.. _UEFI: http://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface
.. _Intel EFI / UEFI: http://www.intel.com/content/www/us/en/architecture-and-technology/unified-extensible-firmware-interface/efi-homepage-general-technology.html
.. _EFI system partition: http://en.wikipedia.org/wiki/EFI_System_partition
.. _Booting: http://en.wikipedia.org/wiki/Booting
.. _rEFInd: http://www.rodsbooks.com/refind
.. _EFI boot loaders: http://www.rodsbooks.com/efi-bootloaders/index.html
.. _Unified EFI forum: http://en.wikipedia.org/wiki/Unified_EFI_Forum
.. _GUID partition table: http://en.wikipedia.org/wiki/GUID_Partition_Table
.. _Master Boot Record: http://en.wikipedia.org/wiki/Master_boot_record
.. _Non-volatile RAM: http://en.wikipedia.org/wiki/Non-volatile_random-access_memory
.. _UEFI 2.4 spec: http://www.uefi.org/specifications
.. _EFI and Ubuntu: http://www.rodsbooks.com/ubuntu-efi
.. _Intel CSM docs: http://www.intel.com/content/www/us/en/architecture-and-technology/unified-extensible-firmware-interface/efi-compatibility-support-module-specification-v097.html
.. _bless manpage online:
   https://developer.apple.com/library/mac/documentation/Darwin/Reference/Manpages/man8/bless.8.html
.. _hybrid MBR: http://www.rodsbooks.com/gdisk/hybrid.html
.. _GPT fdisk: http://www.rodsbooks.com/gdisk/index.html
.. _Partition ID: http://en.wikipedia.org/wiki/Partition_type
