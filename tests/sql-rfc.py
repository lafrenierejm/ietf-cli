#!/usr/bin/env python3
import os
import sys
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
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


if __name__ == '__main__':
    unittest.main()
