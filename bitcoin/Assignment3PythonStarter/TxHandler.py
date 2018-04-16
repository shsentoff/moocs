'''
Replace this file with your implementation from Assignment 1
'''

from UTXO import UTXO
import CryptoUtil
from Transaction import Transaction


class TxHandler(object):
    '''
    Collect transactions into a mutually valid set that can be used
    to mine a new block.
    '''

    def __init__(self, pool):
        '''
        Create the new handler.
        This should make a copy of the UTXOPool passed as a parameter.
        '''
        # TODO - implement this
        pass



    def getUTXOPool(self):
        '''
        Return the current value of this TxHandler's UTXOPool as modified
        by calls to handleTxs.
        '''
        # TODO - implement this
        pass



        
    def isValidTx(self, tx):
        '''
        Return True if:
        (1) all outputs claimed by tx are in the current UTXO pool, 
        (2) the signatures on each input of tx are valid, 
        (3) no UTXO is claimed multiple times by tx,
        (4) all of txs output values are non-negative, and
        (5) the sum of txs input values is greater than or equal to
            the sum of its output values;
        and False otherwise.
        '''
        # TODO - implement this
        pass
    



    
    def handleTxs(self, possibleTxs):
        '''
        Return a maximal subset of mutually valid transactions from possibleTxs.
        "Maximal" means that no other transaction can be added to the list and
        still have all the transactions mutually valid. Note that there may be
        more than one correct subset because of the possibility of transactions
        trying to double spend some output.
        possibleTxs must be a list of Transaction objects.
        '''
        # TODO - implement this
        pass
    




