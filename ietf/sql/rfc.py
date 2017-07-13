#!/usr/bin/env python3
from ietf.sql.base import Base
from ietf.xml.enum import DocumentType, FileType, Status, Stream
from sqlalchemy import (BigInteger, Column, Enum, ForeignKey, Integer, String,
                        Table,)
from sqlalchemy.orm import relationship


class Abstract(Base):
    __tablename__ = 'abstract'

    id = Column(Integer, primary_key=True)
    par = Column(String, nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='abstract')

    def __repr__(self):
        # 79 - (18 + 3) - 3 = 55
        # 79 to adhere to 80 column width
        # -(18 + 3) from Rfc.__repr__.fmt
        # -3 from ellipses
        return "{}...".format(self.par[:55])


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # no `minOccurs` in XSD
    title = Column(String)
    organization = Column(String)
    org_abbrev = Column(String)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='authors')

    def __repr__(self):
        """String representation of object."""
        representation = self.name
        if self.title:
            representation += ', ' + self.title
        if self.organization:
            representation += ', ' + self.organization
        if self.org_abbrev:
            representation += ', ' + self.org_abbrev
        return representation


class FileFormat(Base):
    __tablename__ = 'format'

    id = Column(Integer, primary_key=True)
    filetype = Column(Enum(FileType), nullable=False)
    char_count = Column(BigInteger, nullable=False)
    page_count = Column(Integer)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='formats')

    def __repr__(self):
        representation = "filetype={}, char count={}".\
            format(self.filetype.value, self.char_count)
        if self.page_count:
            representation += ", page count=" + str(self.page_count)
        return representation


class IsAlso(Base):
    __tablename__ = 'is_also'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='is_also')

    def __repr__(self):
        return "{} {}".format(self.doc_type.value, self.doc_id)


rfc_keyword = Table(
    # Used for many-to-many mapping between Rfc and Keyword
    'rfc_keyword',
    Base.metadata,
    Column('rfc_id', ForeignKey('rfc.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keyword.id'), primary_key=True)
)


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False, unique=True)
    rfcs = relationship(
        'Rfc',
        secondary=rfc_keyword,
        back_populates='keywords',
    )

    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return self.word


class ObsoletedBy(Base):
    __tablename__ = 'obsoleted_by'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='obsoleted_by')

    def __repr__(self):
        return "{} {}".format(self.doc_type.value, self.doc_id)


class Obsoletes(Base):
    __tablename__ = 'obsoletes'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='obsoletes')

    def __repr__(self):
        return "{} {}".format(self.doc_type.value, self.doc_id)


class SeeAlso(Base):
    __tablename__ = 'see_also'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='see_also')

    def __repr__(self):
        return "{} {}".format(self.doc_type.value, self.doc_id)


class Stream(Base):
    __tablename__ = 'stream'

    id = Column(Integer, primary_key=True)
    stream = Column(Enum(Stream), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='stream')

    def __init__(self, stream):
        self.stream = stream

    def __repr__(self):
        return self.stream.value


class UpdatedBy(Base):
    __tablename__ = 'updated_by'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='updated_by')

    def __repr__(self):
        return "{} {}".format(self.doc_type.value, self.doc_id)


class Updates(Base):
    __tablename__ = 'updates'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='updates')

    def __repr__(self):
        return "{} {}".format(self.doc_type.value, self.doc_id)


class Rfc(Base):
    __tablename__ = 'rfc'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authors = relationship('Author', order_by=Author.id,
                           back_populates='rfc')
    date_day = Column(Integer)
    date_month = Column(Integer, nullable=False)
    date_year = Column(Integer, nullable=False)
    formats = relationship('FileFormat', order_by=FileFormat.id,
                           back_populates='rfc')
    keywords = relationship('Keyword', secondary=rfc_keyword,
                            back_populates='rfcs')
    abstract = relationship('Abstract', order_by=Abstract.id,
                            back_populates='rfc')
    draft = Column(String)
    notes = Column(String)
    obsoletes = relationship('Obsoletes', order_by=Obsoletes.id,
                             back_populates='rfc')
    obsoleted_by = relationship('ObsoletedBy', order_by=ObsoletedBy.id,
                                back_populates='rfc')
    updates = relationship('Updates', order_by=Updates.id,
                           back_populates='rfc')
    updated_by = relationship('UpdatedBy', order_by=UpdatedBy.id,
                              back_populates='rfc')
    is_also = relationship('IsAlso', order_by=IsAlso.id, back_populates='rfc')
    see_also = relationship('SeeAlso', order_by=SeeAlso.id,
                            back_populates='rfc')
    current_status = Column(Enum(Status), nullable=False)
    publication_status = Column(Enum(Status), nullable=False)
    stream = relationship('Stream', order_by=Stream.id,
                          back_populates='rfc')
    area = Column(String)
    wg_acronym = Column(String)
    errata_url = Column(String)
    doi = Column(String)

    def __repr__(self):
        """String representation of Rfc instances."""

        # First string is left-aligned with a width of 18
        fmt = "{:<18} : {}"

        id_str = fmt.format('RFC', "{:0>4}".format(self.id))
        title_str = fmt.format('Title', self.title)

        author_strs = []
        for row in self.authors:
            author_strs.append(fmt.format('Author', row.__repr__()))

        if self.date_day:
            date_str = fmt.format(
                'Date',
                "{:0>4}-{:0>2}-{:0>2}".format(self.date_year,
                                              self.date_month,
                                              self.date_day)
            )
        else:
            date_str = fmt.format(
                'Date',
                "{:0>4}-{:0>2}".format(self.date_year,
                                       self.date_month)
            )

        format_strs = []
        if self.formats:
            for row in self.formats:
                format_strs.append(fmt.format('Format', row.__repr__()))

        keyword_strs = []
        if self.keywords:
            for row in self.keywords:
                keyword_strs.append(fmt.format('Keyword', row.__repr__()))

        abstract_strs = []
        if self.abstract:
            for row in self.abstract:
                abstract_strs.append(fmt.format('Abstract', row.__repr__()))

        notes_strs = []
        if self.notes:
            for row in self.notes:
                notes_strs.append(fmt.format('Note', row.__repr__()))

        obsoletes_strs = []
        if self.obsoletes:
            for row in self.obsoletes:
                obsoletes_strs.append(fmt.format('Obsoletes', row.__repr__()))

        obsoleted_by_strs = []
        if self.obsoleted_by:
            for row in self.obsoleted_by:
                obsoleted_by_strs.append(fmt.format('Obsoleted By',
                                                    row.__repr__()))

        updates_strs = []
        if self.updates:
            for row in self.updates:
                updates_strs.append(fmt.format('Updates', row.__repr__()))

        updated_by_strs = []
        if self.updated_by:
            for row in self.updated_by:
                updated_by_strs.append(fmt.format('Updated By',
                                                  row.__repr__()))

        is_also_strs = []
        if self.is_also:
            for row in self.is_also:
                is_also_strs.append(fmt.format('Is Also', row.__repr__()))

        see_also_strs = []
        if self.see_also:
            for row in self.see_also:
                see_also_strs.append(fmt.format('See Also', row.__repr__()))

        current_status_str = fmt.format('Current Status',
                                        self.current_status.value)
        publication_status_str = fmt.format('Publication Status',
                                            self.publication_status.value)

        stream_strs = []
        if self.stream:
            for row in self.stream:
                stream_strs.append(fmt.format('Stream', row.__repr__()))

        if self.area:
            area_str = fmt.format('Area', self.area)
        if self.wg_acronym:
            wg_str = fmt.format('WG Acronym', self.wg_acronym)
        if self.errata_url:
            errata_str = fmt.format('Errata URL', self.errata_url)
        if self.doi:
            doi_str = fmt.format('DOI', self.doi)

        # Assemble a list of the defined strings
        list_repr = [id_str, title_str]
        list_repr.extend(author_strs)
        list_repr.append(date_str)
        list_repr.extend(format_strs)
        list_repr.extend(keyword_strs)
        list_repr.extend(abstract_strs)
        list_repr.extend(notes_strs)
        list_repr.extend(obsoletes_strs)
        list_repr.extend(obsoleted_by_strs)
        list_repr.extend(updates_strs)
        list_repr.extend(updated_by_strs)
        list_repr.extend(is_also_strs)
        list_repr.extend(see_also_strs)
        list_repr.append(current_status_str)
        list_repr.append(publication_status_str)
        list_repr.extend(stream_strs)
        if 'area_str' in vars():
            list_repr.append(area_str)
        if 'wg_str' in vars():
            list_repr.append(wg_str)
        if 'errata_str' in vars():
            list_repr.append(errata_str)
        if 'doi_str' in vars():
            list_repr.append(doi_str)

        # Return a string of list_repr's elements joined using newlines
        return '\n'.join(list_repr)
