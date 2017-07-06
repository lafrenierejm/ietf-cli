#!/usr/bin/env python3
from ietf_cli.sql.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


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
