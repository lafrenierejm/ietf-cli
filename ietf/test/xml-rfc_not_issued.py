#!/usr/bin/env python3
import os
import unittest
import xml.etree.ElementTree as ET

from ietf.sql.base import Base
from ietf.sql.rfc_not_issued import RfcNotIssued
from ietf.xml.rfc_not_issued import add_all
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestXmlRfc(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__),
                             'data/rfc_not_issued-index.xml')
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
        add_all(self.session, self.root)

    def test_row(self):
        # Get the RFCs from the DB session
        self.rows = self.session.query(RfcNotIssued).\
            order_by(RfcNotIssued.id).\
            all()
        self.assertEqual(1, len(self.rows))
        self.assertEqual(14, self.rows[0].id)


if __name__ == '__main__':
    unittest.main()
