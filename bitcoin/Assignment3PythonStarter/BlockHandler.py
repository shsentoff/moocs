from Block import Block
from TxHandler import TxHandler


class BlockHandler(object):
    '''
    A handler to process a blockchain.
    '''

    def __init__(self, blockChain):
        '''
        Create a new handler.
        '''
        self.blockChain = blockChain
        
    def processBlock(self, block):
        '''
        Add the block to the blockchain, if it is valid.
        Return true if block was added, false otherwise.
        '''
        if block is None:
            return False
        else:
            return self.blockChain.addBlock(block)
        
    def createBlock(self, myAddress):
        '''
        Create a new block over the max height block.
        '''
        parent = self.blockChain.getMaxHeightBlock()
        parentHash = parent.getHash()
        current = Block(parentHash, myAddress)
        uPool = self.blockChain.getMaxHeightUTXOPool()
        txPool = self.blockChain.getTransactionPool()
        handler = TxHandler(uPool)
        txs = txPool.getTransactions()
        rTxs = handler.handleTxs(txs)
        for tx in rTxs:
            current.addTransaction(tx)
        current.finalize()
        
        if self.blockChain.addBlock(current):
            return current
        else:
            return None
        
    def processTx(self, tx):
        self.blockChain.addTransaction(tx)
        