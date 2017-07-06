#!/usr/bin/env python3
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    import ietf_cli.xml.parse as parse
    from ietf_cli.xml.enum import DocumentType, FileType
except:
    raise


class TestParse(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/rfc-index.xml')
    namespace = {'index': 'http://www.rfc-editor.org/rfc-index'}

    def setUp(self):
        self.tree = ET.parse(type(self).data_file)
        self.root = self.tree.getroot()
        self.entries = parse.findall(self.root, DocumentType.RFC)

    def test_findall(self):
        self.assertEqual(3, len(self.entries))

    def test_find_doc_id(self):
        self.assertEqual(8180, parse.find_doc_id(self.entries[0]))
        self.assertEqual(10, parse.find_doc_id(self.entries[1]))
        self.assertEqual(8174, parse.find_doc_id(self.entries[2]))

    def test_find_title(self):
        self.assertEqual(  # 8180
            'Minimal IPv6 over the TSCH Mode of IEEE 802.15.4e (6TiSCH) '
            'Configuration',
            parse.find_title(self.entries[0])
        )
        self.assertEqual(  # 10
            'Documentation conventions',
            parse.find_title(self.entries[1])
        )
        self.assertEqual(  # 8174
            'Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words',
            parse.find_title(self.entries[2])
        )

    def test_find_author(self):
        authors = parse.find_author(self.entries[0])

        # name
        self.assertEqual(
            'X. Vilajosana',
            authors[0]['name']
        )
        self.assertEqual(
            'K. Pister',
            authors[1]['name']
        )
        self.assertEqual(
            'T. Watteyne',
            authors[2]['name']
        )

        # title
        self.assertEqual(
            'Editor',
            authors[0]['title']
        )
        self.assertIsNone(
            authors[1]['title']
        )
        self.assertIsNone(
            authors[2]['title']
        )

        # organization
        self.assertIsNone(
            authors[0]['organization']
        )
        self.assertIsNone(
            authors[1]['organization']
        )
        self.assertIsNone(
            authors[2]['organization']
        )

        # org-abbrev
        self.assertIsNone(
            authors[0]['org_abbrev']
        )
        self.assertIsNone(
            authors[1]['org_abbrev']
        )
        self.assertIsNone(
            authors[2]['org_abbrev']
        )

    def test_find_date(self):
        date = parse.find_date(self.entries[0])

        self.assertIsNone(
            date['day']
        )
        self.assertEqual(
            5,
            date['month']
        )
        self.assertEqual(
            2017,
            date['year']
        )

    def test_find_format(self):
        forms = parse.find_format(self.entries[0])
        self.assertEqual(1, len(forms))
        file_format, char_count, page_count = forms[0]

        self.assertEqual(
            parse.FileType.ASCII,
            file_format
        )
        self.assertEqual(
            60068,
            char_count
        )
        self.assertEqual(
            28,
            page_count
        )

    def test_find_abstract(self):
        abstract = parse.find_abstract(self.entries[0])  # RFC 8180
        self.assertEqual(1, len(abstract))
        self.assertEqual(  # RFC 8180
            'This document describes a minimal mode of operation for '
            'an IPv6 over the TSCH mode of IEEE 802.15.4e (6TiSCH) network.',
            abstract[0]
        )

        abstract = parse.find_abstract(self.entries[1])  # RFC 0010
        self.assertEqual(
            [],
            abstract
        )

        abstract = parse.find_abstract(self.entries[2])  # RFC 8174
        self.assertEqual(1, len(abstract))
        self.assertEqual(
            'RFC 2119 specifies common key words that may be used in protocol '
            'specifications.  This document aims to reduce the ambiguity by '
            'clarifying that only UPPERCASE usage of the key words have the '
            'defined special meanings.',
            abstract[0]
        )

    def test_find_draft(self):
        self.assertEqual(  # RFC 8180
            'draft-ietf-6tisch-minimal-21',
            parse.find_draft(self.entries[0])
        )

        self.assertIsNone(  # RFC 0010
            parse.find_draft(self.entries[1])
        )

        self.assertEqual(  # RFC 8174
            'draft-leiba-rfc2119-update-02',
            parse.find_draft(self.entries[2])
        )


if __name__ == '__main__':
    unittest.main()
