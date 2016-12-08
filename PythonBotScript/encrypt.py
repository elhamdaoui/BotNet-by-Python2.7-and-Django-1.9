from Crypto.PublicKey import RSA
import base64


def encrypt(message):
    with open('keys/pub', 'r') as contenu:
        fich_pub = publiq.read()
    keyPub = RSA.importKey(fich_pub)
    msg_crypte = keyPub.encrypt(str(message), 32)
    return base64.b64encode(msg_crypte[0])
