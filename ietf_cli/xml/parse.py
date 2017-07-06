#!/usr/bin/env python3
from typing import List
import xml.etree.ElementTree
from .enum import DocumentType

NAMESPACE = {'index': 'http://www.rfc-editor.org/rfc-index'}


def findall(root: xml.etree.ElementTree.Element, doc_type: DocumentType) -> List[xml.etree.ElementTree.Element]:
    """Return a list of all entries of type `doc_type`."""
    return root.findall('index:{}-entry'.format(doc_type.value.lower()),
                        NAMESPACE)
