# imporar las librerias necesarias
from Crypto.Cipher import DES


# funcion que aplica padding pkcs7 manual
def pkcs7Pad(datos: bytes, tamanoBloque: int = 8) -> bytes:
    if not isinstance(datos, (bytes, bytearray)):
        raise TypeError("datos debe ser bytes o bytearray")
    if not isinstance(tamanoBloque, int) or tamanoBloque <= 0 or tamanoBloque > 255:
        raise ValueError("tamano del Bloque debe ser int entre 1 y 255")

    faltante = tamanoBloque - (len(datos) % tamanoBloque)
    if faltante == 0:
        faltante = tamanoBloque

    return bytes(datos) + bytes([faltante] * faltante)


# funcion que remueve padding pkcs7 manual con validaciones basicas
def pkcs7Unpad(datos: bytes, tamanoBloque: int = 8) -> bytes:
    if not isinstance(datos, (bytes, bytearray)):
        raise TypeError("datos debe ser bytes o bytearray")
    if not isinstance(tamanoBloque, int) or tamanoBloque <= 0 or tamanoBloque > 255:
        raise ValueError("tamano delBloque debe ser int entre 1 y 255")
    if len(datos) == 0 or (len(datos) % tamanoBloque) != 0:
        raise ValueError("datos no tiene longitud valida para pkcs7")

    valorPad = datos[-1]
    if valorPad < 1 or valorPad > tamanoBloque:
        raise ValueError("padding pkcs7 invalido")

    pad = datos[-valorPad:]
    if pad != bytes([valorPad] * valorPad):
        raise ValueError("padding pkcs7 invalido")

    return bytes(datos[:-valorPad])


# funcion que cifra des en modo ecb con padding pkcs7 manual
def cifrarDesEcb(plaintext: bytes, claveDes: bytes) -> bytes:
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plain text debe ser bytes o bytearray")
    if not isinstance(claveDes, (bytes, bytearray)) or len(claveDes) != 8:
        raise ValueError("clave Des debe ser de 8 bytes")

    cipher = DES.new(bytes(claveDes), DES.MODE_ECB)
    padded = pkcs7Pad(bytes(plaintext), 8)
    return cipher.encrypt(padded)


# funcion que descifra des en modo ecb y remueve padding pkcs7 manual
def descifrarDesEcb(ciphertext: bytes, claveDes: bytes) -> bytes:
    if not isinstance(ciphertext, (bytes, bytearray)):
        raise TypeError("cipher text debe ser bytes o bytearray")
    if not isinstance(claveDes, (bytes, bytearray)) or len(claveDes) != 8:
        raise ValueError("clave Des debe ser de 8 bytes")
    if len(ciphertext) == 0 or (len(ciphertext) % 8) != 0:
        raise ValueError("cipher text debe ser multiplo de 8 para des")

    cipher = DES.new(bytes(claveDes), DES.MODE_ECB)
    padded = cipher.decrypt(bytes(ciphertext))
    return pkcs7Unpad(padded, 8)


# funcion que valida que descifrar regresa el original
def validarRoundTripDesEcb(mensaje: bytes, claveDes: bytes) -> bool:
    cifrado = cifrarDesEcb(mensaje, claveDes)
    descifrado = descifrarDesEcb(cifrado, claveDes)
    return descifrado == mensaje
