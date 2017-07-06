#!/usr/bin/env python3
from ietf_cli.sql.base import Base
from ietf_cli.xml.enum import DocumentType
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


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
