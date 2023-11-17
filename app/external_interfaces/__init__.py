from ..config import settings
from .geotab_client import GeotabClient
from .zoho_ei import ZohoEI

# ARG
rdamobility_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.RDAMOBILITY_DB_NAME,
)
syngenta_agro_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.SYNGENTA_AGRO_DB_NAME,
)
stefanini_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.STEFANINI_DB_NAME,
)
schneider_electric_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.SCHNEIDER_ELECTRIC_DB_NAME,
)
agidea_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.AGIDEA_DB_NAME,
)
ferring_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.FERRING_DB_NAME,
)

# COL
grancolombianagold_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.GRANCOLOMBIANAGOLD_DB_NAME,
)
rehinland_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.REHINLAND_DB_NAME,
)
avevacol_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.AVEVACOL_DB_NAME,
)
proyectourcol_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.PROYECTOURCOL_DB_NAME,
)
indracol_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.INDRACOL_DB_NAME,
)
vozikcol_client = GeotabClient(
    username=settings.GEOTAB_USER,
    password=settings.GEOTAB_PASS,
    database=settings.VOZIKCOL_DB_NAME,
)


zoho_client = ZohoEI()
