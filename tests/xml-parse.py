#!/usr/bin/env python3
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    import ietf_cli.xml.parse as parse
    from ietf_cli.xml.enum import DocumentType, FileType, Status, Stream
except:
    raise


class TestParse(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/rfc-index.xml')
    namespace = {'index': 'http://www.rfc-editor.org/rfc-index'}

    def setUp(self):
        self.tree = ET.parse(type(self).data_file)
        self.root = self.tree.getroot()
        self.entries = parse.findall(self.root, 'rfc-entry')

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
        year, month, day = parse.find_date(self.entries[0])  # 8180
        self.assertEqual(2017, year)
        self.assertEqual(5, month)
        self.assertIsNone(day)

        year, month, day = parse.find_date(self.entries[1])  # 0010
        self.assertEqual(1969, year)
        self.assertEqual(7, month)
        self.assertIsNone(day)

        year, month, day = parse.find_date(self.entries[1])  # 8174
        self.assertEqual(2017, year)
        self.assertEqual(5, month)
        self.assertEqual(1, day)

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

    def test_find_notes(self):
        self.assertIsNone(  # RFC 8180
            parse.find_notes(self.entries[0])
        )

        self.assertIsNone(  # RFC 0010
            parse.find_notes(self.entries[1])
        )

        self.assertIsNone(  # RFC 8174
            parse.find_notes(self.entries[2])
        )

    def test_find_obsoletes(self):
        doc_ids = parse.find_obsoletes(self.entries[0])  # RFC 8180
        self.assertEqual(
            [],
            doc_ids
        )

        doc_ids = parse.find_obsoletes(self.entries[1])  # RFC 0010
        # RFC0010 obsoletes 3 entries
        self.assertEqual(
            3,
            len(doc_ids)
        )
        # The first is RFC0024
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            24,
            doc_ids[0][1]
        )
        # The second is RFC0027
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[1][0]
        )
        self.assertEqual(
            27,
            doc_ids[1][1]
        )
        # The second is RFC0030
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[2][0]
        )
        self.assertEqual(
            30,
            doc_ids[2][1]
        )

        doc_ids = parse.find_obsoletes(self.entries[2])  # RFC 8174
        # 1 entry
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            2119,
            doc_ids[0][1]
        )

    def test_find_obsoleted_by(self):
        doc_ids = parse.find_obsoleted_by(self.entries[0])  # RFC 8180
        self.assertEqual(
            [],
            doc_ids
        )

        doc_ids = parse.find_obsoleted_by(self.entries[1])  # RFC 0010
        # RFC0010 obsoleted_by 3 entries
        self.assertEqual(
            3,
            len(doc_ids)
        )
        # The first is RFC0024
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            24,
            doc_ids[0][1]
        )
        # The second is RFC0027
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[1][0]
        )
        self.assertEqual(
            27,
            doc_ids[1][1]
        )
        # The second is RFC0030
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[2][0]
        )
        self.assertEqual(
            30,
            doc_ids[2][1]
        )

        doc_ids = parse.find_obsoleted_by(self.entries[2])  # RFC 8174
        # 1 entry
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            2119,
            doc_ids[0][1]
        )

    def test_find_updates(self):
        doc_ids = parse.find_updates(self.entries[0])  # RFC 8180
        self.assertEqual(
            [],
            doc_ids
        )

        doc_ids = parse.find_updates(self.entries[1])  # RFC 0010
        # RFC0010 updates 3 entries
        self.assertEqual(
            3,
            len(doc_ids)
        )
        # The first is RFC0024
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            24,
            doc_ids[0][1]
        )
        # The second is RFC0027
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[1][0]
        )
        self.assertEqual(
            27,
            doc_ids[1][1]
        )
        # The second is RFC0030
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[2][0]
        )
        self.assertEqual(
            30,
            doc_ids[2][1]
        )

        doc_ids = parse.find_updates(self.entries[2])  # RFC8174
        # 1 entry
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            2119,
            doc_ids[0][1]
        )

    def test_find_updated_by(self):
        doc_ids = parse.find_updated_by(self.entries[0])  # RFC 8180
        self.assertEqual(
            [],
            doc_ids
        )

        doc_ids = parse.find_updated_by(self.entries[1])  # RFC 0010
        self.assertEqual(
            3,
            len(doc_ids)
        )
        # The first is RFC0024
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            24,
            doc_ids[0][1]
        )
        # The second is RFC0027
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[1][0]
        )
        self.assertEqual(
            27,
            doc_ids[1][1]
        )
        # The second is RFC0030
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[2][0]
        )
        self.assertEqual(
            30,
            doc_ids[2][1]
        )

        doc_ids = parse.find_updated_by(self.entries[2])  # RFC 8174
        # 1 entry
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.RFC,
            doc_ids[0][0]
        )
        self.assertEqual(
            2119,
            doc_ids[0][1]
        )

    def test_find_is_also(self):
        doc_ids = parse.find_is_also(self.entries[0])  # RFC 8180
        # There is 1 reference to BCP0000
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.BCP,
            doc_ids[0][0]
        )
        self.assertEqual(
            210,
            doc_ids[0][1]
        )

        doc_ids = parse.find_is_also(self.entries[1])  # RFC 0010
        # There are no aliases
        self.assertEqual(
            [],
            doc_ids
        )

        doc_ids = parse.find_is_also(self.entries[2])  # RFC 8174
        # There is one alias
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.BCP,
            doc_ids[0][0]
        )
        self.assertEqual(
            14,
            doc_ids[0][1]
        )

    def test_find_see_also(self):
        doc_ids = parse.find_see_also(self.entries[0])  # RFC 8180
        # There is 1 reference
        self.assertEqual(
            1,
            len(doc_ids)
        )
        self.assertEqual(
            parse.DocumentType.BCP,
            doc_ids[0][0]
        )
        self.assertEqual(
            0,
            doc_ids[0][1]
        )

        doc_ids = parse.find_see_also(self.entries[1])  # RFC 0010
        # There are no references
        self.assertEqual(
            [],
            doc_ids
        )

        doc_ids = parse.find_see_also(self.entries[1])  # RFC 8174
        # There are no references
        self.assertEqual(
            [],
            doc_ids
        )

    def test_find_current_status(self):
        self.assertEqual(Status.BEST_CURRENT_PRACTICE,
                         parse.find_current_status(self.entries[0]))

        self.assertEqual(Status.UNKNOWN,
                         parse.find_current_status(self.entries[1]))

        self.assertEqual(Status.BEST_CURRENT_PRACTICE,
                         parse.find_current_status(self.entries[2]))

    def test_find_publication_status(self):
        self.assertEqual(Status.BEST_CURRENT_PRACTICE,
                         parse.find_publication_status(self.entries[0]))

        self.assertEqual(Status.UNKNOWN,
                         parse.find_publication_status(self.entries[1]))

        self.assertEqual(Status.BEST_CURRENT_PRACTICE,
                         parse.find_publication_status(self.entries[2]))

    def test_find_stream(self):
        self.assertEqual(Stream.IETF,
                         parse.find_stream(self.entries[0]))

        self.assertIsNone(parse.find_stream(self.entries[1]))

        self.assertEqual(Stream.IETF,
                         parse.find_stream(self.entries[2]))

    def test_find_area(self):
        self.assertEqual('int', parse.find_area(self.entries[0]))

        self.assertIsNone(parse.find_area(self.entries[1]))

        self.assertIsNone(parse.find_area(self.entries[2]))

    def test_find_wg_acronym(self):
        self.assertEqual('6tisch', parse.find_wg_acronym(self.entries[0]))

        self.assertIsNone(parse.find_wg_acronym(self.entries[1]))

        self.assertEqual('NON WORKING GROUP',
                         parse.find_wg_acronym(self.entries[2]))

    def test_find_errata_url(self):
        self.assertEqual('http://www.rfc-editor.org/errata_search.php?rfc=31',
                         parse.find_errata_url(self.entries[0]))

        self.assertIsNone(parse.find_errata_url(self.entries[1]))

        self.assertEqual(
            'http://www.rfc-editor.org/errata_search.php?rfc=8174',
            parse.find_errata_url(self.entries[2]))

    def test_find_doi(self):
        self.assertEqual('10.17487/RFC8180',
                         parse.find_doi(self.entries[0]))

        self.assertEqual('10.17487/RFC0010',
                         parse.find_doi(self.entries[1]))

        self.assertEqual('10.17487/RFC8174',
                         parse.find_doi(self.entries[2]))


if __name__ == '__main__':
    unittest.main()
