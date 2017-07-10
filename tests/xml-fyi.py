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
    from ietf_cli.sql.fyi import Fyi
    from ietf_cli.xml.fyi import add_all
except:
    raise


class TestXmlRfc(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/fyi-index.xml')
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
        self.rows = self.session.query(Fyi).order_by(Fyi.id).all()
        self.assertEqual(1, len(self.rows))

    def test_title(self):
        # RFC 8180
        self.std0002 = self.session.query(Fyi).filter(Fyi.id == 2).one()
        self.assertIsNone(self.std0002.title)


if __name__ == '__main__':
    unittest.main()
