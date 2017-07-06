#!/usr/bin/env python3
from typing import List
import xml.etree.ElementTree
from .enum import DocumentType

NAMESPACE = {'index': 'http://www.rfc-editor.org/rfc-index'}


def findall(root: xml.etree.ElementTree.Element, doc_type: DocumentType) -> List[xml.etree.ElementTree.Element]:
    """Return a list of all entries of type `doc_type`."""
    return root.findall('index:{}-entry'.format(doc_type.value.lower()),
                        NAMESPACE)


def find_doc_id(entry: xml.etree.ElementTree.Element) -> int:
    """Retrieve the numerical part of `entry`'s ID"""
    doc_id = entry.find('index:doc-id', NAMESPACE).text
    # Strip the three DocumentType letters off the ID
    return int(doc_id[3:])
