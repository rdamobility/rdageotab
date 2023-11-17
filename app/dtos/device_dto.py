from ..helpers.format_helpers import license_plate_validator
import logging

logger = logging.getLogger(__name__)

class DeviceDTO:
    def __init__(self, **kwargs):
        self.id = kwargs['id']  # Just for geotab
        self.name = kwargs['name']
        self.license_plate = None
        chassis = kwargs['engineVehicleIdentificationNumber']
        self.chassis = None if '@' in chassis else chassis
        self.last_odometer_kms = None
        self.last_odometer_date = None

        if license_plate_validator(kwargs['licensePlate']) is not None:
            self.license_plate = kwargs['licensePlate']
        elif license_plate_validator(self.name) is not None:
            self.license_plate = self.name
        else:
            logger.warn(f'Failed to extract device patent for {kwargs["licensePlate"]} and {self.name}')

    def __str__(self) -> str:
        res = f'{self.id} - {self.name}'
        if self.license_plate:
            res += f' ({self.license_plate})'
        return res
    
    def __repr__(self) -> str:
        res = f'{self.id} - {self.name}'
        if self.license_plate:
            res += f' ({self.license_plate})'
        return res

    def dict(self) -> dict:
        response = {
            'Ultimo_Odometro_KM': self.last_odometer_kms,
            'Fecha_ult_Odometro': self.last_odometer_date,
        }
        if self.chassis is not None:
            response['Chasis'] = self.chassis

        if self.license_plate is not None:
            response['Name'] = self.license_plate

        if 'Name' not in response and 'Chasis' not in response:
            return None
        return response
