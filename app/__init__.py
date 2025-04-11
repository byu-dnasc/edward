import os
import abc
import sys
import dotenv

CONFIG_FILE = '.env'
if 'pytest' in sys.modules:
    CONFIG_FILE = 'tests/.env'

if not os.path.exists(CONFIG_FILE):
    raise ImportError(f'Config file {CONFIG_FILE} not found.')

dotenv.load_dotenv(CONFIG_FILE)
    
try:
    GLOBUS_CLIENT_ID = os.environ.get('GLOBUS_CLIENT_ID')
    GLOBUS_CLIENT_SECRET = os.environ.get('GLOBUS_CLIENT_SECRET')
    GLOBUS_COLLECTION_ID = os.environ.get('GLOBUS_COLLECTION_ID')
    SMRTLINK_HOST = os.environ.get('SMRTLINK_HOST')
    SMRTLINK_PORT = os.environ.get('SMRTLINK_PORT')
    SMRTLINK_USER = os.environ.get('SMRTLINK_USER')
    SMRTLINK_PASS = os.environ.get('SMRTLINK_PASS')
    DB_PATH = os.environ.get('DB_PATH')
    GROUP_NAME = os.environ.get('GROUP_NAME')
    APP_USER = os.environ.get('APP_USER')
    GLOBUS_PERMISSION_DAYS = os.environ.get('GLOBUS_PERMISSION_DAYS')
    STAGING_ROOT = os.environ.get('STAGING_ROOT')
except KeyError as e:
    raise ImportError(f"Variable {e} not found in .env file.")

class BaseProject(abc.ABC):

    @property
    def id(self) -> int:
        return self._id

    @property
    def datasets(self) -> dict:
        return self._datasets

    @property
    def members(self) -> list[str]:
        return self._members