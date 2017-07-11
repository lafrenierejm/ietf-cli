from ..sql.rfc_not_issued import RfcNotIssued
from .enum import DocumentType
from .parse import findall, find_doc_id, find_title

import sqlalchemy.orm
import xml.etree.ElementTree

def add_all(session: sqlalchemy.orm.session.Session,
            root: xml.etree.ElementTree.Element):
    """Add all rfc-not-issued entries from XML `root` to sqlalchemy
    `session`.
    """

    entries = findall(root, 'rfc-not-issued-entry')
    for entry in entries:
        doc_id = find_doc_id(entry)

        fyi = RfcNotIssued(
            id=doc_id,
        )

        session.add(fyi)
