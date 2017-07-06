#!/usr/bin/env python3
import os
import sys
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from ietf_cli.sql.author import Author
    from ietf_cli.sql.base import Base
    from ietf_cli.sql.rfc import Rfc
    from ietf_cli.xml.enum import Status, Stream
except:
    raise


class TestRfc(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine, checkfirst=True)
        self.session = sessionmaker(bind=self.engine)()

        self.rfc0001 = Rfc(id=1, title='title for RFC 1', date_month=1,
                           date_year=1,
                           current_status=Status.UNKNOWN,
                           publication_status=Status.UNKNOWN)
        self.session.add(self.rfc0001)

        self.rfc0002 = Rfc(id=2, title='title for RFC 2',
                           date_month=2, date_year=2,
                           keywords='keywords for RFC 2',
                           abstract='abstract for RFC 2',
                           draft='draft for RFC 2',
                           notes='notes for RFC 2',
                           current_status=Status.UNKNOWN,
                           publication_status=Status.UNKNOWN,
                           stream=Stream.IETF,
                           area='area for RFC 2',
                           wg_acronym='wg_acronym for RFC 2',
                           errata_url='errata_url for RFC 2',
                           doi='doi for RFC 2')
        self.session.add(self.rfc0002)

    def test_authors(self):
        self.assertEqual(0, len(self.rfc0001.authors))  # before adding authors
        self.assertEqual(0, len(self.rfc0002.authors))  # before adding authors

        # Add formats information to the RFCs
        self.rfc0001.authors = [Author(name='Author 1 for RFC 1')]
        self.rfc0002.authors = [Author(name='Author 1 for RFC 2'),
                                Author(name='Author 2 for RFC 2')]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Check the DB's copy of rfc0001
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.assertEqual(1, len(self.rfc0001_query.authors))
        self.assertEqual('Author 1 for RFC 1',
                         self.rfc0001_query.authors[0].name)

        # Check the DB's copy of rfc0002
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()
        self.assertEqual(2, len(self.rfc0002_query.authors))
        self.assertEqual('Author 1 for RFC 2',
                         self.rfc0002_query.authors[0].name)
        self.assertIsNone(self.rfc0002_query.authors[0].title)


if __name__ == '__main__':
    unittest.main()
