import os
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import generarClaveAes256, generarIvAes


# demo que muestra la diferencia entre aes ecb y cbc mostrando los bloques cifrados en hex y comparando la cantidad de bloques repetidos para un mensaje con bloques repetidos
def partirEnBloquesHex(datos: bytes, tamanoBloque: int = 16) -> list[str]:
    return [
        datos[i : i + tamanoBloque].hex() for i in range(0, len(datos), tamanoBloque)
    ]


def main():
    mensaje = ("hola hola hola!!" * 6).encode("utf-8")
    clave = generarClaveAes256()
    iv = generarIvAes()
    mensajePadded = pad(mensaje, 16)

    aesEcb = AES.new(clave, AES.MODE_ECB)
    cifradoEcb = aesEcb.encrypt(mensajePadded)
    aesCbc = AES.new(clave, AES.MODE_CBC, iv=iv)
    cifradoCbc = aesCbc.encrypt(mensajePadded)
    bloquesEcb = partirEnBloquesHex(cifradoEcb, 16)
    bloquesCbc = partirEnBloquesHex(cifradoCbc, 16)

    print("mensaje en bytes:", len(mensaje))
    print("mensaje padded bytes:", len(mensajePadded))
    print("")

    print("ecb bloques hex:")
    for i, b in enumerate(bloquesEcb):
        print(f"bloque {i:02d}: {b}")

    print("")
    print("cbc bloques hex:")
    for i, b in enumerate(bloquesCbc):
        print(f"bloque {i:02d}: {b}")

    print("")
    print("comparacion simple de repeticion")
    repetidosEcb = len(bloquesEcb) - len(set(bloquesEcb))
    repetidosCbc = len(bloquesCbc) - len(set(bloquesCbc))
    print("bloques repetidos ecb:", repetidosEcb)
    print("bloques repetidos cbc:", repetidosCbc)


if __name__ == "__main__":
    main()
