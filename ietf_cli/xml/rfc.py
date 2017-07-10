from ..sql.rfc import Abstract, Author, FileFormat, IsAlso, Keyword,\
    ObsoletedBy, Obsoletes, Rfc, SeeAlso, UpdatedBy, Updates
from .enum import DocumentType
from .parse import findall,\
    find_abstract,\
    find_area,\
    find_author,\
    find_current_status,\
    find_date,\
    find_doc_id,\
    find_doi,\
    find_draft,\
    find_errata_url,\
    find_format,\
    find_is_also,\
    find_keywords,\
    find_notes,\
    find_obsoleted_by,\
    find_obsoletes,\
    find_publication_status,\
    find_see_also,\
    find_stream,\
    find_title,\
    find_updated_by,\
    find_updates,\
    find_wg_acronym

import sqlalchemy.orm
import xml.etree.ElementTree

def add_all(session: sqlalchemy.orm.session.Session,
            root: xml.etree.ElementTree.Element):
    """Add all RFC entries from XML `root` to sqlalchemy `session`."""

    entries = findall(root, 'rfc-entry')
    for entry in entries:
        doc_id = find_doc_id(entry)
        title = find_title(entry)
        authors = find_author(entry)
        year, month, day = find_date(entry)
        formats = find_format(entry)
        keywords = find_keywords(entry)
        abstract_pars = find_abstract(entry)
        draft = find_draft(entry)
        notes = find_notes(entry)
        obsoletes = find_obsoletes(entry)
        obsoleted_by = find_obsoleted_by(entry)
        updates = find_updates(entry)
        updated_by = find_updated_by(entry)
        is_also = find_is_also(entry)
        see_also = find_see_also(entry)
        cur_status = find_current_status(entry)
        pub_status = find_publication_status(entry)
        stream = find_stream(entry)
        area = find_area(entry)
        wg = find_wg_acronym(entry)
        errata = find_errata_url(entry)
        doi = find_doi(entry)

        rfc = Rfc(
            # Create the Rfc object with its single-column values set
            id=doc_id,
            title=title,
            date_year=year, date_month=month, date_day=day,
            draft=draft,
            notes=notes,
            current_status=cur_status,
            publication_status=pub_status,
            stream=stream,
            area=area,
            wg_acronym=wg,
            errata_url=errata,
            doi=doi,
        )
        for author in authors:
            # Add authors to rfc
            rfc.authors.append(Author(name=author['name'],
                                      title=author['title'],
                                      organization=author['organization'],
                                      org_abbrev=author['org_abbrev']))
        for entry in formats:
            # Add formats to rfc
            filetype, char_count, page_count = entry
            rfc.formats.append(FileFormat(filetype=filetype,
                                          char_count=char_count,
                                          page_count=page_count))
        for keyword in keywords:
            # Add keywords to rfc
            rfc.keywords.append(Keyword(word=keyword))
        for par in abstract_pars:
            # Add abstract to rfc
            rfc.abstract.append(Abstract(par=par))
        for doc in obsoletes:
            # Add obsoletes to rfc
            doc_type, doc_id = doc
            rfc.obsoletes.append(Obsoletes(doc_id=doc_id, doc_type=doc_type))
        for doc in obsoleted_by:
            # Add obsoleted_by to rfc
            doc_type, doc_id = doc
            rfc.obsoleted_by.append(ObsoletedBy(doc_id=doc_id, doc_type=doc_type))
        for doc in updates:
            # Add updates to rfc
            doc_type, doc_id = doc
            rfc.updates.append(Updates(doc_id=doc_id, doc_type=doc_type))
        for doc in updated_by:
            # Add updated_by to rfc
            doc_type, doc_id = doc
            rfc.updated_by.append(UpdatedBy(doc_id=doc_id, doc_type=doc_type))
        for doc in is_also:
            # Add is_also to rfc
            doc_type, doc_id = doc
            rfc.is_also.append(IsAlso(doc_id=doc_id, doc_type=doc_type))
        for doc in see_also:
            # Add see_also to rfc
            doc_type, doc_id = doc
            rfc.see_also.append(SeeAlso(doc_id=doc_id, doc_type=doc_type))

        session.add(rfc)
