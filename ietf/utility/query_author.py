#!/usr/bin/env python3
from ietf.sql.rfc import Author, Rfc
from string import ascii_uppercase


def _has_capital(the_string):
    """Return whether or not there is a capital letter in `the_string`."""
    if any(char in ascii_uppercase for char in the_string):
        return True
    else:
        return False


def query_author_by_name(Session, names):
    """Return a query that, if run, would return RFCs whose authors match every
    string in `names`.

    The matching on `names` is case-insensitive.  Asterisks (*) in passed names
    are replaced with percent signs (%) to function as wildcards in the actual
    SQL query.
    """
    # Assemble a query for each name
    queries = []  # Empty list to store queries
    for name in names:
        name = name.replace('*', '%')  # Substitute wildcard character
        # Attempt an exact search
        query = Session.query(Rfc).join(Author).filter(Author.name == name)
        if query.first():  # If that returns something, add the query
            queries.append(query)
        else:  # Otherwise add a case-insensitive query
            queries.append(
                Session.query(Rfc).join(Author).
                filter(Author.name.ilike(name))
            )
    # Build a query of intersections
    query_to_run = queries[0]  # Assign first query
    for query in queries[1:]:  # Start at second element in list
        query_to_run = query_to_run.intersect(query)
    # Return the built query
    return query_to_run


def query_author_by_org(Session, orgs):
    """Return a query that, if run, would return all RFCs whose authors'
    organizations match every string in `orgs`.

    The matching on `orgs` is case-insensitive.  Asterisks (*) in passed orgs
    are replaced with percent signs (%) to function as wildcards in the actual
    SQL query.
    """
    # Assemble a query for each org
    queries = []  # Empty list to store queries
    for org in orgs:
        org = org.replace('*', '%')  # Substitute wildcard character
        # Attempt an exact search
        query = Session.query(Rfc).join(Author).\
            filter(Author.organization == org)
        if query.first():  # If that returns something, add the query
            queries.append(query)
        else:  # Otherwise add a case-insensitive query
            queries.append(
                Session.query(Rfc).join(Author).
                filter(Author.organization.ilike(org))
            )
    # Build a query of intersections
    query_to_run = queries[0]  # Assign first query
    for query in queries[1:]:  # Start at second element in list
        query_to_run = query_to_run.intersect(query)
    # Return the built query
    return query_to_run


def query_author_by_orgabbrev(Session, abbrevs):
    """Return a query that, if run, would return all RFCs whose authors'
    abbreviations match every string in `abbrevs`.

    The matching on `abbrevs` is case-insensitive.  Asterisks (*) in passed
    abbreviations are replaced with percent signs (%) to function as wildcards
    in the actual SQL query.
    """
    # Assemble a query for each abbrev
    queries = []  # Empty list to store queries
    for abbrev in abbrevs:
        abbrev = abbrev.replace('*', '%')  # Substitute wildcard character
        # Attempt an exact search
        query = Session.query(Rfc).join(Author).\
            filter(Author.org_abbrev == abbrev)
        if query.first():  # If that returns something, add the query
            queries.append(query)
        else:  # Otherwise add a case-insensitive query
            queries.append(
                Session.query(Rfc).join(Author).
                filter(Author.org_abbrev.ilike(abbrev))
            )
    # Build a query of intersections
    query_to_run = queries[0]  # Assign first query
    for query in queries[1:]:  # Start at second element in list
        query_to_run = query_to_run.intersect(query)
    # Return the built query
    return query_to_run


def query_author_by_title(Session, titles):
    """Return a query that, if run, would return all RFCs whose authors' titles
    match every string in `titles`.

    The matching on `titles` is case-insensitive.  Asterisks (*) in passed
    titles are replaced with percent signs (%) to function as wildcards in the
    actual SQL query.
    """
    # Assemble a query for each title
    queries = []  # Empty list to store queries
    for title in titles:
        title = title.replace('*', '%')  # Substitute wildcard character
        # Attempt an exact search
        query = Session.query(Rfc).join(Author).filter(Author.title == title)
        if query.first():  # If that returns something, add the query
            queries.append(query)
        else:  # Otherwise add a case-insensitive query
            queries.append(
                Session.query(Rfc).join(Author).
                filter(Author.title.ilike(title))
            )
    # Build a query of intersections
    query_to_run = queries[0]  # Assign first query
    for query in queries[1:]:  # Start at second element in list
        query_to_run = query_to_run.intersect(query)
    # Return the built query
    return query_to_run
