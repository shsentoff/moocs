class TransactionPool(object):
    '''
    A pool of available transactions, indexed by their hashes.
    '''

    def __init__(self):
        '''
        Create the empty pool.
        '''
        self.txdict = {}
        
    def copy(self):
        newPool = TransactionPool()
        newPool.txdict = self.txdict.copy()
        return newPool
        
    def addTransaction(self, tx):
        self.txdict[tx.getHash()] = tx
        
    def removeTransaction(self, tx):
        if tx.getHash() in self.txdict:
            del self.txdict[tx.getHash()]
            
    def getTransaction(self, txHash):
        if txHash in self.txdict:
            return self.txdict[txHash]
        else:
            return None
    
    def getTransactions(self):
        return list(self.txdict.values())
