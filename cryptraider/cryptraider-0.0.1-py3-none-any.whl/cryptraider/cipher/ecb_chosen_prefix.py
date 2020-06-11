import random
import binascii

import logging

logger = logging.getLogger('ecb_chosen_prefix')

import string
class EcbChosenPrefixAttack:
    def __init__(self, oracle, block_length=16, charset=string.printable):
        self.block_length = block_length
        self.charset = charset
        self.oracle = oracle

    def execute(self, derived_plaintext = '') : # If you know some prefix of the plaintext, you can pass it in.
        for block_index in range(0, 5) :
            block_start = block_index * self.block_length
            block_end = (block_index + 1)*self.block_length
            for byte_index in range(16) :
                if block_start + byte_index < len(derived_plaintext) :
                    continue
                prefix_length = (self.block_length - byte_index - 1)
                known_block = ('X'*self.block_length)[-prefix_length:]
                if prefix_length == 0 :
                    known_block = ''
                logger.debug('salt=%s, len(known_block)=%d, prefix_length=%d',known_block, len(known_block), prefix_length)
                assert len(known_block) == prefix_length
                target = self.oracle(known_block)
                logger.debug('target = %s',binascii.hexlify(target))
                nextCharFound = False
                for c in self.charset :
                    x = known_block + derived_plaintext+ c
                    logger.debug('len(x)=%d, block_end=%d',len(x),block_end)
                    assert len(x) == block_end
                    result = self.oracle(x)

                    logger.debug('result[%s] = %s' % (c, binascii.hexlify(result)))
                    if result[block_start:block_end] == target[block_start:block_end] :
                        derived_plaintext = derived_plaintext + c
                        nextCharFound = True
                        logger.info('Character found! derived_plaintext = %s', derived_plaintext)
                        break
                
                if not nextCharFound :
                    return derived_plaintext