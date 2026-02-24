# importar las librerias necesarias
# se solicito ayuda con chatgpt para la escritura de este codigo para lograr hacer la separacion correcta
from typing import Tuple


# funciones para separar el header y body de un ppm y recomponerlo despues de cifrar el body
def separarHeaderYBodyPpm(datosPpm: bytes) -> Tuple[bytes, bytes]:
    if not isinstance(datosPpm, (bytes, bytearray)):
        raise TypeError("datos del Ppm debe ser bytes o bytearray")

    data = bytes(datosPpm)
    if not data.startswith(b"P6"):
        raise ValueError("solo se soporta ppm tipo p6")
    i = 0
    tokens = []
    while len(tokens) < 4:
        if i >= len(data):
            raise ValueError("ppm invalido")
        if data[i : i + 1].isspace():
            i += 1
            continue
        if data[i : i + 1] == b"#":
            while i < len(data) and data[i : i + 1] not in (b"\n", b"\r"):
                i += 1
            continue
        inicio = i
        while i < len(data) and not data[i : i + 1].isspace():
            i += 1
        tokens.append(data[inicio:i])
    headerFin = i
    while headerFin < len(data) and data[headerFin : headerFin + 1].isspace():
        headerFin += 1
    header = data[:headerFin]
    body = data[headerFin:]
    return header, body


# funcion que recombina el header y body de un ppm para generar un nuevo ppm
def recomponerPpm(header: bytes, body: bytes) -> bytes:
    if not isinstance(header, (bytes, bytearray)):
        raise TypeError("header debe ser bytes o bytearray")
    if not isinstance(body, (bytes, bytearray)):
        raise TypeError("body debe ser bytes o bytearray")

    return bytes(header) + bytes(body)
