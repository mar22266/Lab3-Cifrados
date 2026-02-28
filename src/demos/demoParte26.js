const crypto = require("crypto");

// demo que muestra como cifrar y descifrar con aes gcm usando la libreria crypto de nodejs mostrando el nonce el tag y el texto cifrado en hex
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