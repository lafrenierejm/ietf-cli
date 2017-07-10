#!/usr/bin/env python3
import os
import sys
import unittest
import xml.etree.ElementTree as ET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from ietf_cli.sql.base import Base
    from ietf_cli.sql.bcp import Bcp
    from ietf_cli.xml.bcp import add_all
except:
    raise


class TestXmlBcp(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/bcp-index.xml')
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

    def test_num_rows(self):
        # Get the RFCs from the DB session
        self.rows = self.session.query(Bcp).order_by(Bcp.id).all()
        self.assertEqual(2, len(self.rows))

    def test_title(self):
        self.bcp0002 = self.session.query(Bcp).filter(Bcp.id == 2).one()
        self.assertIsNone(self.bcp0002.title)
        self.bcp0003 = self.session.query(Bcp).filter(Bcp.id == 3).one()
        self.assertIsNone(self.bcp0003.title)


if __name__ == '__main__':
    unittest.main()
