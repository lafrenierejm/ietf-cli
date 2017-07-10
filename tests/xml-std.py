#!/usr/bin/env python3
import os
import sys
import unittest
import xml.etree.ElementTree as ET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    import ietf_cli.xml.std as std

    from ietf_cli.sql.base import Base
    from ietf_cli.sql.std import Std
except:
    raise


class TestXmlStd(unittest.TestCase):
    data_file = os.path.join(os.path.dirname(__file__), 'data/std-index.xml')
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
        std.add_all(self.session, self.root)

    def test_num_rows(self):
        self.rows = self.session.query(Std).order_by(Std.id).all()
        self.assertEqual(2, len(self.rows))

    def test_authors(self):
        self.std0001 = self.session.query(Std).filter(Std.id == 1).one()
        self.assertEqual('[STD number 1 is retired. It was "Internet Official '
                         'Protocol Standards".  See BCP 9 / RFC 7100 for more '
                         'information.]',
                         self.std0001.title)
        self.std0003 = self.session.query(Std).filter(Std.id == 3).one()
        self.assertEqual('Requirements for Internet Hosts', self.std0003.title)


if __name__ == '__main__':
    unittest.main()
