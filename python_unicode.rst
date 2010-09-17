.. _python-unicode:

Python and unicode
==================

See :ref:`introducing-unicode` for an introduction to Unicode.

See also:

* http://docs.python.org/howto/unicode.html
* http://effbot.org/zone/unicode-objects.htm
* http://wiki.python.org/moin/Unicode

Python supports unicode with unicode strings::

   s = u'Hello world'

There are various ways of inputing characters you cannot type at your
prompt.  The simplest is to give the unicode code point in octal::

   question = u'\u00bfHabla espa\u00f1ol?'  # ¿Habla español?

where ``00bf`` is the code for the inverted question mark; see
http://www.unicode.org/Public/UNIDATA/UnicodeData.txt.  Use the
``\u0000`` format, i.e. ``\u`` followed by 4 octal digits.  For code
points outside the 16 bit range (outside the BMP - see
:ref:`introducing-unicode` - use capital U and eight octal digits, like
this::

   complicated = u'\U0001D11A is musical symbol 5 line staff'

See below for some complications of using these 32 bit unicode
characters in python though.

You can also use the standard unicode name (see
http://www.unicode.org/Public/UNIDATA/UnicodeData.txt )::

   less_opaque = u'\N{MUSICAL SYMBOL FIVE-LINE STAFF} is more obviously a five line staff'

To create an utf-8 encoded version of a string - for example to write to a text file::

   question = u'\u00bfHabla espa\u00f1ol?'  # ¿Habla español?
   raw_str = question.encode('utf-8')

Similarly for UTF-16, or other encodings:
http://docs.python.org/lib/standard-encodings.html

::

   raw_str = question.encode('utf-16')

To get a unicode string from text that has been encoded::

   question = raw_str.decode('utf-8')

Python internal encoding of unicode strings
-------------------------------------------

Python - as of version 2.2 - either stores its unicode strings in UCS-2
or UCS-4 format.  See :ref:`introducing-unicode` for definitions of
UCS-2 and UCS-4.  Which one of these it uses is dictated by a compile
time flag such as ``-enable-unicode=ucs2``.

To tell which format your python uses::

   import sys
   ucs2 = sys.maxunicode == 65535


If ucs2 is True, you have UCS2, otherwise you have UCS4.

See also:

* http://www.python.org/dev/peps/pep-0100/
* http://www.python.org/dev/peps/pep-0261/

Python and 32 bit unicode code points
-------------------------------------

If you have a UCS-2 build of python, and want to use a 32 bit code
point, then some oddness occurs::

   complicated = u'\U0001D11A '
   print ord(complicated[0])
   print ord(complicated[1])

On a UCS-2 build the above gives you::

   55348
   56602

In this case, the 32 bit value has been represented by two 16 bit values - a **surrogate pair** - see :ref:`introducing-unicode`.

On a UCS-4 build you get::

   119066
   32

which might have been more what you were expecting - 119066 is the
decimal representation of octal 1D11A.  The difference between the two
builds can mean some oddness in slicing strings... (as noted in
http://www.python.org/dev/peps/pep-0261/).

Recent discussion about UCS-2, UCS-4 and Python 3 here:
http://mail.python.org/pipermail/python-dev/2008-July/080886.html

Relevant python modules and commands
------------------------------------

Modules
=======

* `codecs <http://docs.python.org/lib/module-codecs.html>`_
* `unicodedata <http://docs.python.org/lib/module-unicodedata.html>`_
* `locale <http://docs.python.org/lib/module-locale.html>`_ (locale.getdefaultlocale)
* `regular expressions <http://docs.python.org/lib/module-re.html>`_ - (?u) flag, re.UNICODE
* `standard encodings <http://docs.python.org/lib/standard-encodings.html>`_
* encodings - e.g. ``encodings.getaliases()``

String methods
==============

* encode
* decode

Builtins
========

* unichr - unicode equivalent of ``chr``
* unicode - constructor for unicode strings

Exceptions:
===========

* UnicodeEncodeError


