#!/usr/bin/env python3
from typing import List, Dict
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


def find_title(entry: xml.etree.ElementTree.Element) -> str:
    """Return the `title` element of `entry`."""
    return entry.find('index:title', NAMESPACE).text


def find_author(entry: xml.etree.ElementTree.Element) -> List[Dict[str, str]]:
    """Return a list containing `entry`'s author information.

    Each entry in the list is a dict of strings.  The dict's keys are 'name',
    'title', 'orgaization', and 'org_abbrev'.  All will have values in the
    returned dict, but only 'name' is guaranteed to have a non-None value.
    """

    author_entries = entry.findall('index:author', NAMESPACE)
    authors = []

    for author_entry in author_entries:
        author = {}

        # Set author's name
        name = author_entry.find('index:name', NAMESPACE).text
        author['name'] = name

        # Set author's title, which is not guaranteed to exist
        try:
            title = author_entry.find('index:title', NAMESPACE).text
        except AttributeError:
            title = None
        except:
            raise
        author['title'] = title

        # Set author's organization, which is not guaranteed to exist
        try:
            organization = author_entry.find('index:organization',
                                             NAMESPACE).text
        except AttributeError:
            organization = None
        except:
            raise
        author['organization'] = organization

        # Set author's org_abbrev, which is not guaranteed to exist
        try:
            org_abbrev = author_entry.find('index:org-abbrev', NAMESPACE).text
        except AttributeError:
            org_abbrev = None
        except:
            raise
        author['org_abbrev'] = org_abbrev

        # Add author to the list of authors
        authors.append(author)

    return authors
