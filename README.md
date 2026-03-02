## Como correr el proyecto y validar que todo funciona

### instalar dependencias

antes de correr cualquier cosa, instalar los requirements desde la raiz del proyecto:

```bash
pip install -r requirements.txt
```

### correr los tests

los tests verifican que todo el codigo funciona correctamente. actualmente hay 17 tests y se ejecutan con pytest, los puntos extra no se encuentran en los tests unicamente en los demos del inciso especifico...

desde la raiz del proyecto:

```bash
pytest -q
```

### Archivo requerido para pytest

para que pytest detecte los tests con el patron correcto, se debe tener este archivo en la raiz del proyecto:

archivo: pytest.ini

contenido:

```bash
[pytest]
python_files = test*.py
python_functions = test*
```

### Estructura de carpetas y para que sirve cada una

### `src`

Aquí está toda la implementación del laboratorio:

- Funciones de cifrado
- Funciones de descifrado
- Implementación de padding (PKCS#7)
- Procesamiento de imágenes PPM
- Utilidades auxiliares

Esta carpeta es la base del código que utilizan tanto los tests como los demos.

---

### `tests`

Aquí están los tests unitarios que validan que cada punto del laboratorio funciona correctamente.

### `demos`

Aquí están los scripts de demostración utilizados para la Parte 2 (análisis de seguridad).

Estos scripts imprimen resultados en consola para responder las preguntas

### `images`

Esta carpeta contiene imágenes de entrada y salida utilizadas en la parte visual del laboratorio.

#### `images/input/`

Contiene todas las imágenes disponibles.

Hay varias imágenes que se podrían utilizar para las pruebas, pero en este laboratorio se utilizó:

tux.ppm

#### `images/output/`

Guarda las imágenes generadas por los procesos de cifrado, por ejemplo:

tuxAesEcb.ppm
tuxAesCbc.ppm
tuxAesEcb.ppm.iv
tuxAesCbc.ppm.iv

Estas salidas se utilizan para comparar visualmente por qué ECB es inseguro, ya que mantiene patrones visibles en la imagen cifrada.

#### `images/renders/`

Contiene las versiones finales en **formato PNG** utilizadas en el README:

- Imagen original
- Imagen cifrada con AES-ECB
- Imagen cifrada con AES-CBC

Esta carpeta existe para facilitar la visualización directa en GitHub y mostrar claramente la diferencia entre los modos de operación.

### `images/demo/`

Esta carpeta guarda los outputs generados por uno de los scripts de demostración de la Parte 2.

---

## Parte 2: Análisis de Seguridad (25 puntos)

### 2.1 Análisis de Tamaños de Clave (4 puntos)

**Pregunta: ¿Qué tamaño de clave está usando para DES, 3DES y AES? Para cada uno:**

- **o Indique el tamaño en bits y bytes**
- **o Explique por qué DES se considera inseguro hoy en día**
- **o Calcule cuánto tiempo tomaría un ataque de fuerza bruta con hardware moderno**

**Requisito:**

- **o Incluya un snippet de código que muestre cómo genera cada clave y su longitud.**

#### tamaños de clave usados en este laboratorio

- **des**
  - **tamano en bytes:** 8 bytes
  - **tamano en bits:** 64 bits totales
  - **bits efectivos de seguridad:** 56 bits los otros 8 bits son de paridad

- **3des**
  - **tamano en bytes:** 16 o 24 bytes
  - **tamano en bits:** 128 o 192 bits totales
  - **bits efectivos aproximados:**
    - **16 bytes (dos claves):** 112 bits efectivos esquema k1 k2 k1
    - **24 bytes (tres claves):** 168 bits efectivos k1 k2 k3

- **aes 256**
  - **tamano en bytes:** 32 bytes
  - **tamano en bits:** 256 bits efectivos

#### por que des se considera inseguro hoy en dia

DES es inseguro principalmente porque su seguridad efectiva es de **56 bits**, lo cual es un espacio de claves demasiado pequeno para la fuerza bruta hoy en dia. Lo que significa que un atacante puede probar una cantidad grande de claves por segundo con hardware capaz y encontrar la clave en un tiempo practico.
Ademas, DES es un cifrado antiguo, y existen implementaciones y hardware dedicados que aceleran el ataque de fuerza bruta, volviendolo aun mas accesible.

#### cuanto tiempo tomaria un ataque de fuerza bruta con hardware moderno

- **espacio de claves efectivo de des:** \(2^{56}\) claves

- si un atacante tiene hardware capaz de probar aproximadamente:
  - **10^12 claves por segundo** 1 tera de clave por segundo, cifra realista para hardware especializado o clusters modernos (ayuda de verificacion de dato con chatgpt)

entonces el tiempo seria:

- **peor caso:**  
  \( 2^{56} / 10^{12} \approx 72,057,594 \) segundos  
  eso son aproximadamente:
  - **833 dias**
  - **2.28 anos**

- **caso promedio encontrar la clave a la mitad del espacio:**  
  \(\approx 1.14 anos\)

Con hardware muy bueno y potente o distribuido, los tiempos se reducen aun mas. Por eso ya no es lo mejor hoy en dia.

#### snippet de codigo para generar cada clave y mostrar su longitud

```bash
demoParte2.py
des longitud bytes: 8
des longitud bits: 64
----------------------------------------
3des 16 longitud bytes: 16
3des 16 longitud bits: 128
----------------------------------------
3des 24 longitud bytes: 24
3des 24 longitud bits: 192
----------------------------------------
aes 256 longitud bytes: 32
aes 256 longitud bits: 256
----------------------------------------
```

### 2.2 Comparación de Modos de Operación (5 puntos)

**Pregunta: Compare ECB vs CBC mostrando:**
o ¿Qué modo de operación implementó en cada algoritmo?  
o ¿Cuáles son las diferencias fundamentales entre ECB y CBC?  
o ¿Se puede notar la diferencia directamente en una imagen?

**Requisitos:**
o Incluya las tres imágenes lado a lado: original, cifrada con ECB, cifrada con CBC  
o Señale específicamente qué patrones son visibles en ECB pero no en CBC  
o Proporcione el código exacto que usó para generar estas imágenes...

#### ¿Qué modo de operación implementó en cada algoritmo?

- **des:** ecb
- **3des:** cbc
- **aes (imagen):** ecb y cbc

en este punto, la comparacion visual se hace con **aes**, porque ecb vs cbc se nota claramente en imagenes con patrones.

#### ¿Cuáles son las diferencias fundamentales entre ECB y CBC?

- **ecb (electronic codebook)**
  - cifra cada bloque por separado con la misma clave
  - si dos bloques de plaintext son iguales, generan dos bloques de ciphertext iguales
  - esto filtra patrones y estructura del contenido

- **cbc (cipher block chaining)**
  - antes de cifrar cada bloque, lo combina con el bloque cifrado anterior usando xor
  - usa un iv aleatorio para el primer bloque
  - aunque dos bloques de plaintext sean iguales, su ciphertext suele ser diferente por el encadenamiento y el iv

#### ¿Se puede notar la diferencia directamente en una imagen?

si. con una imagen con areas uniformes o patrones claros, se nota asi:

- **aes ecb:** se siguen viendo siluetas y patrones por repeticion de bloques
- **aes cbc:** la imagen pierde estructura visible y se ve mas como ruido uniforme

#### evidencia visual lado a lado

## Evidencia visual lado a lado

<table>
  <tr>
    <th>Original</th>
    <th>ECB</th>
    <th>CBC</th>
  </tr>
  <tr>
    <td><img src="imagenes/renders/tux.png" width="250"/></td>
    <td><img src="imagenes/renders/tuxAesEcb.png" width="250"/></td>
    <td><img src="imagenes/renders/tuxAesCbc.png" width="250"/></td>
  </tr>
</table>

```bash
import os

from utils import generarClaveAes256
from aesImageCipher import cifrarImagenPpmAesEcb, cifrarImagenPpmAesCbc


def main():
    rutaEntrada = os.path.join("images", "input", "tux.ppm")
    rutaSalidaEcb = os.path.join("images", "demo", "tuxAesEcb.ppm")
    rutaSalidaCbc = os.path.join("images", "demo", "tuxAesCbc.ppm")

    claveAes = generarClaveAes256()

    cifrarImagenPpmAesEcb(rutaEntrada, rutaSalidaEcb, claveAes)
    cifrarImagenPpmAesCbc(rutaEntrada, rutaSalidaCbc, claveAes)


if __name__ == "__main__":
    main()
```

### 2.3 Vulnerabilidad de ECB (6 puntos)

**Pregunta: ¿Por qué no debemos usar ECB en datos sensibles?**

**Requisitos:**
o Cree un ejemplo que muestre cómo bloques idénticos producen cifrados idénticos  
o Cifre un mensaje que contenga texto repetido (ej: "ATAQUE ATAQUE ATAQUE") con ECB y CBC  
o Muestre en hexadecimal cómo los bloques cifrados son iguales en ECB pero diferentes en CBC  
o Explique qué información podría filtrar esto en un escenario real

#### ¿Por qué no debemos usar ECB en datos sensibles?

no debemos usar ecb en datos sensibles porque **no oculta patrones**. ecb cifra cada bloque de manera independiente con la misma clave, entonces si el plaintext tiene bloques repetidos, el ciphertext tambien tendra bloques repetidos. esto puede filtrar estructura, repeticion y partes del contenido, aun si el atacante no conoce la clave.

#### ejemplo practico: bloques identicos generan cifrados identicos

Para demostrarlo, se cifra un mensaje con texto repetido. la idea es que el mensaje tenga bloques iguales. luego se imprime el ciphertext en bloques y en hexadecimal para ver si hay repeticiones. en ecb, se ven bloques iguales repetidos. en cbc, aunque el plaintext se repita, los bloques de ciphertext no quedan iguales por el encadenamiento y el iv.

#### script de demostracion

```bash
import os
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import generarClaveAes256, generarIvAes


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

```

#### Resultado del codigo

```bash
mensaje en bytes: 96
mensaje padded bytes: 112

ecb bloques hex:
bloque 00: a636fc4af14c0d3011384353e9d85ee9
bloque 01: a636fc4af14c0d3011384353e9d85ee9
bloque 02: a636fc4af14c0d3011384353e9d85ee9
bloque 03: a636fc4af14c0d3011384353e9d85ee9
bloque 04: a636fc4af14c0d3011384353e9d85ee9
bloque 05: a636fc4af14c0d3011384353e9d85ee9
bloque 06: f029c404e3d1d928986f2bab1ef7d158

cbc bloques hex:
bloque 00: f318dbeef72ed0c31e2e80cf3f84415c
bloque 01: f9afbaec62985a1262473d50cc8ed02e
bloque 02: 2f9ed0eb2971cf2605a852c2f05ce2a4
bloque 03: 3815cc3427e21e2707799fcdfa79e6da
bloque 04: b68b3bb3137423f0a4d1ed758a7da791
bloque 05: 4dbae3db0e6d3a9ee31d96dcc4c1f184
bloque 06: 9b925dc3e8b267830f1585ea6f458fb2

comparacion simple de repeticion
bloques repetidos ecb: 5
bloques repetidos cbc: 0
```

### 2.4 Vector de Inicialización (IV) (4 puntos)

**Pregunta: ¿Qué es el IV y por qué es necesario en CBC pero no en ECB?**

**Requisitos:**
o Implemente un experimento: cifre el mismo mensaje dos veces con CBC usando:  
o El mismo IV  
o IVs diferentes  
o Muestre cómo los cifrados resultantes son diferentes en el caso 2  
o Explique qué pasaría si un atacante intercepta mensajes cifrados con el mismo IV

#### ¿Qué es el IV y por qué es necesario en CBC pero no en ECB?

el iv es un bloque de bytes aleatorio que se usa como punto de arranque en modos encadenados como cbc. su objetivo es que aunque el mismo mensaje se cifre con la misma clave, el resultado sea diferente cada vez. ssi un atacante intercepta mensajes cifrados con el mismo IV y la misma clave, puede identificar que los mensajes comienzan con el mismo bloque de texto plano, ya que el primer bloque cifrado será idéntico en ambos casos.

- en **cbc**, el primer bloque del plaintext se combina con el iv antes de cifrar. por eso el iv es necesario: evita que dos cifrados del mismo mensaje arranquen igual.
- en **ecb**, cada bloque se cifra independiente y no existe encadenamiento, por eso ecb no usa iv. el problema es que ecb filtra patrones.

---

#### experimento con aes cbc: mismo iv vs iv diferente

para demostrarlo, se cifra el mismo mensaje dos veces con la misma clave:

1. usando el mismo iv
2. usando ivs diferentes

```bash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import sys


rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import generarClaveAes256, generarIvAes


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

```

#### Resultado del codigo

```bash
caso 1 mismo iv
iv: 86cea20a6580938b2ed971c0ae49553c
cbc1: ad28a8e310bb89a6d7596ddebe1adc1ae5c28ac0d6320f913633517d280eb020
cbc2: ad28a8e310bb89a6d7596ddebe1adc1ae5c28ac0d6320f913633517d280eb020
cbc1 igual a cbc2: True
--------------------------------------------------
caso 2 ivs diferentes
iv1: 4bca4bb66060a5a14d7865218269e600
iv2: 9fde9e63c7ceb5b712fc5f444aff977a
cbc3: 98a9c786b98bca90d3dd07fd5467d9f78932abf9624f3bd8c5026ba8f4a5ab90
cbc4: f019b573953170d3e9d66196276a354532b55f9f533082d63fba4a61f1034872
cbc3 igual a cbc4: False
```

### 2.5 Padding (3 puntos)

**Pregunta: ¿Qué es el padding y por qué es necesario?**

**Requisitos:**
• Muestre el resultado de su función pkcs7_pad con diferentes mensajes:  
o Mensaje de 5 bytes  
o Mensaje de 8 bytes (exactamente un bloque de DES)  
o Mensaje de 10 bytes  
o Explique byte por byte qué se agregó en cada caso  
o Demuestre que su función pkcs7_unpad recupera el mensaje original

#### ¿Qué es el padding y por qué es necesario?

el padding es un relleno que se agrega al final de un mensaje para que su longitud sea multiplo del tamano de bloque del cifrado. por ejemplo, des trabaja con bloques de 8 bytes, entonces si el mensaje no mide 8, 16, 24, etc, hay que completarlo para poder cifrar.
pkcs7 define una regla estandar que dice que se agregan n bytes, y cada uno de esos bytes vale n. si el mensaje ya es multiplo exacto del bloque, se agrega un bloque completo de padding.

---

#### demostracion con mi pkcs7_pad y pkcs7_unpad

```bash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import sys


rutaRaiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if rutaRaiz not in sys.path:
    sys.path.insert(0, rutaRaiz)

from src.utils import generarClaveAes256, generarIvAes


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
```

#### Resultado del codigo

```bash
caso 1 mensaje de 5 bytes
mensaje original bytes: 5
mensaje original hex: 6162636465
mensaje padded bytes: 8
mensaje padded hex: 6162636465030303
recuperado bytes: 5
recuperado hex: 6162636465
recuperado igual al original: True
--------------------------------------------------
caso 2 mensaje de 8 bytes
mensaje original bytes: 8
mensaje original hex: 6162636465666768
mensaje padded bytes: 16
mensaje padded hex: 61626364656667680808080808080808
recuperado bytes: 8
recuperado hex: 6162636465666768
recuperado igual al original: True
--------------------------------------------------
caso 3 mensaje de 10 bytes
mensaje original bytes: 10
mensaje original hex: 6162636465666768696a
mensaje padded bytes: 16
mensaje padded hex: 6162636465666768696a060606060606
recuperado bytes: 10
recuperado hex: 6162636465666768696a
recuperado igual al original: True
--------------------------------------------------
```

### 2.6 Recomendaciones de Uso (3 puntos)

**Pregunta: ¿En qué situaciones se recomienda cada modo de operación? ¿Cómo elegir un modo seguro
en cada lenguaje de programación?**

**Requisitos:**
o Tabla comparativa de modos (ECB, CBC, CTR, GCM)  
o Para cada modo: casos de uso recomendados y desventajas  
o Código de ejemplo en al menos 2 lenguajes diferentes mostrando cómo usar un modo seguro  
o Mención específica a modos AEAD como GCM

#### tabla comparativa de modos

se utilizo chatgpt y fuentes externas para llegar a estas respuestas y resultados de codigos

- MAC = Message Authentication Code
- AEAD = Authenticated Encryption with Associated Data

| modo | se recomienda para                                                           | desventajas principales                                                                     | nota de seguridad                   |
| ---- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------------- |
| ecb  | casi nunca, solo pruebas o datos totalmente aleatorios sin estructura        | filtra patrones, bloques iguales producen cifrados iguales                                  | no usar en datos sensibles          |
| cbc  | compatibilidad con sistemas legados y cifrado de archivos cuando no hay aead | requiere iv aleatorio unico, no da integridad, vulnerable a padding oracle si se maneja mal | usar con mac o preferir aead        |
| ctr  | cifrado tipo streaming y alto rendimiento en datos grandes                   | requiere nonce, no da integridad, reutilizar nonce rompe seguridad                          | combinar con mac o preferir aead    |
| gcm  | cifrado moderno recomendado para casi todo como api, archivos, mensajes      | requiere nonce unico, manejo correcto de tag                                                | aead: confidencialidad + integridad |

---

#### casos de uso recomendados y desventajas

- **ecb**
  - casos de uso: practicas academicas, pruebas internas
  - desventajas: revela patrones y estructura, inseguro para datos sensibles

- **cbc**
  - casos de uso: cifrado de archivos en sistemas legados, interoperabilidad
  - desventajas: no incluye integridad, necesita iv aleatorio, mal manejo puede permitir padding oracle

- **ctr**
  - casos de uso: streaming, cifrado por bloques grandes, escenarios donde se quiere paralelo
  - desventajas: no incluye integridad, requiere nonce unico, si se reutiliza nonce se compromete seguridad

- **gcm**
  - casos de uso: recomendado por defecto para datos sensibles, comunicaciones, almacenamiento, apis
  - desventajas: requiere nonce unico y guardar/verificar tag correctamente

---

#### Codigo de Ejemplos

#### Ejemplo python

```bash
from Crypto.Cipher import AES
import secrets


def cifrarAesGcm(plaintext: bytes, clave: bytes) -> tuple[bytes, bytes, bytes]:
    nonce = secrets.token_bytes(12)
    cipher = AES.new(clave, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce, ciphertext, tag


def descifrarAesGcm(nonce: bytes, ciphertext: bytes, tag: bytes, clave: bytes) -> bytes:
    cipher = AES.new(clave, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

```

#### Ejemplo Javascript

```bash
const crypto = require("crypto");

function cifrarAesGcm(plainText, clave) {
  const nonce = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv("aes-256-gcm", clave, nonce);
  const cipherText = Buffer.concat([cipher.update(plainText), cipher.final()]);
  const tag = cipher.getAuthTag();

  return { nonce, ciphertext: cipherText, tag };
}

function descifrarAesGcm(nonce, ciphertext, tag, clave) {
  const decipher = crypto.createDecipheriv("aes-256-gcm", clave, nonce);
  decipher.setAuthTag(tag);

  return Buffer.concat([decipher.update(ciphertext), decipher.final()]);
}
```

## Parte 3: Validación y Pruebas (10 puntos)

### 3.1 Implementación de Modo CTR (5 puntos extra)

**Implemente el modo CTR (Counter) para AES y compare su funcionamiento con ECB y CBC:**
o Implementación completa de cifrado/descifrado en modo CTR  
o Demostración de que CTR no requiere padding  
o Comparación de rendimiento: mida el tiempo de cifrado de un archivo de 10MB con CBC vs CTR  
o Análisis de paralelización: explique por qué CTR puede paralelizarse y CBC no

#### implementacion completa de cifrado y descifrado en modo ctr

se implemento aes ctr usando una clave de 256 bits (32 bytes). en ctr, cifrar y descifrar usan la misma operacion porque el modo genera un keystream y se aplica xor.

```bash
mensaje bytes: 22
cbc bytes: 32
ctr bytes: 22
ctr no requiere padding porque mantiene longitud igual al mensaje
--------------------------------------------------
round trip cbc ok: True
round trip ctr ok: True
--------------------------------------------------
benchmark 10mb
tiempo cbc segundos: 0.030528
tiempo ctr segundos: 0.011635
```

### analisis de paralelizacion

En modo ctr cada bloque se cifra usando un keystream que depende unicamente del nonce y del contador, por lo que cada bloque puede procesarse de forma independiente. Esto permite que ctr pueda paralelizarse usando multiples hilos o gpu y tambien permite acceso aleatorio a bloques especificos sin necesidad de procesar los anteriores. Por otro lado en modo cbc cada bloque depende del bloque cifrado anterior debido al encadenamiento, lo que obliga a procesar la informacion de manera secuencial y evita que el cifrado pueda paralelizarse.

### Referencias

- National Institute of Standards and Technology. (2001). _FIPS PUB 197: Advanced Encryption Standard (AES)_. U.S. Department of Commerce. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

- Dworkin, M. (2001). _Recommendation for Block Cipher Modes of Operation: Methods and Techniques (NIST Special Publication 800-38A)_. National Institute of Standards and Technology. https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38a.pdf

- Dworkin, M. (2007). _Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC (NIST Special Publication 800-38D)_. National Institute of Standards and Technology. https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38d.pdf

- National Institute of Standards and Technology. (1999). _FIPS PUB 46-3: Data Encryption Standard (DES)_. U.S. Department of Commerce. https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf

- Barker, E., & Mouha, N. (2017). _Recommendation for the Triple Data Encryption Algorithm (TDEA) Block Cipher (NIST Special Publication 800-67 Revision 2)_. National Institute of Standards and Technology. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-67r2.pdf

- Housley, R. (2009). _Cryptographic Message Syntax (CMS) (RFC 5652)_. Internet Engineering Task Force (IETF). https://datatracker.ietf.org/doc/html/rfc5652

- PyCryptodome Contributors. (n.d.). _AES cipher (PyCryptodome documentation)_. PyCryptodome. https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

- PyCryptodome Contributors. (n.d.). _Crypto.Util.Padding: pad and unpad (PyCryptodome documentation)_. PyCryptodome. https://pycryptodome.readthedocs.io/en/latest/src/util/util.html

- OpenAI. (2026). ChatGPT (gpt-5.2). https://chat.openai.com
