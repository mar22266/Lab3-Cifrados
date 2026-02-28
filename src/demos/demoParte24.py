from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import sys


rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import generarClaveAes256, generarIvAes


# demo que muestra como el uso de un iv fijo en aes cbc hace que el mismo mensaje cifrado con la misma clave produzca el mismo resultado
def cifrarAesCbcConIv(mensaje: bytes, clave: bytes, iv: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_CBC, iv=iv)
    mensajePadded = pad(mensaje, 16)
    return cipher.encrypt(mensajePadded)


def main():
    mensaje = b"me gusta jugar futbol"
    clave = generarClaveAes256()

    ivFijo = generarIvAes()
    cbc1 = cifrarAesCbcConIv(mensaje, clave, ivFijo)
    cbc2 = cifrarAesCbcConIv(mensaje, clave, ivFijo)

    iv1 = generarIvAes()
    iv2 = generarIvAes()
    cbc3 = cifrarAesCbcConIv(mensaje, clave, iv1)
    cbc4 = cifrarAesCbcConIv(mensaje, clave, iv2)

    print("caso 1 mismo iv")
    print("iv:", ivFijo.hex())
    print("cbc1:", cbc1.hex())
    print("cbc2:", cbc2.hex())
    print("cbc1 igual a cbc2:", cbc1 == cbc2)
    print("-" * 50)

    print("caso 2 ivs diferentes")
    print("iv1:", iv1.hex())
    print("iv2:", iv2.hex())
    print("cbc3:", cbc3.hex())
    print("cbc4:", cbc4.hex())
    print("cbc3 igual a cbc4:", cbc3 == cbc4)


if __name__ == "__main__":
    main()
