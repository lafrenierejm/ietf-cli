#!/usr/bin/env python3
from ietf.sql.base import Base
from sqlalchemy import Column, Integer, String


class Std(Base):
    __tablename__ = 'std'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    def __repr__(self):
        return "StdEntry(id=STD{}, title={}".format(
            self.id, self.title)
