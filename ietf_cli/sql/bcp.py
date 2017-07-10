#!/usr/bin/env python3
from .base import Base
from sqlalchemy import Column, Integer, String


class Bcp(Base):
    __tablename__ = 'bcp'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)

    def __repr__(self):
        return "BCP(id={}, title={}".format(
            self.id, self.title)
