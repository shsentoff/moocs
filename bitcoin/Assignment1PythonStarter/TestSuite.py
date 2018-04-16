import unittest
import Crypto.PublicKey.RSA
import CryptoUtil
from Transaction import Transaction
from UTXOPool import UTXOPool
from UTXO import UTXO
from TxHandler import TxHandler

'''
This is a test suite for the regular part of the assignment.
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


class CryptoUtilTest(unittest.TestCase):

    def testDigest(self):
        msg = b'1231232131'
        expected = b'\x9f\xb7&l\xd3{p\xc8j[\xcb\x89\xef\x19K9b\xc8\xaf\xbc\xca\x1d\x99\xf2\xeb\x89 \x1f\xb7\xe1\xd9\xf6'
        self.assertEqual(CryptoUtil.digest(msg), expected, 'incorrect digest')
    
    def testSignAndVerify(self):
        msg = b'1231232131'
        keyPair = CryptoUtil.genKeyPair()  
        privKey = CryptoUtil.getPrivateKey(keyPair)
        pubKey = CryptoUtil.getPublicKey(keyPair)
        sig = CryptoUtil.signMessage(privKey, msg)
        self.assertTrue(CryptoUtil.verifySignature(pubKey, msg, sig), 'correct signature not verified')
    
    def testBadSignature(self):
        msg = b'1231232131'
        keyPair = CryptoUtil.genKeyPair()  
        privKey = CryptoUtil.getPrivateKey(keyPair)
        sig = CryptoUtil.signMessage(privKey, msg)
        keyPair2 = CryptoUtil.genKeyPair()
        pubKey2 = CryptoUtil.getPublicKey(keyPair2)
        self.assertFalse(CryptoUtil.verifySignature(pubKey2, msg, sig), 'incorrect signature was verified as correct')       


class TransactionTest(unittest.TestCase):

    def testGenesisTransaction(self):
        expectedHash = b'\x8d\xffg<\x18\xf9\xc5I]\xd1\x14\xb8\xe3\xe9\x08T\rr\xe8\xccB j\xb3b\x1c\x92\xe1L\xed\xf4\xc4'
        self.assertEqual(genesis.getHash(), expectedHash, 'incorrect hash')
        self.assertEqual(genesis.outputs[0].value, genesisValue, 'incorrect value')
        self.assertEqual(genesis.outputs[0].address.exportKey(), scroogePubK.exportKey(), 'incorrect address')

    def testTransactionMultipleInsAndOuts(self):    
        expectedHash = b'\xfa\xc7t\x1f\xf0\xa3\xf5a\xdd\x9e\x0c\x96\x97\xd0\xdb\xa8L\xd9\x0cH\xca\xee\xd4g\x19 \xac\x84\xdd2\x11\xdb'
        self.assertEqual(tx2in2out.getHash(), expectedHash, 'incorrect hash')
        self.assertEqual(tx2in2out.numInputs(), 2, 'incorrect number of inputs')
        self.assertEqual(tx2in2out.numOutputs(), 2, 'incorrect number of outputs')
        self.assertEqual(tx2in2out.getInput(0).prevTxHash, genesis.hash, 'incorrect prevTxHash for input 0')
        self.assertEqual(tx2in2out.getInput(1).index, 1, 'incorrect index for input 1')
        self.assertEqual(tx2in2out.getInput(0).signature, sig0, 'incorrect signature for input 0')
        self.assertEqual(tx2in2out.getOutput(0).value, 10.0, 'incorrect value for output 0')
        self.assertEqual(tx2in2out.getOutput(1).address, scroogePubK, 'incorrect address for output 1')
        self.assertEqual(tx2in2out.getInputs()[1], tx2in2out.getInput(1), 'getInputs failure')
        self.assertEqual(tx2in2out.getOutputs()[0], tx2in2out.getOutput(0), 'getOutputs failure')
        self.assertIsNone(tx2in2out.getInput(tx2in2out.numInputs()), 'getInput failed to recognize out of bounds')
        self.assertIsNone(tx2in2out.getOutput(tx2in2out.numOutputs()), 'getOutput failed to recognize out of bounds')
        self.assertTrue(CryptoUtil.verifySignature(scroogePubK, tx2in2out.getRawDataToSign(0), tx2in2out.getInput(0).signature), \
                        'signature on input 0 does not verify')

    def testCopy(self):
        tx2 = tx2in2out.copy()
        self.assertEqual(tx2in2out.getHash(), tx2.getHash(), 'hashes should be equal')
        self.assertEqual(tx2in2out.getInputs(), tx2.getInputs(), 'inputs should be equal')
        self.assertEqual(tx2in2out.getOutputs(), tx2.getOutputs(), 'outputs should be equal')
        self.assertNotEqual(tx2in2out, tx2, 'objects should be different')
        
         
class UTXOPoolTest(unittest.TestCase):

    def testConstructor(self):
        pool = UTXOPool()
        self.assertEqual(len(pool.getAllUTXO()), 0, 'did not form empty pool correctly')
        
    def testCopy(self):
        pool = UTXOPool()
        pool2 = pool.copy()
        utxo = UTXO(txValid.getHash(), 0)
        pool2.addUTXO(utxo, txValid.getOutput(0))
        self.assertEqual(len(pool.getAllUTXO()), 0, 'pool modified')
        self.assertEqual(len(pool2.getAllUTXO()), 1, 'pool2 not modified')

    def testAddUTXO(self):
        pool = UTXOPool()
        utxo = UTXO(txValid.getHash(), 0)
        pool.addUTXO(utxo, txValid.getOutput(0))
        self.assertEqual(len(pool.getAllUTXO()), 1, 'utxo not added')
        self.assertEqual(pool.getTxOutput(utxo), txValid.getOutput(0), 'utxo not added correctly')

    def testContains(self):
        pool = UTXOPool()
        utxo = UTXO(txValid.getHash(), 0)
        pool.addUTXO(utxo, txValid.getOutput(0))
        self.assertTrue(pool.contains(utxo), 'should contain utxo')
        
    def testRemoveUTXO(self):
        pool = UTXOPool()
        utxo = UTXO(txValid.getHash(), 0)
        pool.addUTXO(utxo, txValid.getOutput(0))
        pool.removeUTXO(utxo)
        self.assertEqual(len(pool.getAllUTXO()), 0, 'did not remove correctly')

        
class TxHandlerTest(unittest.TestCase):

    def testIsValidWithValidTx(self):
        handler = TxHandler(initialPool)
        self.assertTrue(handler.isValidTx(txValid), 'valid tx was called invalid')
        
    def testIsValidWithBadInput(self):
        handler = TxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txBadInput), 'bad input not detected')

    def testIsValidWithBadSignature(self):
        handler = TxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txBadSig), 'bad signature not detected')
        
    def testIsValidWithDoubleInput(self):
        handler = TxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txDoubleInput), 'double input not detected')
        
    def testIsValidWithNegativeOutput(self):
        handler = TxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txNegOut), 'negative output not detected')
        
    def testIsValidWithOutGreaterThanIn(self):
        handler = TxHandler(initialPool)
        self.assertFalse(handler.isValidTx(txTooMuch), 'outputs > inputs not detected')
        
    def testHandleTxsWithNoTx(self):
        handler = TxHandler(initialPool)
        self.assertEqual(handler.handleTxs([]), [], 'should return empty list')
        
    def testHandleTxsWithOneTx(self):
        handler = TxHandler(initialPool)
        accepted = handler.handleTxs([txValid])
        self.assertEqual(len(accepted), 1, 'should return list with one transaction')
        
    def testHandleTxsAllInvalid(self):
        handler = TxHandler(initialPool)
        accepted = handler.handleTxs([genesis, txBadInput, txNegOut])
        self.assertEqual(len(accepted), 0, 'should return empty list')
        
    def testHandleTxsWithUtxoInPool(self):
        pool = initialPool.copy()
        utxo = UTXO(txA.getHash(), 0)
        pool.addUTXO(utxo, txA.getOutput(0))
        handler = TxHandler(pool)
        accepted = handler.handleTxs([txB])
        self.assertEqual(len(accepted), 1, 'should return list with one transaction')
        
    def testHandleTxsCheckPool(self):
        pool = initialPool.copy()
        utxo = UTXO(txA.getHash(), 0)
        pool.addUTXO(utxo, txA.getOutput(0))
        poolsize = len(pool.getAllUTXO())
        handler = TxHandler(pool)
        handler.handleTxs([txB])
        self.assertEqual(len(pool.getAllUTXO()), poolsize, 'pool should not be altered')
        self.assertTrue(utxo in pool.getAllUTXO(), 'pool should not be altered')
        
    def testHandleTxsDoubleSpending(self):
        handler = TxHandler(initialPool)
        accepted = handler.handleTxs([txA, txB, txC, txD])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1 or acceptedHashes == ans2, 'wrong set')
        
    def testHandleTxsDoubleSpendingVaryOrder(self):
        handler = TxHandler(initialPool)
        accepted = handler.handleTxs([txA, txC, txB, txD])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1 or acceptedHashes == ans2, 'wrong set')
        
    def testHandleTxsNeedMultiplePasses(self):
        handler = TxHandler(initialPool)
        accepted = handler.handleTxs([txC, txB, txD, txA])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1 or acceptedHashes == ans2, 'wrong set')
        
    def testHandleTxsMixValidInvalid(self):
        handler = TxHandler(initialPool)
        accepted = handler.handleTxs([txC, genesis, txB, txNegOut,
                                      txD, txBadSig, txA, txD])
        acceptedHashes = sorted([tx.getHash() for tx in accepted])
        self.assertTrue(acceptedHashes == ans1 or acceptedHashes == ans2, 'wrong set')
    
    def testGetUtxoPool(self):
        handler = TxHandler(initialPool)
        handler.handleTxs([txValid])
        utxos = handler.getUTXOPool().getAllUTXO()
        self.assertEqual(len(utxos), 1, 'pool should have one UTXO')
        self.assertTrue(UTXO(txValid.getHash(), 0) in utxos, 'should have the UTXO from the added tx')
        
    
if __name__ == "__main__":
    unittest.main()
