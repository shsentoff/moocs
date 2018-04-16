import unittest
import Crypto.PublicKey.RSA
import CryptoUtil
from Transaction import Transaction
from UTXOPool import UTXOPool
from UTXO import UTXO
from MaxFeeTxHandler import MaxFeeTxHandler

'''
This is a test suite for the Extra Credit Project.
'''

# Use a fixed Scrooge key for the testing.
exportedKey = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCyvh9t+A9qWzUZL2fPuh' + \
    b'//LhAdnuRtnaG8slkrXo3AaTufedCH\nO+1kbz8csCeo0iQl0y4mQVW3Z3I3VWl/CGRFE9eSNw3gh' + \
    b'doIYRB6dfo46kDY7GVf\ncYnSR7fR/LEBcKQ48HpxX8S8dMy/zkbfIFEB9tVsZz9wOvleJmib2igEY' + \
    b'wIDAQAB\nAoGAUohRUODKlWx57yAhihxCK/zj+hllFmxDwzKC0/C7+U1d93wy2k7EhayMcr2w\nAlb' + \
    b'N1B1X4NgoMSB177DjnoGMckX1r8A4jrvSDDqymyqQxsBHvYrMuzdLmNql8uHW\nSPp1HnKYyaOJGEW' + \
    b'aevQmv2Hb0uu53gxWEvAEQUYJt0QFNKECQQC9KQfwM9FamgQR\niPAQLOCEAGIEr9a/zHjR9IkVfzT' + \
    b'88zyMUNnnn8xBM96kDfpVKR5ge/Ahja179i9G\nG1jCFNGRAkEA8ea9mCOGIo4osriiM6/pRZn+zmD' + \
    b'cQDhV9s0CTMtlJvxykVO18EQs\nWlHJpmWQqAmn4d8TM1xxJrf7acOcdwO8swJATsgq/TinpeNldGQ' + \
    b'jD6mRLIj4Sdlu\nSF2BqHf/LAvZ5svrWMlHp/de230d6hfEPfmtJCQaQ+885NcIo1s6YULIcQJBAMd' + \
    b't\noXUiJF2ssaTWTvMp3blCAi4G8M4JI+X6kiDZtqTzj0h8qQxSR/aWYxbJuP6wJzYy\nANRhK+/t0' + \
    b'loZqI7+B70CQH2LLsccb1MHAkAGRqDZjtAfFAt7p7IaNeEp0jo4TcvK\ny50t2C9i5aa5tY6TFp4pQ' + \
    b'3Vfk6l+21J6e5BKari9wfY=\n-----END RSA PRIVATE KEY-----'
scroogePrivK = Crypto.PublicKey.RSA.importKey(exportedKey)
scroogePubK = CryptoUtil.getPublicKey(scroogePrivK)
keyPair = CryptoUtil.genKeyPair()
alicePrivK = CryptoUtil.getPrivateKey(keyPair)
alicePubK = CryptoUtil.getPublicKey(keyPair)

# Make a genesis transaction
genesis = Transaction()
genesisValue = 25.0
genesis.addOutput(genesisValue, scroogePubK)
genesis.finalize()

# Make an initial pool
initialPool = UTXOPool()
utxo = UTXO(genesis.getHash(), 0)
initialPool.addUTXO(utxo, genesis.getOutput(0))

# Note this transaction is not valid -- one of its inputs does not exist
tx2in2out = Transaction()
tx2in2out.addInput(genesis.hash, 0)
tx2in2out.addInput(genesis.hash, 1)
tx2in2out.addOutput(10.0, scroogePubK)
tx2in2out.addOutput(15.0, scroogePubK)
raw0 = tx2in2out.getRawDataToSign(0)
sig0 = CryptoUtil.signMessage(scroogePrivK, raw0)
tx2in2out.addSignature(sig0, 0)
raw1 = tx2in2out.getRawDataToSign(1)
sig1 = CryptoUtil.signMessage(scroogePrivK, raw1)
tx2in2out.addSignature(sig1, 1)
tx2in2out.finalize()

txValid = Transaction()
txValid.addInput(genesis.getHash(), 0)
txValid.addOutput(10.0, scroogePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txValid.getRawDataToSign(0))
txValid.addSignature(sig, 0)
txValid.finalize()

txBadInput = Transaction()
txBadInput.addInput(genesis.getHash(), 1)
txBadInput.addOutput(10.0, scroogePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txBadInput.getRawDataToSign(0))
txBadInput.addSignature(sig, 0)
txBadInput.finalize()

txBadSig = Transaction()
txBadSig.addInput(genesis.getHash(), 0)
txBadSig.addOutput(10.0, alicePubK)
sig = CryptoUtil.signMessage(alicePrivK, txBadSig.getRawDataToSign(0))
txBadSig.addSignature(sig, 0)
txBadSig.finalize()

txDoubleInput = Transaction()
txDoubleInput.addInput(genesis.getHash(), 0)
txDoubleInput.addInput(genesis.getHash(), 0)
txDoubleInput.addOutput(10.0, alicePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txDoubleInput.getRawDataToSign(0))
txDoubleInput.addSignature(sig, 0)
sig = CryptoUtil.signMessage(scroogePrivK, txDoubleInput.getRawDataToSign(1))
txDoubleInput.addSignature(sig, 1)
txDoubleInput.finalize()

txNegOut = Transaction()
txNegOut.addInput(genesis.getHash(), 0)
txNegOut.addOutput(-10.0, scroogePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txNegOut.getRawDataToSign(0))
txNegOut.addSignature(sig, 0)
txNegOut.finalize()

txTooMuch = Transaction()
txTooMuch.addInput(genesis.getHash(), 0)
txTooMuch.addOutput(50.0, scroogePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txTooMuch.getRawDataToSign(0))
txTooMuch.addSignature(sig, 0)
txTooMuch.finalize()

txA = Transaction()
txA.addInput(genesis.getHash(), 0)
txA.addOutput(10.0, alicePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txA.getRawDataToSign(0))
txA.addSignature(sig, 0)
txA.finalize()

txB = Transaction()
txB.addInput(txA.getHash(), 0)
txB.addOutput(7.0, scroogePubK)
sig = CryptoUtil.signMessage(alicePrivK, txB.getRawDataToSign(0))
txB.addSignature(sig, 0)
txB.finalize()

txC = Transaction()
txC.addInput(txA.getHash(), 0)
txC.addOutput(8.0, scroogePubK)
sig = CryptoUtil.signMessage(alicePrivK, txC.getRawDataToSign(0))
txC.addSignature(sig, 0)
txC.finalize()

txD = Transaction()
txD.addInput(txB.getHash(), 0)
txD.addOutput(6.0, alicePubK)
sig = CryptoUtil.signMessage(scroogePrivK, txD.getRawDataToSign(0))
txD.addSignature(sig, 0)
txD.finalize()

ans1 = sorted([tx.getHash() for tx in [txA, txB, txD]])
ans2 = sorted([tx.getHash() for tx in [txA, txC]])


def addTx(pool, tx):
    # Remove the transaction's inputs
    for inp in tx.getInputs():
        u = UTXO(inp.prevTxHash, inp.index)
        pool.remove(u)
    
    # Add the outputs
    for i in range(tx.numOutputs()):
        u = UTXO(tx.getHash(), i)
        pool.addUTXO(u, tx.getOutput(i))

        
def signInput(tx, privKey, index):
    tx.addSignature(CryptoUtil.signMessage(privKey, tx.getRawDataToSign(index)), index)

    
def makeConflictingTree(root, pubK, priK, depth):
    ret = []
    if depth > 0:
        prevOut = root.getOutput(0)
        prevVal = prevOut.value
        for i in range(2):
            tx = Transaction()
            tx.addInput(root.getHash(), 0)
            tx.addOutput(prevVal * 0.3 * (i + 1), pubK)
            signInput(tx, priK, 0)
            tx.finalize()
            ret.append(tx)
            for tx2 in makeConflictingTree(tx, pubK, priK, depth - 1):
                ret.append(tx2)
                
    return ret

                     
class MaxFeeTxHandlerTest(unittest.TestCase):

    def testIsValidWithValidTx(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertTrue(handler.isValidTx(txValid), 'valid tx was called invalid')
         
    def testIsValidWithBadInput(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txBadInput), 'bad input not detected')
 
    def testIsValidWithBadSignature(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txBadSig), 'bad signature not detected')
         
    def testIsValidWithDoubleInput(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txDoubleInput), 'double input not detected')
         
    def testIsValidWithNegativeOutput(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txNegOut), 'negative output not detected')
         
    def testIsValidWithOutGreaterThanIn(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txTooMuch), 'outputs > inputs not detected')
         
    def testHandleTxsWithNoTx(self):
        handler = MaxFeeTxHandler(initialPool)
        self.assertEqual(handler.handleTxs([]), [], 'should return empty list')
         
    def testHandleTxsWithOneTx(self):
        handler = MaxFeeTxHandler(initialPool)
        accepted = handler.handleTxs([txValid])
        self.assertEqual(len(accepted), 1, 'should return list with one transaction')
         
    def testHandleTxsAllInvalid(self):
        handler = MaxFeeTxHandler(initialPool)
        accepted = handler.handleTxs([genesis, txBadInput, txNegOut])
        self.assertEqual(len(accepted), 0, 'should return empty list')
         
    def testHandleTxsWithUtxoInPool(self):
        pool = initialPool.copy()
        utxo = UTXO(txA.getHash(), 0)
        pool.addUTXO(utxo, txA.getOutput(0))
        handler = MaxFeeTxHandler(pool)
        accepted = handler.handleTxs([txB])
        self.assertEqual(len(accepted), 1, 'should return list with one transaction')
         
    def testHandleTxsCheckPool(self):
        pool = initialPool.copy()
        utxo = UTXO(txA.getHash(), 0)
        pool.addUTXO(utxo, txA.getOutput(0))
        poolsize = len(pool.getAllUTXO())
        handler = MaxFeeTxHandler(pool)
        handler.handleTxs([txB])
        self.assertEqual(len(pool.getAllUTXO()), poolsize, 'pool should not be altered')
        self.assertTrue(utxo in pool.getAllUTXO(), 'pool should not be altered')
         
    def testHandleTxsDoubleSpending(self):
        handler = MaxFeeTxHandler(initialPool)
        accepted = handler.handleTxs([txA, txB, txC, txD])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1, 'wrong set')
         
    def testHandleTxsDoubleSpendingVaryOrder(self):
        handler = MaxFeeTxHandler(initialPool)
        accepted = handler.handleTxs([txA, txC, txB, txD])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1, 'wrong set')
         
    def testHandleTxsNeedMultiplePasses(self):
        handler = MaxFeeTxHandler(initialPool)
        accepted = handler.handleTxs([txC, txB, txD, txA])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1, 'wrong set')
         
    def testHandleTxsMixValidInvalid(self):
        handler = MaxFeeTxHandler(initialPool)
        accepted = handler.handleTxs([txC, genesis, txB, txNegOut,
                                      txD, txBadSig, txA, txD])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1, 'wrong set')
     
    def testGetUtxoPool(self):
        handler = MaxFeeTxHandler(initialPool)
        handler.handleTxs([txValid])
        utxos = handler.getUTXOPool().getAllUTXO()
        self.assertEqual(len(utxos), 1, 'pool should have one UTXO')
        self.assertTrue(UTXO(txValid.getHash(), 0) in utxos, 'should have the UTXO from the added tx')
         
    def testHandleTxsManyNonconflictingTxs(self):
        many = 30
        baseTx = Transaction()
        for i in range(many):
            baseTx.addOutput(1.0, scroogePubK)
        baseTx.finalize()
         
        # Add these outputs to the pool anyway
        pool = UTXOPool()
        addTx(pool, baseTx)
         
        # Make a bunch of transactions that depend on that one.
        possibleTxs = []
        for i in range(many):
            tx = Transaction()
            tx.addInput(baseTx.getHash(), i)
            tx.addOutput(0.5, alicePubK)
            signInput(tx, scroogePrivK, 0)
            tx.finalize()
            possibleTxs.append(tx)
             
        handler = MaxFeeTxHandler(pool)
        ret = handler.handleTxs(possibleTxs)
         
        self.assertEquals(len(ret), many, 'should return all transactions')
     
    def testHandleTxsConflictingBinaryTree(self):
        # Force search to all branches
        depth = 4
        handler = MaxFeeTxHandler(initialPool)
        
        proposedTxs = makeConflictingTree(genesis, scroogePubK, scroogePrivK, depth)
        ret = handler.handleTxs(proposedTxs)
        
        self.assertEqual(len(ret), depth, 'wrong number transactions')
        expectedVal = 25 * 0.3
        for i in range(len(ret)):
            outVal = ret[i].getOutput(0).value
            self.assertAlmostEqual(outVal, expectedVal, 6, 'wrong output value')
            expectedVal *= 0.3
        
    def testHandleTxsMessy(self):
        # Make the initial pool
        pool = UTXOPool()
        
        # Make the base transaction and put in pool
        baseTx = Transaction()
        baseTx.addOutput(10, scroogePubK)
        baseTx.addOutput(10, scroogePubK)
        baseTx.finalize()
        addTx(pool, baseTx)
        
        # Transaction A
        txA = Transaction()
        txA.addInput(baseTx.getHash(), 0)  # 10 in, conflicts with B and C
        txA.addOutput(7, scroogePubK)  # 7 out, fee = 3
        signInput(txA, scroogePrivK, 0)
        txA.finalize()
        
        # Transaction B
        txB = Transaction()
        txB.addInput(baseTx.getHash(), 0)  # 10 in, conflicts with A and C
        txB.addOutput(9, scroogePubK)  # 9 out, fee = 1
        signInput(txB, scroogePrivK, 0)
        txB.finalize()
        
        # Transaction C
        txC = Transaction()
        txC.addInput(baseTx.getHash(), 0)  # 10 in, conflicts with A and B
        txC.addInput(baseTx.getHash(), 1)  # 10 more in, conflicts with D
        txC.addOutput(5, scroogePubK)
        txC.addOutput(14, scroogePubK)  # 19 out, fee = 1
        signInput(txC, scroogePrivK, 0)
        signInput(txC, scroogePrivK, 1)
        txC.finalize()
        
        # Transaction D
        txD = Transaction()
        txD.addInput(baseTx.getHash(), 1)  # 10 in, conflicts with C
        txD.addOutput(9, scroogePubK)  # 9 out, fee = 1
        signInput(txD, scroogePrivK, 0)
        txD.finalize()
        
        # Transaction E
        txE = Transaction()
        txE.addInput(txA.getHash(), 0)  # 7 in, from A
        txE.addOutput(6, scroogePubK)  # 6 out, fee = 1
        signInput(txE, scroogePrivK, 0)
        txE.finalize()
        
        # Transaction F
        txF = Transaction()
        txF.addInput(txC.getHash(), 0)  # 5 in, from C
        txF.addOutput(4, scroogePubK)  # 4 out, fee = 1
        signInput(txF, scroogePrivK, 0)
        txF.finalize()

        # Transaction G
        txG = Transaction()
        txG.addInput(txB.getHash(), 0)  # 9 in, from B
        txG.addInput(txC.getHash(), 1)  # 14 in, from C
        txG.addOutput(8, scroogePubK)  # 8 out, fee = 15
        signInput(txG, scroogePrivK, 0)
        signInput(txG, scroogePrivK, 1)
        txG.finalize()
        
        # Transaction H
        txH = Transaction()
        txH.addInput(baseTx.getHash(), 0)  # 10 in
        txH.addOutput(4, scroogePubK)  # 4 out, fee = 6
        signInput(txH, alicePrivK, 0)  # But invalid, since wrong signature
        txH.finalize()
 
        # Transaction I
        txI = Transaction()
        txI.addInput(baseTx.getHash(), 2)  # no such input, so invalid
        txI.addOutput(4, scroogePubK)  # 4 out, fee = NA
        signInput(txI, scroogePrivK, 0)
        txI.finalize()

        # Transaction J
        txJ = Transaction()
        txJ.addInput(txI.getHash(), 0)  # 4 in (if txI were valid)
        txJ.addOutput(3, scroogePubK)  # 3 out, fee = 1
        signInput(txJ, scroogePrivK, 0)
        txJ.finalize()
        
        # Make the proposed transaction list
        proposedTxs = [txA, txB, txC, txD, txE, txF, txG, txH, txI, txJ]
        
        handler = MaxFeeTxHandler(pool)
        acceptedHashes = sorted([tx.getHash() for tx in handler.handleTxs(proposedTxs)])
        
        expectedHashes = sorted([tx.getHash() for tx in [txA, txD, txE]])
        self.assertEqual(acceptedHashes, expectedHashes, 'wrong set')

        # Make another proposed transaction list
        proposedTxs = [txB, txD, txH, txC, txF, txG, txI, txA, txE, txJ]
        
        handler = MaxFeeTxHandler(pool)
        acceptedHashes = sorted([tx.getHash() for tx in handler.handleTxs(proposedTxs)])
        
        self.assertEqual(acceptedHashes, expectedHashes, 'wrong set')

        # Make another proposed transaction list
        proposedTxs = [txC, txJ, txF, txD, txB, txE, txG, txH, txI, txA]
        
        handler = MaxFeeTxHandler(pool)
        acceptedHashes = sorted([tx.getHash() for tx in handler.handleTxs(proposedTxs)])
        
        self.assertEqual(acceptedHashes, expectedHashes, 'wrong set')

    
if __name__ == "__main__":
    unittest.main()
