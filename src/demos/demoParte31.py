import os
import sys
import time
import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import generarClaveAes256, generarIvAes, generarClaveDes


# demo que muestra la diferencia entre aes cbc y ctr mostrando que ctr no requiere padding y es mas rapido para grandes cantidades de datos
def cifrarAesCbc(plaintext: bytes, clave: bytes, iv: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_CBC, iv=iv)
    return cipher.encrypt(pad(plaintext, 16))


def descifrarAesCbc(ciphertext: bytes, clave: bytes, iv: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ciphertext), 16)


def cifrarAesCtr(plaintext: bytes, clave: bytes, nonce: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_CTR, nonce=nonce)
    return cipher.encrypt(plaintext)


def descifrarAesCtr(ciphertext: bytes, clave: bytes, nonce: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(ciphertext)


# ayuda de chat gpt para escribir la demo que compara aes cbc vs ctr y muestra que ctr no requiere padding y es mas rapido para grandes cantidades de datos
def main():
    clave = generarClaveAes256()
    iv = generarIvAes()
    nonce = generarClaveDes()
    mensaje = b"hola hola hola holah"
    print("mensaje bytes:", len(mensaje))

    cbc = cifrarAesCbc(mensaje, clave, iv)
    ctr = cifrarAesCtr(mensaje, clave, nonce)

    print("cbc bytes:", len(cbc))
    print("ctr bytes:", len(ctr))
    print("ctr no requiere padding porque mantiene longitud igual al mensaje")
    print("-" * 50)

    mensajeCbc = descifrarAesCbc(cbc, clave, iv)
    mensajeCtr = descifrarAesCtr(ctr, clave, nonce)

    print("round trip cbc ok:", mensajeCbc == mensaje)
    print("round trip ctr ok:", mensajeCtr == mensaje)
    print("-" * 50)

    tamano = 10 * 1024 * 1024
    datos = secrets.token_bytes(tamano)

    print("benchmark 10mb")

    inicio = time.perf_counter()
    _ = cifrarAesCbc(datos, clave, iv)
    fin = time.perf_counter()
    tiempoCbc = fin - inicio

    inicio = time.perf_counter()
    _ = cifrarAesCtr(datos, clave, nonce)
    fin = time.perf_counter()
    tiempoCtr = fin - inicio

    print("tiempo cbc segundos:", round(tiempoCbc, 6))
    print("tiempo ctr segundos:", round(tiempoCtr, 6))


if __name__ == "__main__":
    main()
