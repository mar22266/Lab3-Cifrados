from Crypto.Cipher import AES
from Crypto.Util import Counter


# cifra datos usando aes 256 en modo ctr con nonce de 8 bytes y contador de 64 bits sin padding y requiere nonce unico por clave
def cifrarAesCtr(plaintext: bytes, claveAes: bytes, nonce: bytes) -> bytes:
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plain text debe ser bytes o bytearray")
    if not isinstance(claveAes, (bytes, bytearray)) or len(claveAes) != 32:
        raise ValueError("clave Aes debe ser de 32 bytes para aes 256")
    if not isinstance(nonce, (bytes, bytearray)) or len(nonce) != 8:
        raise ValueError("nonce debe ser de 8 bytes")

    contador = Counter.new(
        64, prefix=bytes(nonce), initial_value=0, little_endian=False
    )
    cipher = AES.new(bytes(claveAes), AES.MODE_CTR, counter=contador)
    return cipher.encrypt(bytes(plaintext))


# ctr usa el mismo flujo para descifrar
def descifrarAesCtr(ciphertext: bytes, claveAes: bytes, nonce: bytes) -> bytes:
    return cifrarAesCtr(ciphertext, claveAes, nonce)
