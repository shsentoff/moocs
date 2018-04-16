from UTXOPool import UTXOPool
from UTXO import UTXO
from TransactionPool import TransactionPool
from TxHandler import TxHandler
import CryptoUtil
import Block


CUT_OFF_AGE = 10


class BlockChain(object):
    '''
    A block chain.
    '''

    def __init__(self, genesisBlock):
        '''
        Create the new BlockChain, with just the coinbase output.
        Adds genesisBlock without checking its validity.
        '''
        # TODO - implement this
        pass




    def getMaxHeightBlock(self):
        '''
        Get the maximum height block
        '''
        # TODO - implement this
        pass
        



    def getMaxHeightUTXOPool(self):
        '''
        Get the UTXOPool for mining a new block on top of max height block
        '''
        # TODO - implement this
        pass
    



    def getTransactionPool(self):
        '''
        Get the transaction pool to mine a new block on top of max height block
        '''
        # TODO - implement this
        pass



    
    def addBlock(self, block):
        '''
        Add block to the block chain if it is valid. For validity, all
        transactions should be valid and block should be at
        height > (maxHeight - CUT_OFF_AGE).
        
        For example, you can try creating a new block over the genesis block (block
        height 2) if the block chain height is <= CUT_OFF_AGE + 1.
        As soon as height > CUT_OFF_AGE + 1, you cannot create a new block at height 2.
        
        return true if block is successfully added
        '''
        # TODO - implement this
        pass
        



        
    def addTransaction(self, tx):
        '''
        Add a transaction to the transaction pool
        '''
        # TODO - implement this
        pass




