# imporar las librerias necesarias
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

from utils import generarClaveDes


# funcion que cifra con 3des en modo cbc con padding
# retorna iv concatenado al inicio seguido del ciphertext
def cifrarTripleDesCbc(plaintext: bytes, claveTripleDes: bytes) -> bytes:
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plaintext debe ser bytes o bytearray")
    if not isinstance(claveTripleDes, (bytes, bytearray)) or len(
        claveTripleDes
    ) not in (16, 24):
        raise ValueError("clave Triple Des debe ser de 16 o 24 bytes")

    iv = generarClaveDes()
    cipher = DES3.new(bytes(claveTripleDes), DES3.MODE_CBC, iv=iv)
    padded = pad(bytes(plaintext), 8)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext


# funcion que descifra con 3des en modo cbc espera que el iv venga
def descifrarTripleDesCbc(ivMasCiphertext: bytes, claveTripleDes: bytes) -> bytes:
    if not isinstance(ivMasCiphertext, (bytes, bytearray)):
        raise TypeError("iv Mas Cipher text debe ser bytes o bytearray")
    if not isinstance(claveTripleDes, (bytes, bytearray)) or len(
        claveTripleDes
    ) not in (16, 24):
        raise ValueError("clave Triple Des debe ser de 16 o 24 bytes")
    if len(ivMasCiphertext) < 16:
        raise ValueError("iv Mas Cipher text demasiado corto")

    iv = bytes(ivMasCiphertext[:8])
    ciphertext = bytes(ivMasCiphertext[8:])

    if (len(ciphertext) % 8) != 0:
        raise ValueError("cipher text debe ser multiplo de 8")

    cipher = DES3.new(bytes(claveTripleDes), DES3.MODE_CBC, iv=iv)
    padded = cipher.decrypt(ciphertext)

    return unpad(padded, 8)


# funcion que da descripcion del esquema de clave usado segun su longitud
def obtenerDescripcionEsquemaClave(claveTripleDes: bytes) -> str:
    if not isinstance(claveTripleDes, (bytes, bytearray)):
        raise TypeError("clave Triple Des debe ser bytes o bytearray")
    if len(claveTripleDes) == 16:
        return "clave de 16 bytes usa esquema de dos claves k1 y k2, equivalente a k1 k2 k1"
    if len(claveTripleDes) == 24:
        return "clave de 24 bytes usa esquema de tres claves k1 k2 k3"
    raise ValueError("clave Triple Des debe ser de 16 o 24 bytes")


# funcion que valida que descifrar regresa el original
def validarRoundTripTripleDesCbc(mensaje: bytes, claveTripleDes: bytes) -> bool:
    cifrado = cifrarTripleDesCbc(mensaje, claveTripleDes)
    descifrado = descifrarTripleDesCbc(cifrado, claveTripleDes)
    return descifrado == mensaje
