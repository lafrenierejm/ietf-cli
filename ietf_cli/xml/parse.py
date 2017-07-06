#!/usr/bin/env python3
from typing import List, Dict
import xml.etree.ElementTree
from .enum import DocumentType, Month

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


def find_date(entry: xml.etree.ElementTree.Element) -> Dict[str, int]:
    """Return a dict containing `entry`'s publication date.

    The dict's keys are 'year', 'month', and 'day'.
    - 'year' is a integer year from the Gregorian calendar
    (https://www.w3.org/TR/2001/REC-xmlschema-2-20010502/#gYear).
    - 'month' is an integer in the range [1,12].
    - 'day' is the day of the month.  Its value is either an integer in the
    range [0,31] or None.
    """
    date_entry = entry.find('index:date', NAMESPACE)
    date = {}

    # Set date's year
    year_str = date_entry.find('index:year', NAMESPACE).text
    date['year'] = int(year_str)

    # Set date's month
    month_str = date_entry.find('index:month', NAMESPACE).text
    month = Month[month_str].value
    date['month'] = month

    # Set date's day of the month, which is not guaranteed to exist
    ## Attempt to get the text from inside the XML day tag
    try:
        day_str = date_entry.find('index:day', NAMESPACE).text
    except AttributeError:
        day = None
    except:
        raise
    ## If there was no exception convert the retrieved str to an int
    else:
        day = int(day_str)
    date['day'] = day

    return date
