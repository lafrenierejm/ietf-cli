#!/usr/bin/env python3
import os
import sys
import unittest
import xml.etree.ElementTree as ET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    import ietf_cli.xml.rfc as rfc

    from ietf_cli.sql.base import Base
    from ietf_cli.sql.rfc import Rfc
    from ietf_cli.xml.enum import DocumentType, FileType
except:
    raise


class TestXmlRfc(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/rfc-index.xml')
    namespace = {'index': 'http://www.rfc-editor.org/rfc-index'}

    def setUp(self):
        # XML tree
        self.tree = ET.parse(type(self).data_file)
        self.root = self.tree.getroot()
        # sqlalchemy session
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine, checkfirst=True)
        self.session = sessionmaker(bind=self.engine)()
        # Add all RFC entries in self.root to self.session
        rfc.add_all(self.session, self.root)

    def test_num_rows(self):
        # Get the RFCs from the DB session
        self.rows = self.session.query(Rfc).order_by(Rfc.id).all()
        self.assertEqual(3, len(self.rows))

    def test_authors(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(3, len(self.rfc8180.authors))
        self.assertEqual('X. Vilajosana', self.rfc8180.authors[0].name)
        self.assertEqual('Editor', self.rfc8180.authors[0].title)
        self.assertIsNone(self.rfc8180.authors[0].organization)
        self.assertIsNone(self.rfc8180.authors[0].org_abbrev)
        self.assertEqual('K. Pister', self.rfc8180.authors[1].name)
        self.assertIsNone(self.rfc8180.authors[1].title)
        self.assertIsNone(self.rfc8180.authors[1].organization)
        self.assertIsNone(self.rfc8180.authors[1].org_abbrev)
        self.assertEqual('T. Watteyne', self.rfc8180.authors[2].name)
        self.assertIsNone(self.rfc8180.authors[2].title)
        self.assertIsNone(self.rfc8180.authors[2].organization)
        self.assertIsNone(self.rfc8180.authors[2].org_abbrev)
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(1, len(self.rfc0010.authors))
        self.assertEqual('S.D. Crocker', self.rfc0010.authors[0].name)
        self.assertIsNone(self.rfc0010.authors[0].title)
        self.assertIsNone(self.rfc0010.authors[0].organization)
        self.assertIsNone(self.rfc0010.authors[0].org_abbrev)
        # RFC 8174 has the same author structure as RFC 0010

    def test_formats(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(1, len(self.rfc8180.formats))
        self.assertEqual(FileType.ASCII, self.rfc8180.formats[0].filetype)
        self.assertEqual(60068, self.rfc8180.formats[0].char_count)
        self.assertEqual(28, self.rfc8180.formats[0].page_count)

    def test_abstract(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(1, len(self.rfc8180.abstract))
        self.assertEqual('This document describes a minimal mode of operation '
                         'for an IPv6 over the TSCH mode of IEEE 802.15.4e '
                         '(6TiSCH) network.',
                         self.rfc8180.abstract[0].par)

    def test_obsoletes(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(0, len(self.rfc8180.obsoletes))
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(3, len(self.rfc0010.obsoletes))
        self.assertEqual(DocumentType.RFC, self.rfc0010.obsoletes[0].doc_type)
        self.assertEqual(24, self.rfc0010.obsoletes[0].doc_id)
        self.assertEqual(DocumentType.RFC, self.rfc0010.obsoletes[1].doc_type)
        self.assertEqual(27, self.rfc0010.obsoletes[1].doc_id)
        self.assertEqual(DocumentType.RFC, self.rfc0010.obsoletes[2].doc_type)
        self.assertEqual(30, self.rfc0010.obsoletes[2].doc_id)
        # RFC 8174
        self.rfc8174 = self.session.query(Rfc).filter(Rfc.id == 8174).one()
        self.assertEqual(1, len(self.rfc8174.obsoletes))
        self.assertEqual(DocumentType.RFC, self.rfc8174.obsoletes[0].doc_type)
        self.assertEqual(2119, self.rfc8174.obsoletes[0].doc_id)

    def test_obsoleted_by(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(0, len(self.rfc8180.obsoleted_by))
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(3, len(self.rfc0010.obsoleted_by))
        self.assertEqual(DocumentType.RFC,
                         self.rfc0010.obsoleted_by[0].doc_type)
        self.assertEqual(24, self.rfc0010.obsoleted_by[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0010.obsoleted_by[1].doc_type)
        self.assertEqual(27, self.rfc0010.obsoleted_by[1].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0010.obsoleted_by[2].doc_type)
        self.assertEqual(30, self.rfc0010.obsoleted_by[2].doc_id)
        # RFC 8174
        self.rfc8174 = self.session.query(Rfc).filter(Rfc.id == 8174).one()
        self.assertEqual(1, len(self.rfc8174.obsoleted_by))
        self.assertEqual(DocumentType.RFC,
                         self.rfc8174.obsoleted_by[0].doc_type)
        self.assertEqual(2119, self.rfc8174.obsoleted_by[0].doc_id)

    def test_updates(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(0, len(self.rfc8180.updates))
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(3, len(self.rfc0010.updates))
        self.assertEqual(DocumentType.RFC, self.rfc0010.updates[0].doc_type)
        self.assertEqual(24, self.rfc0010.updates[0].doc_id)
        self.assertEqual(DocumentType.RFC, self.rfc0010.updates[1].doc_type)
        self.assertEqual(27, self.rfc0010.updates[1].doc_id)
        self.assertEqual(DocumentType.RFC, self.rfc0010.updates[2].doc_type)
        self.assertEqual(30, self.rfc0010.updates[2].doc_id)
        # RFC 8174
        self.rfc8174 = self.session.query(Rfc).filter(Rfc.id == 8174).one()
        self.assertEqual(1, len(self.rfc8174.updates))
        self.assertEqual(DocumentType.RFC, self.rfc8174.updates[0].doc_type)
        self.assertEqual(2119, self.rfc8174.updates[0].doc_id)

    def test_updated_by(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(0, len(self.rfc8180.updated_by))
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(3, len(self.rfc0010.updated_by))
        self.assertEqual(DocumentType.RFC, self.rfc0010.updated_by[0].doc_type)
        self.assertEqual(24, self.rfc0010.updated_by[0].doc_id)
        self.assertEqual(DocumentType.RFC, self.rfc0010.updated_by[1].doc_type)
        self.assertEqual(27, self.rfc0010.updated_by[1].doc_id)
        self.assertEqual(DocumentType.RFC, self.rfc0010.updated_by[2].doc_type)
        self.assertEqual(30, self.rfc0010.updated_by[2].doc_id)
        # RFC 8174
        self.rfc8174 = self.session.query(Rfc).filter(Rfc.id == 8174).one()
        self.assertEqual(1, len(self.rfc8174.updated_by))
        self.assertEqual(DocumentType.RFC, self.rfc8174.updated_by[0].doc_type)
        self.assertEqual(2119, self.rfc8174.updated_by[0].doc_id)

    def test_is_also(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(1, len(self.rfc8180.is_also))
        self.assertEqual(DocumentType.BCP, self.rfc8180.is_also[0].doc_type)
        self.assertEqual(210, self.rfc8180.is_also[0].doc_id)
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(0, len(self.rfc0010.is_also))
        # RFC 8174
        self.rfc8174 = self.session.query(Rfc).filter(Rfc.id == 8174).one()
        self.assertEqual(1, len(self.rfc8174.is_also))
        self.assertEqual(DocumentType.BCP, self.rfc8174.is_also[0].doc_type)
        self.assertEqual(14, self.rfc8174.is_also[0].doc_id)

    def test_see_also(self):
        # RFC 8180
        self.rfc8180 = self.session.query(Rfc).filter(Rfc.id == 8180).one()
        self.assertEqual(1, len(self.rfc8180.see_also))
        self.assertEqual(DocumentType.BCP, self.rfc8180.see_also[0].doc_type)
        self.assertEqual(0, self.rfc8180.see_also[0].doc_id)
        # RFC 0010
        self.rfc0010 = self.session.query(Rfc).filter(Rfc.id == 10).one()
        self.assertEqual(0, len(self.rfc0010.see_also))
        # RFC 8174
        self.rfc8174 = self.session.query(Rfc).filter(Rfc.id == 8174).one()
        self.assertEqual(0, len(self.rfc8174.see_also))


if __name__ == '__main__':
    unittest.main()
