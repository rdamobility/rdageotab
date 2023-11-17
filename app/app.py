import logging
from threading import Thread
from typing import List

from . import external_interfaces as repo
from .config import constants
from .dtos.device_dto import DeviceDTO

logger = logging.getLogger(__name__)


def get_devices_by_db():
    # Init threads
    schneider_electric__thread = Thread(
        target=repo.schneider_electric_client.get_devices)
    rdamobility__thread = Thread(target=repo.rdamobility_client.get_devices)
    syngenta_agro__thread = Thread(
        target=repo.syngenta_agro_client.get_devices)
    stefanini__thread = Thread(target=repo.stefanini_client.get_devices)
    agidea__thread = Thread(target=repo.agidea_client.get_devices)
    ferring__thread = Thread(target=repo.ferring_client.get_devices)

    grancolombianagold_client__thread = Thread(target=repo.grancolombianagold_client.get_devices)
    rehinland_client__thread = Thread(target=repo.rehinland_client.get_devices)
    avevacol_client__thread = Thread(target=repo.avevacol_client.get_devices)
    proyectourcol_client__thread = Thread(target=repo.proyectourcol_client.get_devices)
    indracol_client__thread = Thread(target=repo.indracol_client.get_devices)
    vozikcol_client__thread = Thread(target=repo.vozikcol_client.get_devices)

    # Start threads
    schneider_electric__thread.start()
    rdamobility__thread.start()
    syngenta_agro__thread.start()
    stefanini__thread.start()
    agidea__thread.start()
    ferring__thread.start()

    grancolombianagold_client__thread.start()
    rehinland_client__thread.start()
    avevacol_client__thread.start()
    proyectourcol_client__thread.start()
    indracol_client__thread.start()
    vozikcol_client__thread.start()

    # Join threads
    schneider_electric__thread.join()
    rdamobility__thread.join()
    syngenta_agro__thread.join()
    stefanini__thread.join()
    agidea__thread.join()
    ferring__thread.join()

    grancolombianagold_client__thread.join()
    rehinland_client__thread.join()
    avevacol_client__thread.join()
    proyectourcol_client__thread.join()
    indracol_client__thread.join()
    vozikcol_client__thread.join()


def update_devices_by_db():
    # Init threads
    schneider_electric__thread = Thread(
        target=repo.schneider_electric_client.update_devices)
    rdamobility__thread = Thread(target=repo.rdamobility_client.update_devices)
    syngenta_agro__thread = Thread(
        target=repo.syngenta_agro_client.update_devices)
    stefanini__thread = Thread(target=repo.stefanini_client.update_devices)
    agidea__thread = Thread(target=repo.agidea_client.update_devices)
    ferring__thread = Thread(target=repo.ferring_client.update_devices)

    grancolombianagold_client__thread = Thread(target=repo.grancolombianagold_client.update_devices)
    rehinland_client__thread = Thread(target=repo.rehinland_client.update_devices)
    avevacol_client__thread = Thread(target=repo.avevacol_client.update_devices)
    proyectourcol_client__thread = Thread(target=repo.proyectourcol_client.update_devices)
    indracol_client__thread = Thread(target=repo.indracol_client.update_devices)
    vozikcol_client__thread = Thread(target=repo.vozikcol_client.update_devices)

    # Start threads
    schneider_electric__thread.start()
    rdamobility__thread.start()
    syngenta_agro__thread.start()
    stefanini__thread.start()
    agidea__thread.start()
    ferring__thread.start()

    grancolombianagold_client__thread.start()
    rehinland_client__thread.start()
    avevacol_client__thread.start()
    proyectourcol_client__thread.start()
    indracol_client__thread.start()
    vozikcol_client__thread.start()

    # Join threads
    schneider_electric__thread.join()
    rdamobility__thread.join()
    syngenta_agro__thread.join()
    stefanini__thread.join()
    agidea__thread.join()
    ferring__thread.join()

    grancolombianagold_client__thread.join()
    rehinland_client__thread.join()
    avevacol_client__thread.join()
    proyectourcol_client__thread.join()
    indracol_client__thread.join()
    vozikcol_client__thread.join()


def get_full_list():
    devices: List[DeviceDTO] = []

    devices += repo.rdamobility_client.devices
    devices += repo.syngenta_agro_client.devices
    devices += repo.stefanini_client.devices
    devices += repo.schneider_electric_client.devices
    devices += repo.agidea_client.devices
    devices += repo.ferring_client.devices

    devices += repo.grancolombianagold_client.devices
    devices += repo.rehinland_client.devices
    devices += repo.avevacol_client.devices
    devices += repo.proyectourcol_client.devices
    devices += repo.indracol_client.devices
    devices += repo.vozikcol_client.devices


    return [device.dict() for device in devices if device.dict() is not None]


def update_devices_in_zoho():
    device_list = get_full_list()

    partitions = [device_list[i: i + constants.REGS_PER_BULK]
                  for i in range(0, len(device_list), constants.REGS_PER_BULK)]

    total_success_cases = 0
    for index, data in enumerate(partitions, 1):
        try:
            logger.info(
                f'Updating set {index} of {len(partitions)} with {len(data)} vehicles.')
            response = repo.zoho_client.call_upsert(data)
            success_cases = len(
                [case for case in response['data'] if case['code'] == 'SUCCESS'])
            total_success_cases += success_cases
            if success_cases < len(data):
                logger.warning(
                    f'Some vehicles could not be upldated. Just {success_cases} of {len(data)} cases were success')
                logger.warning(data)
                logger.warning(response)
                continue
            logger.info('All update cases were success.')

        except AssertionError as error:
            logger.error(
                f'Error on update of partition N°{index} of {len(partitions)}')
            logger.error(error.args)
    logger.info(f'Updated {total_success_cases} vehicles.')


def run():
    get_devices_by_db()

    update_devices_by_db()

    update_devices_in_zoho()
