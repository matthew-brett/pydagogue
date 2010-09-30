.. _introducing-unicode:

Introducing Unicode
===================

A collection of links and some very basic introduction.

For some information on Unicode in Python, see :ref:`python-unicode`.

For a good programmer's introduction see:
http://www.joelonsoftware.com/articles/Unicode.html

Unicode
-------

Unicode is a convention that defines a unique number for a very very
large number of possible characters in almost all known alphabets:

* http://www.unicode.org/standard/WhatIsUnicode.html.
* http://en.wikipedia.org/wiki/Unicode

The number assigned to each character is referred to as the **code
point**.  The `Unicode consortium <http://www.unicode.org/>`_ has the
job of defining which code point corresponds to which character.  The
correspondence of code points to characters is published in the Unicode
Character Database - the latest version of which should be at
http://www.unicode.org/Public/UNIDATA/.  To refer to a code point it is
conventional to use octal - for example code point U+00E9 is the latin
small letter e with an acute accent.

The code points up to 128 (octal 7F) are identical to the ascii
character codes; so for example ``U+0065`` is the latin letter e.

Code points from 0 to 65535 (octal FFFF) represent characters in the
Basic Multilingual Plane (BMP).  The BMP contains characters for almost
all modern languages, including Chinese, as well as a large number of
symbols.  Codes outside the BMP (octal 10000 and above) include some
modern Chinese characters, various historical scripts and characters,
and musical and mathematical symbols - see
http://en.wikipedia.org/wiki/Mapping_of_Unicode_characters.

Encoding
--------

When these code points are represented on disk or in memory as a string,
the string has an **encoding** - which specifies the relationship
between the bytes in the string and the eventual resulting unicode code
points.

Fixed width encoding
~~~~~~~~~~~~~~~~~~~~

Fixed width encodings are encodings with one value (16 or 32 bit) per
unicode character.

At the moment, the number range of the defined Unicode code points can
be contained in the range of a 32 bit unsigned integer.  The simplest
possible encoding for a string is therefore just to contain one 32 bit
value for each character, where each 32 bit value is the code point for
the character.  This encoding is referred to as Universal Character Set
4 (UCS-4) or Unicode Transformation Format 32 (UTF-32):
http://en.wikipedia.org/wiki/UTF-32/UCS-4

Unicode characters above octal FFFF (and outside the BMP) are very rare,
and so another simple way of representing almost all common unicode
strings is to have one 16 bit value per character; this is UCS-2.
Because it cannot encode all unicode strings, UCS-2 has become
increasingly uncommon: http://en.wikipedia.org/wiki/UTF-16/UCS-2

Variable width encoding
~~~~~~~~~~~~~~~~~~~~~~~

Variable width encoding represents individual characters with different
numbers of bytes. Thus a string representing a single code point with a
variable width encoding could be 1 to 4 bytes long, depending on the
code point it contained.

A common encoding for unicode is UTF-8; this is standard with most Linux
distributions and many multilingual web pages:
http://en.wikipedia.org/wiki/UTF-8.  A single unicode code point can be
represented by up to four bytes.  Code points in the ascii range (0 to
7F) only need one byte, so this format is very space efficient for most
western text.

UTF-16 uses one 16 bit value for characters in the BMP, but two 16 bit
values for characters outside the BMP:
http://en.wikipedia.org/wiki/UTF-16/UCS-2.  The two 16 bit values are
referred to as a 'surrogate pair' - see the **surrogate pair** entry in
the Unicode glossary: http://www.unicode.org/glossary/#S.  UTF-16 is the
standard encoding for modern versions of windows.
