import os
import sys

rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
rutaSrc = os.path.join(rutaRaiz, "src")

for ruta in (rutaRaiz, rutaSrc):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

from src.utils import generarClaveAes256
from src.aesImageCipher import cifrarImagenPpmAesEcb, cifrarImagenPpmAesCbc


# demo que muestra las imagenes cifradas con aes ecb y cbc para mostrar la diferencia visual entre ambos modos
def main():
    rutaEntrada = os.path.join("images", "input", "tux.ppm")
    rutaSalidaEcb = os.path.join("images", "demo", "tuxAesEcb.ppm")
    rutaSalidaCbc = os.path.join("images", "demo", "tuxAesCbc.ppm")

    claveAes = generarClaveAes256()

    cifrarImagenPpmAesEcb(rutaEntrada, rutaSalidaEcb, claveAes)
    cifrarImagenPpmAesCbc(rutaEntrada, rutaSalidaCbc, claveAes)

    print("Imagenes cifrada con AES ECB guardada en:", rutaSalidaEcb)


if __name__ == "__main__":
    main()
