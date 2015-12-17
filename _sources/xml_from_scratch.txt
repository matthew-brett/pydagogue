###########################
XML from absolutely nothing
###########################

************
XML elements
************

The basic unit of an XML document is an `XML element
<http://www.w3schools.com/xml/xml_elements.asp>`_.

A standard XML element consists of:

* a start *tag* |--| e.g. ``<my-element>``;
* optional content |--| e.g. ``Some data``;
* an end *tag* |--| e.g. ``</my-element>``.

::

    <my-element>Some data</my-element>

If an element has no content, it can be abbreviated into an *empty element
tag*::

    <my-element />

.. testcode::
    :hide:

    from __future__ import print_function
    import xml.etree.ElementTree as ET
    print(ET.fromstring("<my-element />").tag)

.. testoutput::
    :hide:

    my-element

To repeat then, there are three types of tag:

* a start tag |--| e.g. ``<a-name>``;
* an end tag |--| e.g. ``</a-name>``;
* an empty element tag |--| e.g ``<a-name />``.

A tag always starts with ``<`` and ends with ``>``.

A start tag and an empty element tag must start with an *element name*. This
is a case-sensitive string starting with a letter or underscore, followed by
any combination of letters, digits, hyphens, underscores, and periods.

A start tag and an empty element tag can have *attributes*. These are name,
value pairs::

    <a-name an-attribute="my value" another-attribute="3">Some text</a-name>
    <a-name an-attribute="my value" another-attribute="3" />

The *content* of an element consists of zero or more items, where an item can
be:

* Text
* An element

Elements contained in other elements are *child elements*, e.g::

    <a-parent>
        <a-child>with text content</a-child>
        <another-child>with more text</another-child>
    </a-parent>

You can mix text items and element items in element content, like this::

    <a-parent>
        Some text
        <a-child>with text content</a-child>
        More text
        <another-child>with more text</another-child>
        Text continues
    </a-parent>

but it is more common to have element content that is *either* one or more
element items, *or* one single text item.

*************
XML documents
*************

There is a single element at the root of a valid XML document. This is the
*root element*.

.. writefile::
    :language: xml
    :cwd: /working

    # file: some_example.xml
    <a-root-element my-type="example">
        <at-second-level>
            <first-thing>Some text</first-thing>
            <second-thing>More text</second-thing>
        </at-second-level>
    </a-root-element>

To take another example, this would be a valid XML document, because it has a
single element at the root level::

    <my-element>
        Some text
    </my-element>

But this would not, because it has two elements at the root level::

    <my-element>
        Some text
    </my-element>
    <another-element>
        More text
    </another-element>

The XML document may start with a special construction called the *XML prolog*
of this form::

    <?xml version="1.0"?>

Default XML encoding is UTF-8, but you can specify another encoding in the XML
prolog::

    <?xml version="1.0" encoding="UTF-16"?>

***********
Reading XML
***********

For example, in Python:

.. workrun:: pycon

    >>> import xml.etree.ElementTree as ET
    >>> tree = ET.parse('some_example.xml')
    >>> root = tree.getroot()
    >>> print(root.tag)
    >>> print(root.attrib)
    >>> children = root.getchildren()
    >>> print(len(children))
    >>> only_child = children[0]
    >>> for child in only_child.getchildren():
    ...     print(child.tag, child.text)

.. include:: links_names.inc
