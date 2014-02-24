############
Booting Macs
############

I've tried to install Linux on maybe 4 or 5 Mac machines.  It was very tiring
and difficult to get the machines to boot.  One problem that came back each time
was that I did spend enough energy trying to understand the boot process.

This is a tutorial to remind myself of the stuff I did understand, and collect
links to stuff that was useful for explanation.

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
    old BIOS_ firmware standard.

UEFI
    Unified extensible firmware interface - see UEFI_.  Designed and released by
    the `Unified EFI forum`_.  Release 2.1 was in January 2007, release 2.4 was in
    July 2013.  Apple has a representative on the unified EFI forum.

As for the rEFInd_ pages, I'll use EFI to mean UEFI unless there's some reason
to distinguish the two, in which case I'll make that clear.

******************
UEFI / EFI vs BIOS
******************

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

*******************
The EFI / UEFI boot
*******************

1. There is a boot manager in firmware (*not* on disk)
    * firmware must also be able to read partition tables and FAT file systems.
1. The firmware boot manager reads an `EFI system partition`_ - a partition on
   disk with a particular partition code. It uses the FAT file system.
1. The boot manager can load *EFI executable programs* from the EFI system
   partition.  EFI executable programs are programs that can run with no
   operating system support, using only EFI firmware service calls. These
   programs are frequently boot loaders (see above) but can also be other useful
   programs like diagnostic utilities.




.. _BIOS: http://en.wikipedia.org/wiki/BIOS
.. _UEFI: http://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface
.. _Intel EFI / UEFI: http://www.intel.com/content/www/us/en/architecture-and-technology/unified-extensible-firmware-interface/efi-homepage-general-technology.html
.. _EFI system partition: http://en.wikipedia.org/wiki/EFI_System_partition
.. _Booting: http://en.wikipedia.org/wiki/Booting
.. _rEFInd: http://www.rodsbooks.com/refind
.. _EFI boot loaders: http://www.rodsbooks.com/efi-bootloaders/index.html
.. _Unified EFI forum: http://en.wikipedia.org/wiki/Unified_EFI_Forum
