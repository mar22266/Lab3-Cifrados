import os
import sys
import secrets

# src al path para poder importar los modulos a probar
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# importar las funciones a probar
from utils import generarClaveTripleDes
from tripleDesCbc import (
    cifrarTripleDesCbc,
    descifrarTripleDesCbc,
    validarRoundTripTripleDesCbc,
    obtenerDescripcionEsquemaClave,
)


# prueba round trip 3des cbc con esquema de 2 claves 16 bytes
def testTripleDesCbcRoundTripClave16():
    clave = generarClaveTripleDes(16)
    mensaje = b"prueba 3des cbc con clave de 16 bytes"
    assert validarRoundTripTripleDesCbc(mensaje, clave)


# prueba round trip 3des cbc con esquema de 3 claves 24 bytes
def testTripleDesCbcRoundTripClave24():
    clave = generarClaveTripleDes(24)
    mensaje = b"prueba 3des cbc con clave de 24 bytes"
    assert validarRoundTripTripleDesCbc(mensaje, clave)


# prueba que cada cifrado en cbc use un iv diferente y por tanto el output sea diferente
def testTripleDesCbcIvDiferenteCadaCifrado():
    clave = generarClaveTripleDes(24)
    mensaje = b"mismo mensaje para comparar iv"
    cifrado1 = cifrarTripleDesCbc(mensaje, clave)
    cifrado2 = cifrarTripleDesCbc(mensaje, clave)
    iv1 = cifrado1[:8]
    iv2 = cifrado2[:8]

    assert iv1 != iv2
    assert cifrado1 != cifrado2


# prueba round trip 3des cbc con varias longitudes
def testTripleDesCbcRecuperaOriginalVariasLongitudes():
    clave = generarClaveTripleDes(16)
    for n in [0, 1, 7, 8, 9, 15, 16, 31, 32, 100, 257]:
        mensaje = secrets.token_bytes(n)
        cifrado = cifrarTripleDesCbc(mensaje, clave)
        descifrado = descifrarTripleDesCbc(cifrado, clave)
        assert descifrado == mensaje


# prueba que la descripcion documente correctamente la diferencia 16 bytes vs 24 bytes
def testDescripcionEsquemaClave():
    clave16 = generarClaveTripleDes(16)
    clave24 = generarClaveTripleDes(24)
    descripcion16 = obtenerDescripcionEsquemaClave(clave16)
    descripcion24 = obtenerDescripcionEsquemaClave(clave24)

    assert "16 bytes" in descripcion16
    assert "24 bytes" in descripcion24


# prueba con archivo real cifra 3des.txt guarda evidencia cipher+iv y clave y valida round-trip exacto
def testTripleDesCbcGeneraOutputDesdeTxtYRecuperaOriginal():
    rutaEntrada = os.path.join("data", "input", "3des.txt")
    rutaSalidaCipher = os.path.join("data", "output", "tripleDesCbcCipher.bin")
    rutaSalidaKeyHex = os.path.join("data", "output", "tripleDesKey.hex")

    with open(rutaEntrada, "rb") as f:
        mensaje = f.read()

    clave = generarClaveTripleDes(24)
    cifrado = cifrarTripleDesCbc(mensaje, clave)  # iv + ciphertext
    os.makedirs(os.path.dirname(rutaSalidaCipher), exist_ok=True)

    with open(rutaSalidaCipher, "wb") as f:
        f.write(cifrado)
    with open(rutaSalidaKeyHex, "w", encoding="utf-8") as f:
        f.write(clave.hex())

    descifrado = descifrarTripleDesCbc(cifrado, clave)
    assert descifrado == mensaje
