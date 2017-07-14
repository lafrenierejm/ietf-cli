#!/usr/bin/env python3
from ietf.utility.environment import get_db_path
from ietf.sql.base import Base
from ietf.xml.enum import DocumentType
from ietf.sql.bcp import Bcp
from ietf.sql.fyi import Fyi
from ietf.sql.rfc import Rfc
from ietf.sql.std import Std
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_session():
    """Return a DB session."""
    db_path = get_db_path()
    engine = create_engine("sqlite:///{}".format(db_path))
    Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)()
    return session


def query_rfc(session, number):
    row = session.query(Rfc).\
                  filter(Rfc.id == number).\
                  one_or_none()
    return row


def query_bcp(session, number):
    row = session.query(Bcp).\
                  filter(Bcp.id == number).\
                  one_or_none()
    return row


def query_fyi(session, number):
    row = session.query(Fyi).\
                  filter(Fyi.id == number).\
                  one_or_none()
    return row
