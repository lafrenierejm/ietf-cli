#!/usr/bin/env python3
from ietf_cli.sql.author import Author
from ietf_cli.sql.base import Base
from ietf_cli.sql.file_format import FileFormat
from ietf_cli.sql.is_also import IsAlso
from ietf_cli.sql.obsoleted_by import ObsoletedBy
from ietf_cli.sql.obsoletes import Obsoletes
from ietf_cli.sql.updated_by import UpdatedBy
from ietf_cli.sql.updates import Updates
from ietf_cli.xml.enum import Status, Stream
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship


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
    abstract = Column(String)
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