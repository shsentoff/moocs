import os
import Crypto.PublicKey.RSA
import Crypto.Hash.SHA256

'''
Helpful routines for signing and verifying message signatures
'''

def digest(message):
    digester = Crypto.Hash.SHA256.new()
    digester.update(message)
    return digester.digest()

def genKeyPair():
    return Crypto.PublicKey.RSA.generate(1024, os.urandom)

def getPrivateKey(keyPair):
    return keyPair

def getPublicKey(keyPair):
    return keyPair.publickey()
    
def signMessage(key, message):
    '''
    Sign a message with a private key
    key must be an RSA.PublicKey object holding the private key
    '''
    # Compute hash of message
    h = digest(message)
    
    # Get the signature
    return key.sign(h, '')
 
def verifySignature(pubKey, message, signature):
    '''
    Returns True iff the signature is verified for the given message
    and public key.
    pubKey is a bytes object containing the PEM encoded public key.
    signature is a bytes object with the signature.
    '''
    # Compute the hash of the message
    h = digest(message)
    
    return pubKey.verify(h, signature)
