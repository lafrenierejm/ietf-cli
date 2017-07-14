#!/usr/bin/env python3
from ietf.sql.base import Base
from sqlalchemy import Column, Integer, String


class Std(Base):
    __tablename__ = 'std'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    def __repr__(self):
        # `{:<18}` left-aligns in 18 columns
        fmt = "{:<18} : {}"
        # `{:0>4}` right-aligns in 4 columns with leading 0
        repr_str = fmt.format('STD', "{:0>4}".format(self.id))
        repr_str += '\n'
        repr_str += fmt.format('Title', self.title)

        return repr_str
