import os
import sys

rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import *


# demo que muestra la longitud en bytes y bits de las claves generadas para des, 3des 16, 3des 24 y aes 256
def mostrarInfoClave(nombre: str, clave: bytes) -> None:
    print(f"{nombre} longitud bytes: {len(clave)}")
    print(f"{nombre} longitud bits: {len(clave) * 8}")
    print("-" * 40)


def main():
    claveDes = generarClaveDes()
    clave3des16 = generarClaveTripleDes(16)
    clave3des24 = generarClaveTripleDes(24)
    claveAes = generarClaveAes256()

    mostrarInfoClave("des", claveDes)
    mostrarInfoClave("3des 16", clave3des16)
    mostrarInfoClave("3des 24", clave3des24)
    mostrarInfoClave("aes 256", claveAes)


if __name__ == "__main__":
    main()
