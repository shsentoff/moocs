from Transaction import Transaction
import CryptoUtil


COINBASE = 25.0


class Block(object):
    '''
    A block in the blockchain.
    '''

    def __init__(self, prevHash, address):
        '''
        Create a new block. Include the coinbase transaction, with output sent to address.
        '''
        self.blockHash = b''
        self.prevBlockHash = prevHash
        self.coinbase = Transaction(coin=COINBASE, address=address)
        self.txs = []

    def getCoinbase(self):
        return self.coinbase
    
    def getHash(self):
        return self.blockHash
 
    def getPrevBlockHash(self):
        return self.prevBlockHash
    
    def getTransactions(self):
        return self.txs
    
    def getTransaction(self, index):
        return self.txs[index]
    
    def addTransaction(self, tx):
        self.txs.append(tx)
        
    def getRawBlock(self):
        raw = b''
        if not self.prevBlockHash is None:
            raw += self.prevBlockHash
        for tx in self.txs:
            raw += tx.getRawTx()
        return raw
    
    def finalize(self):
        self.blockHash = CryptoUtil.digest(self.getRawBlock())
                