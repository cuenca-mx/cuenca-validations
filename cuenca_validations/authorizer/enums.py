from enum import Enum


class EcommerceIndicator(str, Enum):
    """
    Adquirente graba
    Emisor lee
    0, “ “ = No es una transacción de comercio electrónico
    1 = Transacción MOTO
    5 = Comercio seguro, titular autenticado (3D Secure)
    6 = Comercio seguro, titular no autenticado (3D Secure)
    7 = Autenticación 3D Secure no realizada
    """

    NotEcommerce = '0'
    TransaccionMOTO = '1'
    ComercioSeguro3DSAutenticado = '5'
    ComercioSeguro3DSNoAutenticado = '6'
    No3DS = '7'
