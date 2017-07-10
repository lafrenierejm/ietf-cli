#!/usr/bin/env python3
from .base import Base
from sqlalchemy import Column, Integer, String


class Fyi(Base):
    __tablename__ = 'fyi'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)

    def __repr__(self):
        return "FYI(id={}, title={}".format(
            self.id, self.title)
