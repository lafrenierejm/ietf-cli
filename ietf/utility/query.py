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


def query_rfc_by_updates(session, number):
    """Return the most up-to-date document for RFC `number`."""
    orig = query_rfc(session, number)
    # If there are no updates then return the original
    if (orig is None) or (not orig.updated_by):
        return orig
    # Else return the latest document
    else:
        update_doc = orig.updated_by[-1]
        update_type = update_doc.doc_type
        update_id = update_doc.doc_id
        if update_type is DocumentType.RFC:
            return query_rfc(session, update_id)
        elif update_type is DocumentType.STD:
            return query_std(session, update_id)
        elif update_type is DocumentType.BCP:
            return query_bcp(session, update_id)
        elif update_type is DocumentType.FYI:
            return query_fyi(session, update_id)
        else:
            return orig


def query_rfc_by_obsoletes(session, number):
    """Return the latest RFC that obsoletes `number` if such an RFC exists,
    otherwise return RFC `number`."""
    # Lookup RFC `number`
    cur_rfc = query_rfc(session, number)
    # If there is no updated_by then return the original
    if (cur_rfc is None) or (not cur_rfc.obsoleted_by):
        return cur_rfc
    # Else recurse
    else:
        obsoleting_id = cur_rfc.obsoleted_by[-1].doc_id
        return query_rfc_by_obsoletes(session, obsoleting_id)


def query_std(session, number):
    row = session.query(Std).\
                  filter(Std.id == number).\
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
