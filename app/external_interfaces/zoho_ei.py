import json
import logging

import requests

from app.config import constants
from app.config import settings

logger = logging.getLogger(__name__)


class ZohoEI():
    def __init__(self) -> None:
        self.__access_token = None
        self.__client = None
        super().__init__()

    @property
    def client(self):
        if self.__client is None:
            self.__client = requests.Session()
        return self.__client

    @property
    def access_token(self):
        if self.__access_token is None:
            self.__access_token = self._get_access_token()
        return self.__access_token

    def _get_access_token(self) -> str:
        url = constants.ZOHO_API['get_access_token']
        params = {
            'refresh_token': settings.ZOHO_REFRESH_TOKEN,
            'client_id': settings.ZOHO_CLIENT_ID,
            'client_secret': settings.ZOHO_CLIENT_SECRET,
            'grant_type': 'refresh_token',
        }
        response = self.client.post(url, params=params)
        access_token = response.json()['access_token']
        return access_token

    def call_upsert(self, data: list[dict]) -> dict:
        url = constants.ZOHO_API['upsert']  # TODO
        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }

        payload = {
            'data': data,
            'duplicate_check_fields': ['Name', 'Chasis'],
            'trigger': ['workflow'],
        }
        response = self.client.post(
            url=url, data=json.dumps(payload), headers=headers)

        assert response.ok == True

        return response.json()
