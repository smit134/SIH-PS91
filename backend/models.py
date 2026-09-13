"""Backward-compatibility bridge for models.py."""

from app.models.evidence import EvidenceModel as Evidence
from app.models.evidence import *
from app.models.scheme import GovernmentScheme
from app.models.user import User, Profile
from app.models.document_chunk import SchemeDocumentChunk
from app.models.district_stats import DistrictMSMEStats
from app.models.osm_poi import OSMPointOfInterest
