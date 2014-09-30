###########################
XML from absolutely nothing
###########################

The basic unit of an XML document is an *element*.

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

A start tag and an empty element tag can have *attributes*. These are name,
value pairs::

    <a-name an-attribute="my value" another-attribute="3">Some text</a-name>
    <a-name an-attribute="my value" another-attribute="3" />

The *content* of an element can be:

* Empty
* Text
* One more other elements

Elements contained in other elements are *child elements*, e.g::

    <a-parent>
        <a-child>with text content</a-child>
        <another-child>with more text</another-child>
    </a-parent>

There is one single element at the root of a valid XML document:

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
