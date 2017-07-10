#!/usr/bin/env python3
from ietf_cli.sql.base import Base
from ietf_cli.xml.enum import DocumentType, FileType, Status, Stream
from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Abstract(Base):
    __tablename__ = 'abstract'

    id = Column(Integer, primary_key=True)
    par = Column(String, nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='abstract')

    def __repr__(self):
        return "<Abstract(first_10_chars='%s')>" % self.par[0:10]


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
        return "<Author(name='%s')>" % self.name


class FileFormat(Base):
    __tablename__ = 'format'

    id = Column(Integer, primary_key=True)
    filetype = Column(Enum(FileType), nullable=False)
    char_count = Column(BigInteger, nullable=False)
    page_count = Column(Integer)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='formats')

    def __repr__(self):
        return "<Format(filetype='%s', char_count='%d', page_count='%d',"\
            "rfc_id='%s')>" % (self.filetype.value, self.char_count,
                               self.page_count, self.rfc_id)


class IsAlso(Base):
    __tablename__ = 'is_also'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='is_also')

    def __repr__(self):
        return "<IsAlso(id='%s %d', host='%d')>" % (self.doc_type.value,
                                                    self.id, self.rfc_id)


class ObsoletedBy(Base):
    __tablename__ = 'obsoleted_by'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='obsoleted_by')

    def __repr__(self):
        return "<ObsoletedBy(id='%s %d', obsoleted='%d')>"\
            % (self.doc_type.value, self.id, self.rfc_id)


class Obsoletes(Base):
    __tablename__ = 'obsoletes'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='obsoletes')

    def __repr__(self):
        return "<Obsoletes(id='%s %d', obsoleting id='%d')>"\
            % (self.doc_type.value, self.id, self.rfc_id)


class SeeAlso(Base):
    __tablename__ = 'see_also'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='see_also')

    def __repr__(self):
        return "<SeeAlso(id='%s %d', host='%d')>"\
            % (self.doc_type.value, self.id, self.rfc_id)


class UpdatedBy(Base):
    __tablename__ = 'updated_by'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='updated_by')

    def __repr__(self):
        return "<UpdatedBy(id='%s %d', updated='%d')>"\
            % (self.doc_type.value, self.id, self.rfc_id)


class Updates(Base):
    __tablename__ = 'updates'

    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    rfc_id = Column(Integer, ForeignKey('rfc.id'))

    rfc = relationship('Rfc', back_populates='updates')

    def __repr__(self):
        return "<Updates(id='%s %d', updated by='%d')>"\
            % (self.doc_type.value, self.id, self.rfc_id)


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
    keywords = Column(String)
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
    stream = Column(Enum(Stream))
    area = Column(String)
    wg_acronym = Column(String)
    errata_url = Column(String)
    doi = Column(String)

    def __repr__(self):
        return "RfcEntry(id=rfc{}, title={}".format(
            self.id, self.title)
