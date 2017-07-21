from ietf.xml.enum import DocumentType
from ietf.utility.query_doc import (query_bcp, query_fyi, query_rfc,
                                    query_std,)


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
