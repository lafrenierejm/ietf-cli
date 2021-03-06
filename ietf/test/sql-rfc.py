#!/usr/bin/env python3
import unittest

from ietf.sql.base import Base
from ietf.sql.rfc import (Abstract, Author, FileFormat, IsAlso, Keyword,
                          ObsoletedBy, Obsoletes, Rfc, SeeAlso, Stream,
                          UpdatedBy, Updates,)
from ietf.xml.enum import DocumentType, FileType, Status, Stream as StreamEnum
from ietf.xml.rfc import _add_keyword as add_keyword
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestSqlRfc(unittest.TestCase):

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
                           draft='draft for RFC 2',
                           notes='notes for RFC 2',
                           current_status=Status.UNKNOWN,
                           publication_status=Status.UNKNOWN,
                           area='area for RFC 2',
                           wg_acronym='wg_acronym for RFC 2',
                           errata_url='errata_url for RFC 2',
                           doi='doi for RFC 2')
        self.session.add(self.rfc0002)

    def test_abstract(self):
        self.assertEqual(0, len(self.rfc0001.abstract))  # no abstract
        self.assertEqual(0, len(self.rfc0002.abstract))  # no abstract

        # Add abstract information to the RFCs
        self.rfc0001.abstract = [Abstract(par='Abstract 1 for RFC 1')]
        self.rfc0002.abstract = [Abstract(par='Abstract 1 for RFC 2'),
                                 Abstract(par='Abstract 2 for RFC 2')]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Check the DB's copy of rfc0001
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.assertEqual(1, len(self.rfc0001_query.abstract))
        self.assertEqual('Abstract 1 for RFC 1',
                         self.rfc0001_query.abstract[0].par)

        # Check the DB's copy of rfc0002
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()
        self.assertEqual(2, len(self.rfc0002_query.abstract))
        self.assertEqual('Abstract 1 for RFC 2',
                         self.rfc0002_query.abstract[0].par)
        self.assertEqual('Abstract 2 for RFC 2',
                         self.rfc0002_query.abstract[1].par)

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

    def test_formats(self):
        self.assertEqual(0, len(self.rfc0001.formats))  # before adding formats
        self.assertEqual(0, len(self.rfc0002.formats))  # before adding formats

        # Add formats information to the RFCs
        self.rfc0001.formats = [FileFormat(filetype=FileType.ASCII,
                                           char_count=1)]
        self.rfc0002.formats = [FileFormat(filetype=FileType.ASCII,
                                           char_count=1),
                                FileFormat(filetype=FileType.ASCII,
                                           char_count=1, page_count=1)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.formats))
        self.assertEqual(FileType.ASCII,
                         self.rfc0001_query.formats[0].filetype)
        self.assertEqual(1, self.rfc0001_query.formats[0].char_count)
        self.assertIsNone(self.rfc0001_query.formats[0].page_count)

        # Assertions about rfc0002
        # number of format entries
        self.assertEqual(2, len(self.rfc0002_query.formats))
        # first format entry
        self.assertEqual(FileType.ASCII,
                         self.rfc0002_query.formats[0].filetype)
        self.assertEqual(1, self.rfc0002_query.formats[0].char_count)
        self.assertIsNone(self.rfc0002_query.formats[0].page_count)
        # second format entry
        self.assertEqual(FileType.ASCII,
                         self.rfc0002_query.formats[1].filetype)
        self.assertEqual(1, self.rfc0002_query.formats[1].char_count)
        self.assertEqual(1, self.rfc0002_query.formats[1].page_count)

    def test_obsoletes(self):
        self.assertEqual(0, len(self.rfc0001.obsoletes))  # none added
        self.assertEqual(0, len(self.rfc0002.obsoletes))  # none added

        # Add obsoletes information to the RFCs
        self.rfc0001.obsoletes = [Obsoletes(doc_id=1,
                                            doc_type=DocumentType.RFC)]
        self.rfc0002.obsoletes = [Obsoletes(doc_id=1,
                                            doc_type=DocumentType.RFC),
                                  Obsoletes(doc_id=2,
                                            doc_type=DocumentType.STD)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.obsoletes))
        self.assertEqual(1,
                         self.rfc0001_query.obsoletes[0].id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0001_query.obsoletes[0].doc_type)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.obsoletes))
        self.assertEqual(1,
                         self.rfc0002_query.obsoletes[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0002_query.obsoletes[0].doc_type)
        self.assertEqual(2,
                         self.rfc0002_query.obsoletes[1].doc_id)
        self.assertEqual(DocumentType.STD,
                         self.rfc0002_query.obsoletes[1].doc_type)

    def test_keywords(self):
        # No keywords have been assigned
        self.assertEqual(0, len(self.rfc0001.keywords))
        self.assertEqual(0, len(self.rfc0002.keywords))

        # Add keywords to the RFCs
        self.rfc0001.keywords.append(add_keyword(self.session, 'first'))
        self.rfc0002.keywords.append(add_keyword(self.session, 'first'))
        self.rfc0002.keywords.append(add_keyword(self.session, 'second'))
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Test rfc0001
        self.rfc0001_query = self.session.query(Rfc).filter_by(id=1).one()
        self.assertEqual(1, len(self.rfc0001_query.keywords))
        self.assertEqual('first', self.rfc0001_query.keywords[0].word)

        # Test rfc0002
        self.rfc0002_query = self.session.query(Rfc).filter_by(id=2).one()
        self.assertEqual(2, len(self.rfc0002_query.keywords))
        self.keywords = []
        for keyword in self.rfc0002_query.keywords:
            self.keywords.append(keyword.word)
        self.assertIn('first', self.keywords)
        self.assertIn('second', self.keywords)

        # Query by 'first' keyword
        self.first_query = self.session.query(Rfc).\
            join(Keyword, Rfc.keywords).\
            filter(Keyword.word == 'first').\
            order_by(Rfc.id).\
            all()
        self.assertEqual(2, len(self.first_query))
        self.assertEqual(self.rfc0001_query, self.first_query[0])
        self.assertEqual(self.rfc0002_query, self.first_query[1])

        # Query by 'second' keyword
        self.second_query = self.session.query(Rfc).\
            join(Keyword, Rfc.keywords).\
            filter(Keyword.word == 'second').\
            order_by(Rfc.id).\
            all()
        self.assertEqual(1, len(self.second_query))
        self.assertEqual(self.rfc0002_query, self.second_query[0])

        # Query by 'third' keyword
        self.third_query = self.session.query(Rfc).\
            join(Keyword, Rfc.keywords).\
            filter(Keyword.word == 'third').\
            order_by(Rfc.id).\
            all()
        self.assertEqual([], self.third_query)

    def test_obsoleted_by(self):
        self.assertEqual(0, len(self.rfc0001.obsoleted_by))  # none added
        self.assertEqual(0, len(self.rfc0002.obsoleted_by))  # none added

        # Add obsoleted_by information to the RFCs
        self.rfc0001.obsoleted_by = [ObsoletedBy(doc_id=1,
                                                 doc_type=DocumentType.RFC)]
        self.rfc0002.obsoleted_by = [ObsoletedBy(doc_id=1,
                                                 doc_type=DocumentType.RFC),
                                     ObsoletedBy(doc_id=2,
                                                 doc_type=DocumentType.STD)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.obsoleted_by))
        self.assertEqual(1, self.rfc0001_query.obsoleted_by[0].id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0001_query.obsoleted_by[0].doc_type)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.obsoleted_by))
        self.assertEqual(1, self.rfc0002_query.obsoleted_by[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0002_query.obsoleted_by[0].doc_type)
        self.assertEqual(2, self.rfc0002_query.obsoleted_by[1].doc_id)
        self.assertEqual(DocumentType.STD,
                         self.rfc0002_query.obsoleted_by[1].doc_type)

    def test_updates(self):
        self.assertEqual(0, len(self.rfc0001.updates))  # none added
        self.assertEqual(0, len(self.rfc0002.updates))  # none added

        # Add updates information to the RFCs
        self.rfc0001.updates = [Updates(doc_id=1, doc_type=DocumentType.RFC)]
        self.rfc0002.updates = [Updates(doc_id=1, doc_type=DocumentType.RFC),
                                Updates(doc_id=2, doc_type=DocumentType.STD)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.updates))
        self.assertEqual(1,
                         self.rfc0001_query.updates[0].id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0001_query.updates[0].doc_type)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.updates))
        self.assertEqual(1,
                         self.rfc0002_query.updates[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0002_query.updates[0].doc_type)
        self.assertEqual(2,
                         self.rfc0002_query.updates[1].doc_id)
        self.assertEqual(DocumentType.STD,
                         self.rfc0002_query.updates[1].doc_type)

    def test_updated_by(self):
        self.assertEqual(0, len(self.rfc0001.updated_by))  # none added
        self.assertEqual(0, len(self.rfc0002.updated_by))  # none added

        # Add updated_by information to the RFCs
        self.rfc0001.updated_by = [UpdatedBy(doc_id=1,
                                             doc_type=DocumentType.RFC)]
        self.rfc0002.updated_by = [UpdatedBy(doc_id=1,
                                             doc_type=DocumentType.RFC),
                                   UpdatedBy(doc_id=2,
                                             doc_type=DocumentType.STD)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.updated_by))
        self.assertEqual(1, self.rfc0001_query.updated_by[0].id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0001_query.updated_by[0].doc_type)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.updated_by))
        self.assertEqual(1, self.rfc0002_query.updated_by[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0002_query.updated_by[0].doc_type)
        self.assertEqual(2, self.rfc0002_query.updated_by[1].doc_id)
        self.assertEqual(DocumentType.STD,
                         self.rfc0002_query.updated_by[1].doc_type)

    def test_is_also(self):
        self.assertEqual(0, len(self.rfc0001.is_also))  # none added
        self.assertEqual(0, len(self.rfc0002.is_also))  # none added

        # Add is_also information to the RFCs
        self.rfc0001.is_also = [IsAlso(doc_id=1, doc_type=DocumentType.RFC)]
        self.rfc0002.is_also = [IsAlso(doc_id=1, doc_type=DocumentType.RFC),
                                IsAlso(doc_id=2, doc_type=DocumentType.STD)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.is_also))
        self.assertEqual(1,
                         self.rfc0001_query.is_also[0].id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0001_query.is_also[0].doc_type)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.is_also))
        self.assertEqual(1,
                         self.rfc0002_query.is_also[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0002_query.is_also[0].doc_type)
        self.assertEqual(2,
                         self.rfc0002_query.is_also[1].doc_id)
        self.assertEqual(DocumentType.STD,
                         self.rfc0002_query.is_also[1].doc_type)

    def test_see_also(self):
        self.assertEqual(0, len(self.rfc0001.see_also))  # none added
        self.assertEqual(0, len(self.rfc0002.see_also))  # none added

        # Add see_also information to the RFCs
        self.rfc0001.see_also = [SeeAlso(doc_id=1, doc_type=DocumentType.RFC)]
        self.rfc0002.see_also = [SeeAlso(doc_id=1, doc_type=DocumentType.RFC),
                                 SeeAlso(doc_id=2, doc_type=DocumentType.STD)]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.see_also))
        self.assertEqual(1,
                         self.rfc0001_query.see_also[0].id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0001_query.see_also[0].doc_type)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.see_also))
        self.assertEqual(1,
                         self.rfc0002_query.see_also[0].doc_id)
        self.assertEqual(DocumentType.RFC,
                         self.rfc0002_query.see_also[0].doc_type)
        self.assertEqual(2,
                         self.rfc0002_query.see_also[1].doc_id)
        self.assertEqual(DocumentType.STD,
                         self.rfc0002_query.see_also[1].doc_type)

    def test_stream(self):
        self.assertEqual(0, len(self.rfc0001.stream))  # none added
        self.assertEqual(0, len(self.rfc0002.stream))  # none added

        # Add stream information to the RFCs
        self.rfc0001.stream = [Stream(StreamEnum['IETF'])]
        self.rfc0002.stream = [Stream(StreamEnum['IETF']),
                               Stream(StreamEnum['LEGACY'])]
        self.session.add(self.rfc0001)  # add the changes made to rfc0001
        self.session.add(self.rfc0002)  # add the changes made to rfc0002
        self.session.commit()  # commit the added changes

        # Get the RFC entries from the DB
        self.rfc0001_query = self.session.query(Rfc).\
            filter_by(id=1).one()
        self.rfc0002_query = self.session.query(Rfc).\
            filter_by(id=2).one()

        # Assertions about rfc0001
        self.assertEqual(1, len(self.rfc0001_query.stream))
        self.assertEqual(StreamEnum['IETF'],
                         self.rfc0001_query.stream[0].stream)

        # Assertions about rfc0002
        self.assertEqual(2, len(self.rfc0002_query.stream))
        self.assertEqual(StreamEnum['IETF'],
                         self.rfc0002_query.stream[0].stream)
        self.assertEqual(StreamEnum['LEGACY'],
                         self.rfc0002_query.stream[1].stream)


if __name__ == '__main__':
    unittest.main()
