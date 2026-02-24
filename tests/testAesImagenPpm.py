import os
import sys

# src al path para poder importar los modulos a probar
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# importar las funciones a probar
from utils import generarClaveAes256, generarIvAes, leerBytesDesdeArchivo
from aesImageCipher import cifrarImagenPpmAesEcb, cifrarImagenPpmAesCbc
from ppmProcess import separarHeaderYBodyPpm


# prueba que la clave AES-256 generada tenga 32 bytes
def testClaveAes256LongitudCorrecta():
    clave = generarClaveAes256()
    assert len(clave) == 32


# prueba que el IV de AES para CBC tenga 16 bytes
def testIvAesLongitudCorrecta():
    iv = generarIvAes()
    assert len(iv) == 16


# prueba que el header PPM se mantenga intacto al cifrar en ECB y CBC solo cambia el body
def testHeaderSeMantieneIgualEnEcbYCbc():
    rutaEntrada = os.path.join("images", "input", "tux.ppm")
    rutaSalidaEcb = os.path.join("images", "output", "tuxAesEcb.ppm")
    rutaSalidaCbc = os.path.join("images", "output", "tuxAesCbc.ppm")
    clave = generarClaveAes256()
    cifrarImagenPpmAesEcb(rutaEntrada, rutaSalidaEcb, clave)
    cifrarImagenPpmAesCbc(rutaEntrada, rutaSalidaCbc, clave)
    original = leerBytesDesdeArchivo(rutaEntrada)
    ecb = leerBytesDesdeArchivo(rutaSalidaEcb)
    cbc = leerBytesDesdeArchivo(rutaSalidaCbc)
    headerOriginal, _ = separarHeaderYBodyPpm(original)
    headerEcb, _ = separarHeaderYBodyPpm(ecb)
    headerCbc, _ = separarHeaderYBodyPpm(cbc)

    assert headerEcb == headerOriginal
    assert headerCbc == headerOriginal


# prueba que CBC genere un IV distinto en cada cifrado y produzca ciphertext diferente
def testCbcCambiaPorIvDiferente():
    rutaEntrada = os.path.join("images", "input", "tux.ppm")
    rutaSalidaCbc1 = os.path.join("images", "output", "tuxAesCbc_1.ppm")
    rutaSalidaCbc2 = os.path.join("images", "output", "tuxAesCbc_2.ppm")
    clave = generarClaveAes256()
    iv1 = cifrarImagenPpmAesCbc(rutaEntrada, rutaSalidaCbc1, clave)
    iv2 = cifrarImagenPpmAesCbc(rutaEntrada, rutaSalidaCbc2, clave)

    assert iv1 != iv2

    cbc1 = leerBytesDesdeArchivo(rutaSalidaCbc1)
    cbc2 = leerBytesDesdeArchivo(rutaSalidaCbc2)

    assert cbc1 != cbc2
