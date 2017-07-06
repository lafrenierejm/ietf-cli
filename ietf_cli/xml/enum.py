#!/usr/bin/env python3
import enum


@enum.unique
class DocumentType(enum.Enum):
    RFC = 'RFC'
    STD = 'STD'
    BCP = 'BCP'
    FYI = 'FYI'
    NIC = 'NIC'
    IEN = 'IEN'
    RTR = 'RTR'


@enum.unique
class FileType(enum.Enum):
    ASCII = 'ASCII'
    PS = 'PS'
    PDF = 'PDF'
    TGZ = 'TGZ'


@enum.unique
class Status(enum.Enum):
    """The possible values for current_status and publication_status.

    The values are defined in RFC2026.
    """
    PROPOSED_STANDARD = 'PROPOSED STANDARD'
    DRAFT_STANDARD = 'DRAFT STANDARD'
    INTERNET_STANDARD = 'INTERNET STANDARD'
    INFORMATIONAL = 'INFORMATIONAL'
    EXPERIMENTAL = 'EXPERIMENTAL'
    BEST_CURRENT_PRACTICE = 'BEST CURRENT PRACTICE'
    HISTORIC = 'HISTORIC'
    UNKNOWN = 'UNKNOWN'


@enum.unique
class Month(enum.Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


@enum.unique
class Stream(enum.Enum):
    IETF = 'IETF'
    IAB = 'IAB'
    IRTF = 'IRTF'
    INDEPENDENT = 'INDEPENDENT'
    LEGACY = 'Legacy'
