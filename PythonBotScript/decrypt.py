from Crypto.PublicKey import RSA
import base64

def decrypt(message):
    with open('keys/priv', 'r') as contenu:
        fich_priv = contenu.read()
    key_priv = RSA.importKey(fich_priv)
    try:
        message = base64.b64decode(message)
        return key_priv.decrypt(message)
    except:
        return message

