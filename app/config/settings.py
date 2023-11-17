import logging
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
# Logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG') == '1' else logging.INFO,
    filemode='a',
    filename='./logs/{}'.format(datetime.now().strftime('%Y%m%d_rda_geotab.log')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


# ENV
# Geotab Auth Credentials
GEOTAB_USER = os.getenv('GEOTAB_USER')
GEOTAB_PASS = os.getenv('GEOTAB_PASS')

# Geotab Databases
RDAMOBILITY_DB_NAME = os.getenv('RDAMOBILITY_DB_NAME')
SYNGENTA_AGRO_DB_NAME = os.getenv('SYNGENTA_AGRO_DB_NAME')
STEFANINI_DB_NAME = os.getenv('STEFANINI_DB_NAME')
SCHNEIDER_ELECTRIC_DB_NAME = os.getenv('SCHNEIDER_ELECTRIC_DB_NAME')
AGIDEA_DB_NAME = os.getenv('AGIDEA_DB_NAME')
FERRING_DB_NAME = os.getenv('FERRING_DB_NAME')

GRANCOLOMBIANAGOLD_DB_NAME = os.getenv('GRANCOLOMBIANAGOLD_DB_NAME')
REHINLAND_DB_NAME = os.getenv('REHINLAND_DB_NAME')
AVEVACOL_DB_NAME = os.getenv('AVEVACOL_DB_NAME')
PROYECTOURCOL_DB_NAME = os.getenv('PROYECTOURCOL_DB_NAME')
INDRACOL_DB_NAME = os.getenv('INDRACOL_DB_NAME')
VOZIKCOL_DB_NAME = os.getenv('VOZIKCOL_DB_NAME')

# Zoho Credentials
ZOHO_CLIENT_ID = os.getenv('ZOHO_CLIENT_ID')
ZOHO_CLIENT_SECRET = os.getenv('ZOHO_CLIENT_SECRET')
ZOHO_REFRESH_TOKEN = os.getenv('ZOHO_REFRESH_TOKEN')
