import unittest
from ..context import cryptraider

from Crypto.Cipher import AES
import base64

class TestAesBasedOracle(unittest.TestCase):
    def test_basic_oracle_attack(self):
        
        block_length = 16

        def pad( data ):
            return data + '\x00' * ( block_length - ( len( data ) % block_length ) )

        secret = 'Aero{5013a76ed3b98bae1e79169b3495f47a}'

        def oracle( prefix ):
            key = '__s3cr3t_k3y__'
            msg = prefix + secret
            aes = AES.new( pad(key).encode(), AES.MODE_ECB )
            return base64.b64encode( aes.encrypt( pad(msg).encode() ) )
            
        attack = cryptraider.cipher.EcbChosenPrefixAttack(oracle, 16, "Aero{01235467890abcdef}")
        self.assertEqual(secret, attack.execute())

if __name__ == '__main__':
    unittest.main()