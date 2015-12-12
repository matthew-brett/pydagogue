.. _python-unicode:

##################
Python and unicode
##################

See :ref:`introducing-unicode` for an introduction to Unicode.

See also:

* http://docs.python.org/howto/unicode.html
* http://effbot.org/zone/unicode-objects.htm
* http://wiki.python.org/moin/Unicode

Python 2 supports unicode with unicode strings::

   s = u'Hello world'

Python 3 strings are always unicode. Python 3 as of Python 3.3 allows (but
ignores) the ``u`` prefix for strings, so I will use that convention for
unicode strings for compatibility with Python 2 and Python 3.

There are various ways of inputing characters you cannot type at your prompt.
The most basic is to give the unicode code point in hexadecimal::

   question = u'\u00bfHabla espa\u00f1ol?'  # ¿Habla español?

where ``00bf`` is the hexadecimal unicode code point for the inverted question
mark; see http://www.unicode.org/Public/UNIDATA/UnicodeData.txt.  Use the
``\u0000`` format, i.e. ``\u`` followed by 4 hexadecimal digits.  For code
points outside the 16 bit range (outside the BMP |--| see
:ref:`introducing-unicode`) |--| use capital ``U`` and eight hexadecimal
digits, like this::

   complicated = u'\U0001D11A is musical symbol 5 line staff'

See below for some complications of using these 32 bit unicode characters in
some builds of python 2.

You can also use the standard unicode name (see
http://www.unicode.org/Public/UNIDATA/UnicodeData.txt )::

   less_opaque = u'\N{MUSICAL SYMBOL FIVE-LINE STAFF} is more obviously a five line staff'

To create an UTF-8 encoded version of a string - for example to write to a
text file::

   question = u'\u00bfHabla espa\u00f1ol?'  # ¿Habla español?
   raw_str = question.encode('utf-8')

Similarly for UTF-16, or other encodings:
http://docs.python.org/lib/standard-encodings.html

::

   raw_str = question.encode('utf-16')

To get a unicode string from text that has been encoded::

   question = raw_str.decode('utf-8')

In Python 3, ``raw_str`` will be a *byte string* rather than a standard
(unicode) string.

*******************************************
Python internal encoding of unicode strings
*******************************************

The internal encoding of unicode strings depends on the version of Python.

*******************************
Python versions 2.2 through 3.2
*******************************

The internal representation of unicode stirngs Pythons 2.2 through 3.2 depends
on flags with which the Python program binary was built.  Pythons built with
the build flag ``--enable-unicode=ucs2`` `use UTF-16 as the internal
representation
<https://mail.python.org/pipermail/python-dev/2008-July/080892.html>`_.  Yes,
it is confusing that the flag value is ``ucs2`` and the actual result is
UTF-16.  Pythons built with build flag ``--enable-unicode=ucs4`` use UCS-4 (or
equivalently, UTF-32) as their internal representation.

To tell which format your Python uses::

   import sys
   utf_16 = sys.maxunicode == 65535


If ``utf_16`` is True, you have a UTF-16 build, otherwise you have UCS4.

See also:

* http://www.python.org/dev/peps/pep-0100/
* http://www.python.org/dev/peps/pep-0261/

UTF-16 (ucs2) builds of Python and 32 bit unicode code points
=============================================================

If you have a UTF-16 build of python, and want to use a 32 bit code point,
then some oddness occurs::

   complicated = u'\U0001D11A '
   print ord(complicated[0])
   print ord(complicated[1])

On a UTF-16 build the above gives you::

   55348
   56602

In this case, the 32 bit value has been represented by two 16 bit values - a
UTF-16 **surrogate pair** - see :ref:`introducing-unicode`.

On a UCS-4 build you get::

   119066
   32

which might have been more what you were expecting - 119066 is the
decimal representation of hexadecimal 1D11A.  The difference between the two
builds can mean some oddness in slicing strings... (as noted in
http://www.python.org/dev/peps/pep-0261/).

Some discussion about UTF-16 / UCS-2, UCS-4 and Python 3 here:
http://mail.python.org/pipermail/python-dev/2008-July/080886.html

************************
Python versions from 3.3
************************

Python versions 3.3 and above use a flexible internal representation of the
string that depends on the string contents |--| see
http://www.python.org/dev/peps/pep-0393.

************************************
Relevant python modules and commands
************************************

Modules
=======

* `codecs <https://docs.python.org/2/library/codecs.html>`_;
* `unicodedata <https://docs.python.org/2/library/unicodedata.html>`_;
* `locale <http://docs.python.org/2/library/locale.html>`_ (``locale.getdefaultlocale``);
* `regular expressions <http://docs.python.org/2/library/re.html>`_ - ``(?u)``
  flag, ``re.UNICODE``;
* `standard encodings <https://docs.python.org/2/library/codecs.html#standard-encodings>`_;
* encodings - e.g. ``encodings.getaliases()``

String methods
==============

* encode
* decode

Builtins
========

* unichr - unicode equivalent of ``chr`` in Python 2.
* unicode - constructor for unicode strings in Python 2.

Exceptions:
===========

* UnicodeEncodeError

.. include:: links_names.inc
