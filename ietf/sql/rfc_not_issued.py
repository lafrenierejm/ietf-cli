#!/usr/bin/env python3
from ietf.sql.base import Base
from sqlalchemy import Column, Integer


class RfcNotIssued(Base):
    __tablename__ = 'rfc_not_issued'

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "RFC not issued(id={})".format(self.id)
