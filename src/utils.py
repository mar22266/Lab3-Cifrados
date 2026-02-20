# importar las librerias necesarias
import secrets
from typing import Union
from Crypto.Cipher import DES3


# funcion que genera una clave des de 8 bytes
def generarClaveDes() -> bytes:
    return secrets.token_bytes(8)


# funcion que lee los bytes de un archivo y los regresa como bytes
def leerBytesDesdeArchivo(rutaArchivo: str) -> bytes:
    with open(rutaArchivo, "rb") as f:
        return f.read()


# funcion que escribe bytes a un archivo
def escribirBytesEnArchivo(rutaArchivo: str, datos: Union[bytes, bytearray]) -> None:
    with open(rutaArchivo, "wb") as f:
        f.write(datos)


# funcion que genera una clave triple des valida de 16 o 24 bytes segun el tamano solicitado
def generarClaveTripleDes(tamanoClave: int = 24) -> bytes:
    if tamanoClave not in (16, 24):
        raise ValueError("tamanoClave debe ser 16 o 24")
    while True:
        candidata = secrets.token_bytes(tamanoClave)
        candidata = DES3.adjust_key_parity(candidata)

        try:
            DES3.new(candidata, DES3.MODE_ECB)
            return candidata
        except ValueError:
            continue


# funcion que genera una clave aes de 32 bytes para aes 256
def generarClaveAes256() -> bytes:
    return secrets.token_bytes(32)


# funcion que genera un iv de 16 bytes para aes
def generarIvAes() -> bytes:
    return secrets.token_bytes(16)
