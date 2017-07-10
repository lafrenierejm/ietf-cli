from ..sql.fyi import Fyi
from .enum import DocumentType
from .parse import findall, find_doc_id, find_title

import sqlalchemy.orm
import xml.etree.ElementTree

def add_all(session: sqlalchemy.orm.session.Session,
            root: xml.etree.ElementTree.Element):
    """Add all FYI entries from XML `root` to sqlalchemy `session`."""

    entries = findall(root, 'fyi-entry')
    for entry in entries:
        doc_id = find_doc_id(entry)
        title = find_title(entry)

        fyi = Fyi(
            # Create the Fyi object with its single-column values set
            id=doc_id,
            title=title,
        )

        session.add(fyi)
