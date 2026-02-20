import os
import sys
import secrets
import pytest

# agregar el src al path para poder importar los modulos a probar
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# importar las funciones a probar padding manual y DES ECB
from desEcb import (
    pkcs7Pad,
    pkcs7Unpad,
    cifrarDesEcb,
    descifrarDesEcb,
    validarRoundTripDesEcb,
)


# prueba padding agrega 4 bytes 0x04
def testPkcs7PadCasoBasico():
    datos = b"hola"
    padded = pkcs7Pad(datos, 8)
    assert len(padded) == 8
    assert padded.endswith(b"\x04" * 4)


# prueba padding si el mensaje ya es multiplo exacto agrega un bloque completo 8 bytes 0x08
def testPkcs7PadBloqueCompleto():
    datos = b"12345678"
    padded = pkcs7Pad(datos, 8)
    assert len(padded) == 16
    assert padded.endswith(b"\x08" * 8)


# prueba unpad recupera el mensaje original despues de pad
def testPkcs7UnpadRecuperaOriginal():
    datos = b"hola"
    padded = pkcs7Pad(datos, 8)
    unpadded = pkcs7Unpad(padded, 8)
    assert unpadded == datos


# prueba round trip DES ECB para multiples longitudes aleatorias comprobar descifrar(cifrar(m)) == m
def testDesEcbRoundTripVariasLongitudes():
    clave = secrets.token_bytes(8)
    for n in [0, 1, 2, 7, 8, 9, 15, 16, 31, 32, 100]:
        mensaje = secrets.token_bytes(n)
        assert validarRoundTripDesEcb(mensaje, clave)


# prueba cifrado y descifrado DES ECB recupera el mensaje original en un caso fijo
def testDesEcbDescifrarRecuperaOriginal():
    clave = secrets.token_bytes(8)
    mensaje = b"mensaje de prueba para des ecb"
    cifrado = cifrarDesEcb(mensaje, clave)
    descifrado = descifrarDesEcb(cifrado, clave)
    assert descifrado == mensaje


# prueba de error
def testPkcs7UnpadInvalidoLanzaError():
    with pytest.raises(ValueError):
        pkcs7Unpad(b"abcd\x02\x03", 4)


# prueba con archivo real cifra des.txt, guarda evidencia cipher y clave y valida round-trip exacto
def testDesEcbGeneraOutputDesdeTxtYRecuperaOriginal():
    rutaEntrada = os.path.join("data", "input", "des.txt")
    rutaSalidaCipher = os.path.join("data", "output", "desEcbCipher.bin")
    rutaSalidaKeyHex = os.path.join("data", "output", "desEcbKey.hex")

    with open(rutaEntrada, "rb") as f:
        mensaje = f.read()
    clave = secrets.token_bytes(8)
    cifrado = cifrarDesEcb(mensaje, clave)
    os.makedirs(os.path.dirname(rutaSalidaCipher), exist_ok=True)

    with open(rutaSalidaCipher, "wb") as f:
        f.write(cifrado)

    with open(rutaSalidaKeyHex, "w", encoding="utf-8") as f:
        f.write(clave.hex())

    descifrado = descifrarDesEcb(cifrado, clave)
    assert descifrado == mensaje
