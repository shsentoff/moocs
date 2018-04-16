import unittest
import CryptoUtil
from Block import Block
from Block import COINBASE
from BlockChain import CUT_OFF_AGE
from BlockChain import BlockChain
from Transaction import Transaction
from BlockHandler import BlockHandler


scroogeKeyPair = CryptoUtil.genKeyPair()
scroogePriKey = CryptoUtil.getPrivateKey(scroogeKeyPair)
scroogePubKey = CryptoUtil.getPublicKey(scroogeKeyPair)

def signInput(tx, priKey, index):
    tx.addSignature(CryptoUtil.signMessage(priKey, tx.getRawDataToSign(index)), index)


class BlockChainTest(unittest.TestCase):

    def testMethods(self):
        genesis = Block(b'', scroogePubKey)
        genesis.finalize()
        blockChain = BlockChain(genesis)
        blockHandler = BlockHandler(blockChain)
        
        # Genesis block test
        self.assertEqual(genesis.getHash(), blockChain.getMaxHeightBlock().getHash(), \
                         'genesis should be max height block')
        self.assertEqual(blockChain.getMaxHeightBlock(), genesis, \
                         'genesis should be max height block')
        self.assertEqual(len(blockChain.getMaxHeightUTXOPool().getAllUTXO()), 1, \
                         'UTXOPool should have one output')
        self.assertEqual(len(blockChain.getTransactionPool().getTransactions()), 0, \
                         'transaction pool should be empty')

        # Spend the genesis coinbase transaction in many outputs
        tx = Transaction()
        tx.addInput(genesis.getCoinbase().getHash(), 0)
        numGenOuts = int(COINBASE)
        for i in range(numGenOuts):
            tx.addOutput(1.0, scroogePubKey)
        signInput(tx, scroogePriKey, 0)
        tx.finalize()
        
        # Add one transaction test. No block has been added.
        blockHandler.processTx(tx)       
        self.assertEqual(blockChain.getMaxHeightBlock(), genesis, \
                         'genesis should be max height block')
        self.assertEqual(len(blockChain.getMaxHeightUTXOPool().getAllUTXO()), 1, \
                         'UTXOPool should have one output')
        self.assertEqual(len(blockChain.getTransactionPool().getTransactions()), 1, \
                         'transaction pool should have one entry')
        self.assertIsNotNone(blockChain.getTransactionPool().getTransaction(tx.getHash()), \
                            'tx should be in txPool')
        
        # Build out the chain
        depth = 15;
        chainedBlocks = []
        for i in range(depth):
            # Spend the new outputs, one tx per block
            tx2 = Transaction()
            tx2.addInput(tx.getHash(), i)
            tx2.addOutput(1.0, scroogePubKey)
            signInput(tx2, scroogePriKey, 0)
            tx2.finalize()
            blockHandler.processTx(tx2);
            chainedBlocks.append(blockHandler.createBlock(scroogePubKey))
            
            # Deep chain test
            self.assertIsNotNone(chainedBlocks[i], 'ith block should exist')
            self.assertEqual(blockChain.getMaxHeightBlock(), chainedBlocks[i], \
                             'ith block should be max height')
            self.assertEqual(len(blockChain.getMaxHeightUTXOPool().getAllUTXO()), numGenOuts + i + 1, \
                             'wrong number UTXOs when i = ' + str(i))
            self.assertEqual(len(blockChain.getTransactionPool().getTransactions()), 0, \
                             'txPool should be empty')
        
        # Remember the current max height block
        maxBlockBefore = blockChain.getMaxHeightBlock()
        
        # Make another block on the deepest block that should still work
        sideBlock = Block(chainedBlocks[depth - CUT_OFF_AGE - 1].getHash(), scroogePubKey)
        sideBlock.finalize()
        retVal = blockChain.addBlock(sideBlock)
        
        # Add valid side chain block test
        self.assertTrue(retVal, 'side block should have been added')
        self.assertEqual(blockChain.getMaxHeightBlock(), maxBlockBefore, \
                         'max height block should not have changed')
        
        # Make another block that is too deep
        tooDeep = Block(chainedBlocks[depth - CUT_OFF_AGE - 2].getHash(), scroogePubKey)
        tooDeep.finalize()
        retVal2 = blockChain.addBlock(tooDeep)
        
        # Too deep test
        self.assertFalse(retVal2, 'too deep block should not be added')
 
        # Build on the side chain
        prevBlock = sideBlock
        for i in range(CUT_OFF_AGE - 1):
            # Spend the previous coinbase transaction
            tx2 = Transaction();
            tx2.addInput(prevBlock.getCoinbase().getHash(), 0)
            tx2.addOutput(10.0, scroogePubKey)
            signInput(tx2, scroogePriKey, 0)
            tx2.finalize();
            
            newBlock = Block(prevBlock.getHash(), scroogePubKey)
            newBlock.addTransaction(tx2)
            newBlock.finalize()
            retVal3 = blockChain.addBlock(newBlock)
            
            self.assertTrue(retVal3, 'side blocks should be added')
            
            prevBlock = newBlock
            
        # The side chain should be the same length as the previous chain
        # and so the max height block should not have changed.
        self.assertEqual(blockChain.getMaxHeightBlock(), maxBlockBefore, \
                    'max height block should not be changed')
        
        # Now add another to the side chain, making it the new highest
        # Spend the previous coinbase transaction
        tx3 = Transaction()
        tx3.addInput(prevBlock.getCoinbase().getHash(), 0)
        tx3.addOutput(10.0, scroogePubKey)
        signInput(tx3, scroogePriKey, 0)
        tx3.finalize()
        
        newBlock = Block(prevBlock.getHash(), scroogePubKey)
        newBlock.addTransaction(tx3)
        newBlock.finalize()
        retVal3 = blockChain.addBlock(newBlock)
        
        self.assertTrue(retVal3, 'block should be added')
        self.assertNotEqual(blockChain.getMaxHeightBlock(), maxBlockBefore, \
                         'max height block should be changed')
        self.assertEqual(blockChain.getMaxHeightBlock(), newBlock, \
                         'max height block should be the new block')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
