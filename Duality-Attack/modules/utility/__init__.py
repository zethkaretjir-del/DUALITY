from .crypt import FileCrypt
from .hash import HashGenerator
from .encode import EncodeDecode
from .passgen import PasswordGenerator
from .malware import EducationalMalware
from .rot13 import ROT13Tool
from .finder import FindWrapper
from .qr_gen import QRGenerator
from .speedtest import SpeedTest

__all__ = [
    'FileCrypt',
    'HashGenerator',
    'EncodeDecode',
    'PasswordGenerator',
    'EducationalMalware',
    'ROT13Tool',
    'FindWrapper'
    'QRGenerator',
    'SpeedTest',
]
