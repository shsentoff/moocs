class UTXOPool(object):
    '''
    A pool of UTXOs.
    '''

    def __init__(self):
        '''
        Create a new empty UTXO pool.
        '''
        self.pooldict = {}

    def copy(self):
        '''
        Create a new UTXO pool that is a copy of the old one.
        '''
        newPool = UTXOPool()
        newPool.pooldict = self.pooldict.copy()
        return newPool

    def addUTXO(self, utxo, txOutput):
        '''
        Add a UTXO and its associated transaction output to the pool.
        utxo should be a tuple made by UTXO.UTXO.
        txOutput should be a reference to a Transaction.Output object.
        '''
        self.pooldict[utxo] = txOutput
    
    def removeUTXO(self, utxo):
        '''
        Remove a UTXO from the pool.
        utxo should be a tuple made by UTXO.UTXO.
        '''
        if utxo in self.pooldict:
            del self.pooldict[utxo]
    
    def getTxOutput(self, utxo):
        '''
        Get the Transaction.Output object associated with this UTXO.
        utxo should be a tuple made by UTXO.UTXO.
        '''
        if utxo in self.pooldict:
            return self.pooldict[utxo]
        else:
            return None
    
    def contains(self, utxo):
        '''
        Determines whether a UTXO is in the pool.
        utxo should be a tuple made by UTXO.UTXO.
        '''
        return utxo in self.pooldict
    
    def getAllUTXO(self):
        '''
        Return a copy of all the tuples representing the UTXOs in the pool.
        '''
        return list(self.pooldict.keys())
