#!/usr/bin/env python3
from ietf_cli.sql.base import Base
from ietf_cli.xml.enum import DocumentType
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


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
