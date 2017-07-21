from ietf.sql.bcp import Bcp
from ietf.sql.rfc import IsAlso, Rfc
from ietf.sql.std import Std
from ietf.utility.query_doc import (query_bcp, query_fyi, query_rfc,
                                    query_std,)
from ietf.xml.enum import DocumentType


def query_bcp_is_also(Session, number):
    docs = []  # List of docs to return
    rfcs = Session.query(Rfc).join(IsAlso).\
        filter(IsAlso.doc_type == DocumentType.BCP).\
        filter(IsAlso.doc_id == number).\
        all()  # Returns a list
    docs.extend(rfcs)  # Add rfcs to list
    for rfc in rfcs:
        rfc_aliases = query_rfc_is_also(Session, rfc.id)
        for doc in rfc_aliases:
            if (not isinstance(doc, Bcp)) or (doc.id != number):
                docs.append(doc)
    return docs


def query_rfc_is_also(Session, number):
    """Return aliases for RFC `number`."""
    # Lookup RFC `number`
    rfc = query_rfc(Session, number)
    #
    aliases = []
    if rfc and rfc.is_also:
        for alias in rfc.is_also:
            alias_type = alias.doc_type
            alias_id = alias.doc_id
            if alias_type is DocumentType.RFC:
                aliases.append(query_rfc(Session, alias_id))
            elif alias_type is DocumentType.STD:
                aliases.append(query_std(Session, alias_id))
            elif alias_type is DocumentType.BCP:
                aliases.append(query_bcp(Session, alias_id))
            elif alias_type is DocumentType.FYI:
                aliases.append(query_fyi(Session, alias_id))
            else:
                aliases.append(alias)
    return aliases


def query_std_is_also(Session, number):
    docs = []  # List of docs to return
    rfcs = Session.query(Rfc).join(IsAlso).\
        filter(IsAlso.doc_type == DocumentType.std).\
        filter(IsAlso.doc_id == number).\
        all()  # Returns a list
    docs.extend(rfcs)  # Add rfcs to list
    for rfc in rfcs:
        rfc_aliases = query_rfc_is_also(Session, rfc.id)
        for doc in rfc_aliases:
            if (not isinstance(doc, Std)) or (doc.id != number):
                docs.append(doc)
    return docs
