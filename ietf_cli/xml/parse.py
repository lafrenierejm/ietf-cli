#!/usr/bin/env python3
from typing import List, Dict, Tuple
import xml.etree.ElementTree
from .enum import DocumentType, FileType, Month, Status, Stream

NAMESPACE = {'index': 'http://www.rfc-editor.org/rfc-index'}

DocId = Tuple[DocumentType, int]

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


def find_format(entry: xml.etree.ElementTree.Element) -> List[Tuple[FileType,
                                                                    int, int]]:
    """Return a list of triplets containing `entry`'s format information.

    Elements of tuples composing returned list:
    FileType -- describes a filetype
    int -- the character count
    int/None -- the page count
    """

    format_entries = entry.findall('index:format', NAMESPACE)
    formats = []

    for format_entry in format_entries:
        # Get the file format
        file_format = FileType(format_entry.find('index:file-format',
                                                 NAMESPACE).text)

        # Get the character count
        char_count = int(format_entry.find('index:char-count', NAMESPACE).text)

        # Get the page count, which is not guaraneed to exist
        ## Attempt to get the text from inside the XML page-count tag
        try:
            page_count_str = format_entry.find('index:page-count',
                                               NAMESPACE).text
        except AttributeError:
            page_count = None
        except:
            raise
        ## If there was no exception convert the retrieved str to an int
        else:
            page_count = int(page_count_str)

        # Add the triplet to formats
        formats.append((file_format, char_count, page_count))

    return formats


def find_abstract(entry: xml.etree.ElementTree.Element) -> List[str]:
    """Return a list of strings containing the paragraphs composing `entry`'s
    `abstract` element.
    """

    abstract = []
    try:
        abstract_pars = entry.find('index:abstract', NAMESPACE).\
            findall('index:p', NAMESPACE)
        for abstract_par in abstract_pars:
            abstract.append(abstract_par.text)
    except AttributeError:
        pass
    except:
        raise

    return abstract


def find_draft(entry: xml.etree.ElementTree.Element) -> str:
    """Return the `draft` element of `entry`."""
    draft = entry.find('index:draft', NAMESPACE)

    if draft is not None:
        return draft.text
    else:
        return None


def find_notes(entry: xml.etree.ElementTree.Element) -> str:
    """Return the `notes` element of `entry`."""
    notes = entry.find('index:notes', NAMESPACE)

    if notes is not None:
        return notes.text
    else:
        return None


def find_obsoletes(entry: xml.etree.ElementTree.Element) -> List[DocId]:
    """Return a list of binary tuples that represent the documents that `entry`
    obsoletes.

    The first element of the tuple is a DocumentType.
    The second element is an integer.
    """

    found_entry = entry.find('index:obsoletes', NAMESPACE)

    doc_ids = []
    if found_entry is not None:
        obsoletes = found_entry.findall('index:doc-id', NAMESPACE)
        for obsolete in obsoletes:
            text = obsolete.text  # Get the content of a doc-id element
            doc_type = DocumentType[text[0:3]]
            doc_id = int(text[3:])
            doc_ids.append((doc_type, doc_id))

    return doc_ids


def find_obsoleted_by(entry: xml.etree.ElementTree.Element) -> List[DocId]:
    """Return a list of binary tuples representing the documents that `entry`
    is obsoleted by.

    The first element of the tuple is a DocumentType.
    The second element is an integer.
    """

    found_entry = entry.find('index:obsoleted-by', NAMESPACE)

    doc_ids = []
    if found_entry is not None:
        obsoleted_by = found_entry.findall('index:doc-id', NAMESPACE)
        for by in obsoleted_by:
            text = by.text  # Get the content of a doc-id element
            doc_type = DocumentType[text[0:3]]
            doc_id = int(text[3:])
            doc_ids.append((doc_type, doc_id))

    return doc_ids


def find_updates(entry: xml.etree.ElementTree.Element) -> List[DocId]:
    """Return a list of binary tuples representing the documents that `entry`
    updates.

    The first element of the tuple is a DocumentType.
    The second element is an integer.
    """

    found_entry = entry.find('index:updates', NAMESPACE)

    doc_ids = []
    if found_entry is not None:
        found_doc_ids = found_entry.findall('index:doc-id', NAMESPACE)
        for doc_id in found_doc_ids:
            text = doc_id.text  # Get the content of a doc-id element
            doc_type = DocumentType[text[0:3]]
            doc_num = int(text[3:])
            doc_ids.append((doc_type, doc_num))

    return doc_ids


def find_updated_by(entry: xml.etree.ElementTree.Element) -> List[DocId]:
    """Return a list of binary tuples representing the documents that `entry`
    is updated by.

    The first element of the tuple is a DocumentType.
    The second element is an integer.
    """

    found_entry = entry.find('index:updated-by', NAMESPACE)

    doc_ids = []
    if found_entry is not None:
        found_doc_ids = found_entry.findall('index:doc-id', NAMESPACE)
        for doc_id in found_doc_ids:
            text = doc_id.text  # Get the content of a doc-id element
            doc_type = DocumentType[text[0:3]]
            doc_num = int(text[3:])
            doc_ids.append((doc_type, doc_num))

    return doc_ids


def find_is_also(entry: xml.etree.ElementTree.Element) -> List[DocId]:
    """Return a list of binary tuples representing the documents that are
    aliases for `entry`.

    The first element of the tuple is a DocumentType.
    The second element is an integer.
    """

    found_entry = entry.find('index:is-also', NAMESPACE)

    doc_ids = []
    if found_entry is not None:
        found_doc_ids = found_entry.findall('index:doc-id', NAMESPACE)
        for doc_id in found_doc_ids:
            text = doc_id.text  # Get the content of a doc-id element
            doc_type = DocumentType[text[0:3]]
            doc_num = int(text[3:])
            doc_ids.append((doc_type, doc_num))

    return doc_ids


def find_see_also(entry: xml.etree.ElementTree.Element) -> List[DocId]:
    """References to other related documents - intended as helpful information
    to the reader.

    The references are returned as a list of tuples.

    The first element of the tuple is a DocumentType.
    The second element is the ID number of that document.
    """

    found_entry = entry.find('index:see-also', NAMESPACE)

    doc_ids = []
    if found_entry is not None:
        found_doc_ids = found_entry.findall('index:doc-id', NAMESPACE)
        for doc_id in found_doc_ids:
            text = doc_id.text  # Get the content of a doc-id element
            doc_type = DocumentType[text[0:3]]
            doc_num = int(text[3:])
            doc_ids.append((doc_type, doc_num))

    return doc_ids


def find_current_status(entry: xml.etree.ElementTree.Element) -> Status:
    """Return `entry`'s current status."""
    return Status(entry.find('index:current-status', NAMESPACE).text)


def find_publication_status(entry: xml.etree.ElementTree.Element) -> Status:
    """Return the status of `entry` at the time of its publication."""
    return Status(entry.find('index:publication-status', NAMESPACE).text)


def find_stream(entry: xml.etree.ElementTree.Element) -> Status:
    """Return the `stream` element of `entry`."""
    stream_entry = entry.find('index:stream', NAMESPACE)

    if stream_entry is not None:
        return Stream(stream_entry.text)
    else:
        return None


def find_area(entry: xml.etree.ElementTree.Element) -> str:
    """Return the `area` element of `entry`."""
    area_entry = entry.find('index:area', NAMESPACE)

    if area_entry is not None:
        return area_entry.text
    else:
        return None


def find_wg_acronym(entry: xml.etree.ElementTree.Element) -> str:
    """Return the `wg_acronym` element of `entry`."""
    acronym_entry = entry.find('index:wg_acronym', NAMESPACE)

    if acronym_entry is not None:
        return acronym_entry.text
    else:
        return None


def find_errata_url(entry: xml.etree.ElementTree.Element) -> str:
    """Return the `errata_url` element of `entry`."""
    errata_entry = entry.find('index:errata-url', NAMESPACE)

    if errata_entry is not None:
        return errata_entry.text
    else:
        return None
