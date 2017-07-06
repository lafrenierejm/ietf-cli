#!/usr/bin/env python3
from ietf_cli.sql.base import Base
from ietf_cli.xml.enum import FileType
from sqlalchemy import BigInteger, Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


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
