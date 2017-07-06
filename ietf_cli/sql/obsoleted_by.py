#!/usr/bin/env python3
from ietf_cli.sql.base import Base
from ietf_cli.xml.enum import DocumentType
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


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
