import sqlalchemy.orm
import xml.etree.ElementTree
from ietf.sql.rfc import (Abstract, Author, FileFormat, IsAlso, Keyword,
                          ObsoletedBy, Obsoletes, Rfc, SeeAlso, UpdatedBy,
                          Updates)
import ietf.xml.parse as parse


def _add_keyword(session: sqlalchemy.orm.session.Session,
                 word: str,
                 ) -> Keyword:
    """Create Keyword instances without violating uniqueness restraint."""
    keyword = session.query(Keyword).filter(Keyword.word == word).one_or_none()
    if keyword is None:
        keyword = Keyword(word)
        session.add(keyword)
    return keyword


def add_all(session: sqlalchemy.orm.session.Session,
            root: xml.etree.ElementTree.Element):
    """Add all RFC entries from XML `root` to sqlalchemy `session`."""

    entries = parse.findall(root, 'rfc-entry')
    for entry in entries:
        doc_id = parse.find_doc_id(entry)
        title = parse.find_title(entry)
        authors = parse.find_author(entry)
        year, month, day = parse.find_date(entry)
        formats = parse.find_format(entry)
        keywords = parse.find_keywords(entry)
        abstract_pars = parse.find_abstract(entry)
        draft = parse.find_draft(entry)
        notes = parse.find_notes(entry)
        obsoletes = parse.find_obsoletes(entry)
        obsoleted_by = parse.find_obsoleted_by(entry)
        updates = parse.find_updates(entry)
        updated_by = parse.find_updated_by(entry)
        is_also = parse.find_is_also(entry)
        see_also = parse.find_see_also(entry)
        cur_status = parse.find_current_status(entry)
        pub_status = parse.find_publication_status(entry)
        stream = parse.find_stream(entry)
        area = parse.find_area(entry)
        wg = parse.find_wg_acronym(entry)
        errata = parse.find_errata_url(entry)
        doi = parse.find_doi(entry)

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
        for word in keywords:
            # Add keywords to rfc
            keyword = _add_keyword(session, word)
            rfc.keywords.append(keyword)
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
            rfc.obsoleted_by.append(ObsoletedBy(doc_id=doc_id,
                                                doc_type=doc_type))
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
