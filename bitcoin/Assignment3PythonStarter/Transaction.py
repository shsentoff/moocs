import CryptoUtil
from Crypto.Random import random


class Transaction(object):
    '''
    A transaction.
    '''

    class Input(object):
        '''
        An input of a transaction
        '''

        def __init__(self, prevTxHash, index):
            '''
            Create a transaction input.
            prevTxHash should be a bytes object representing the hash of the transaction
            that created the output.
            index should be an integer indexing the outputs of that transaction.
            '''
            self.prevTxHash = prevTxHash
            self.index = index
            self.signature = None
            
        def addSignature(self, sig):
            '''
            Add the signature for this input.
            sig should be a bytes object representing the signature for this input.
            '''
            if sig is None:
                self.signature = b''
            else:
                self.signature = sig

    class Output(object):
        '''
        An output of a transaction
        '''

        def __init__(self, value, address):
            '''
            Create a transaction output.
            value should be a decimal number of bitcoins.
            address should be a publicKey as obtained from CryptoUtil.extractPublicKey.
            '''
            self.value = value
            self.address = address
            
    def __init__(self, coin=None, address=None):
        '''
        Create a new empty transaction, or a new coinbase transaction with the
        given parameters.
        '''
        if address is None:
            self.hash = b''
            self.inputs = []
            self.outputs = []
            self.coinbase = False
        else:
            # Create a dummy input with a nonce.
            dummyInput = Transaction.Input(b'coinbase', random.randint(0, 1000000000))
            self.inputs = [dummyInput]
            self.outputs = []
            self.addOutput(coin, address)
            self.addSignature(b'', 0)
            self.finalize()
            self.coinbase = True
     
    def copy(self):
        '''
        Create a new transaction that is a copy of the old one.
        '''
        newTx = Transaction()
        newTx.hash = self.hash
        newTx.inputs = self.inputs.copy()
        newTx.outputs = self.outputs.copy()
        return newTx
    
    def isCoinbase(self):
        return self.coinbase

    def addInput(self, prevTxHash, index):
        '''
        Add an input to this transaction's list of inputs.
        prevTxHash should be a bytes object representing the hash of the transaction
        that created the output.
        index should be an integer indexing the outputs of that transaction.
        '''
        txInput = Transaction.Input(prevTxHash, index)
        self.inputs.append(txInput)
        
    def addOutput(self, value, address):
        '''
        Add an output to this transaction's list of outputs.
        value should be a decimal number of bitcoins.
        address should be a publicKey as obtained from CryptoUtil.extractPublicKey.
        '''
        txOutput = Transaction.Output(value, address)
        self.outputs.append(txOutput)

    def getRawDataToSign(self, i):
        '''
        Get the bytes object of the raw data for the ith input
        and all the outputs of the transaction.
        '''
        raw = b''
        
        if i > len(self.inputs):
            return raw
        
        raw += self.inputs[i].prevTxHash
        raw += str(self.inputs[i].index).encode()
        
        for outp in self.outputs:
            raw += str(outp.value).encode()
            raw += outp.address.exportKey()
        
        return raw
        
    def getRawTx(self):
        '''
        Returns the bytes object of the raw data in the transaction
        '''
        raw = b''
        
        for inp in self.inputs:
            raw += inp.prevTxHash
            raw += str(inp.index).encode()
            raw += str(inp.signature).encode()
            
        for outp in self.outputs:
            raw += str(outp.value).encode()
            raw += outp.address.exportKey()
        
        return raw
    
    def finalize(self):
        '''
        Compute and add the hash to this transaction.
        '''

        self.hash = CryptoUtil.digest(self.getRawTx())

    def addSignature(self, signature, index):
        '''
        Add the signature for the input at index.
        signature should be the object obtained by CryptoUtil.signMessage.
        '''
        self.inputs[index].addSignature(signature)
        
    def getHash(self):
        '''
        Get this transaction's hash.
        '''
        return self.hash
    
    def getInput(self, index):
        '''
        Get the Transaction.Input at index.
        '''
        if index < len(self.inputs):
            return self.inputs[index]
        else:
            return None
        
    def getOutput(self, index):
        '''
        Get the Transaction.Output at index.
        '''
        if index < len(self.outputs):
            return self.outputs[index]
        else:
            return None
        
    def numInputs(self):
        return len(self.inputs)
    
    def numOutputs(self):
        return len(self.outputs)
    
    def getInputs(self):
        return self.inputs
    
    def getOutputs(self):
        return self.outputs
