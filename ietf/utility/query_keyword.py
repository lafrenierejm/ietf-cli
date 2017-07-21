#!/usr/bin/env python3
from ietf.sql.rfc import Rfc


def query_rfc_by_keyword(Session, search_terms):
    """Return a query that, if run, would return RFCs with the keywords in
    `keywords`.

    The matching on is case-insensitive.
    """
    # Assemble a query for each name
    queries = []  # Empty list to store queries
    for term in search_terms:
        term = term.lower()  # Convert to lowercase
        queries.append(Session.query(Rfc).filter(Rfc.keywords.any(word=term)))
    # Build a query of intersections
    query_to_run = queries[0]  # Assign first query
    for query in queries[1:]:  # Start at second element in list
        query_to_run = query_to_run.intersect(query)
    # Return the built query
    return query_to_run
