# importacion de libreerias necesarias
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from utils import *
from ppmProcess import separarHeaderYBodyPpm, recomponerPpm


# funcion que cifra el con aed ecb usando padding
def cifrarBodyAesEcb(body: bytes, claveAes: bytes) -> bytes:
    cipher = AES.new(bytes(claveAes), AES.MODE_ECB)
    padded = pad(bytes(body), 16)
    return cipher.encrypt(padded)


# funcon que cifra el con aed cbc usando padding
def cifrarBodyAesCbc(body: bytes, claveAes: bytes, iv: bytes) -> bytes:
    cipher = AES.new(bytes(claveAes), AES.MODE_CBC, iv=bytes(iv))
    padded = pad(bytes(body), 16)
    return cipher.encrypt(padded)


# funcion que lee un ppm mantiene el header intacto y cifra solo los pixeles con aes ecb
def cifrarImagenPpmAesEcb(rutaEntrada: str, rutaSalida: str, claveAes: bytes) -> None:
    datos = leerBytesDesdeArchivo(rutaEntrada)
    header, body = separarHeaderYBodyPpm(datos)
    bodyCifrado = cifrarBodyAesEcb(body, claveAes)
    datosSalida = recomponerPpm(header, bodyCifrado)
    escribirBytesEnArchivo(rutaSalida, datosSalida)


# funcion que lee un ppm mantiene el header intacto y cifra solo los pixeles con cbc
def cifrarImagenPpmAesCbc(rutaEntrada: str, rutaSalida: str, claveAes: bytes) -> bytes:
    datos = leerBytesDesdeArchivo(rutaEntrada)
    header, body = separarHeaderYBodyPpm(datos)
    iv = generarIvAes()
    bodyCifrado = cifrarBodyAesCbc(body, claveAes, iv)
    datosSalida = recomponerPpm(header, bodyCifrado)
    escribirBytesEnArchivo(rutaSalida, datosSalida)
    escribirBytesEnArchivo(rutaSalida + ".iv", iv)
    return iv
