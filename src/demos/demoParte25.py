import os
import sys


rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.desEcb import pkcs7Pad, pkcs7Unpad


# demo que muestra como funciona el padding pkcs7 con bloques de 8 bytes mostrando el mensaje original, el mensaje padded
def imprimirCaso(nombre: str, mensaje: bytes):
    padded = pkcs7Pad(mensaje, 8)
    unpadded = pkcs7Unpad(padded, 8)

    print(nombre)
    print("mensaje original bytes:", len(mensaje))
    print("mensaje original hex:", mensaje.hex())

    print("mensaje padded bytes:", len(padded))
    print("mensaje padded hex:", padded.hex())

    print("recuperado bytes:", len(unpadded))
    print("recuperado hex:", unpadded.hex())
    print("recuperado igual al original:", unpadded == mensaje)
    print("-" * 50)


def main():
    imprimirCaso("caso 1 mensaje de 5 bytes", b"abcde")
    imprimirCaso("caso 2 mensaje de 8 bytes", b"abcdefgh")
    imprimirCaso("caso 3 mensaje de 10 bytes", b"abcdefghij")


if __name__ == "__main__":
    main()
