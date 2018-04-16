def UTXO(txHash, index):
    '''
    Construct an immutable form of the UTXO that can be used as a dictionary key
    '''
    
    return (txHash, index)
