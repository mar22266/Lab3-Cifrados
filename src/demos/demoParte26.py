from Crypto.Cipher import AES
import secrets


# demo que muestra cifrar y decifrar usando AES em modo gcm usando
def cifrarAesGcm(plaintext: bytes, clave: bytes) -> tuple[bytes, bytes, bytes]:
    nonce = secrets.token_bytes(12)
    cipher = AES.new(clave, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce, ciphertext, tag


def descifrarAesGcm(nonce: bytes, ciphertext: bytes, tag: bytes, clave: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
