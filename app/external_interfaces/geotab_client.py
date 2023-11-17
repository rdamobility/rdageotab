import logging
from datetime import date
from datetime import datetime
from datetime import time
from typing import List

from mygeotab import API

from ..dtos.device_dto import DeviceDTO

logger = logging.getLogger(__name__)


class GeotabClient():
    def __init__(self, username: str, password: str, database: str) -> None:
        self.database = database
        self.api: API = API(username=username,
                            password=password, database=database)
        self.devices: List[DeviceDTO] = []

    def __is_active(self, device: dict) -> bool:
        return device['activeTo'].isoformat() > datetime.utcnow().isoformat()

    def get_devices(self) -> List[DeviceDTO]:
        logger.debug(f'Getting devices of {self.database}')
        try:
            response = self.api.get('Device')
            self.devices = [DeviceDTO(**item)
                            for item in response if self.__is_active(item)]
            logger.info(f'Getted {len(self.devices)} from {self.database}')
        except Exception as ex:
            logger.error(f'Error getting vehicles of "{self.database}"')
            logger.error(ex.args)

    def _call(self, device_id, date_from, date_to):
        return self.api.call(
            'Get',
            typeName='StatusData',
            search={
                'deviceSearch': {
                    'id': device_id
                },
                'diagnosticSearch': {
                    'id': 'DiagnosticOdometerId'
                },
                'fromDate': date_from,
                'toDate': date_to,
            }
        )

    def __get_odometer_data(self, device_id: str, date_from: datetime, date_to: datetime = None):
        if date_to is None:
            date_to = datetime.now()

        try:
            odometer = self._call(device_id, date_from, date_to)
            last_odometer = odometer[-1]['data']
            last_date = odometer[-1]['dateTime'].isoformat()

            if not (last_date <= date_to.isoformat() and last_date >= date_from.isoformat()):
                last_odometer = None
            return last_odometer, last_date[:10]
        except IndexError:
            logger.warning(
                f'The vehicle "{device_id}" of "{self.database}" has no data of odometer.')
            return None, None

        except Exception as ex:
            logger.error(
                f'Error getting the odometer of vehicle "{device_id}" (DB "{self.database}")')
            logger.error(ex.args)
            return None, None

    def update_devices(self):
        today = datetime.combine(date.today(), time.min)
        for device in self.devices:
            last_odometer, last_date = self.__get_odometer_data(
                device_id=device.id, date_from=today)
            if last_odometer is None:
                logger.warn(f'last odometer for {device.name} is None')
                continue

            device.last_odometer_kms = int(last_odometer/1000)
            device.last_odometer_date = last_date
            logger.info(device.__dict__)

        self.devices = [
            device for device in self.devices if device.last_odometer_kms is not None]

    def __str__(self) -> str:
        return f'Geotab client for DB "{self.database}" with {len(self.devices)} devices saved'
