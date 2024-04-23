# import unittest

# from main.ledger.account.Account import Account
# from main.utils.fake_crypto import generate_keys


# class TestAccount(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         (cls.genesisPrivateKey, cls.genesisPublicKey) = generate_keys('Genesis')

#     def setUp(self):
#         self.account = Account(self.genesisPrivateKey, self.genesisPublicKey)

#     def tearDown(self):
#         self.account = None

#     @classmethod
#     def tearDownClass(cls):
#         cls.genesisPrivateKey = None
#         cls.genesisPublicKey = None

#     def test_publicKey(self):
#         self.assertEqual(self.account.public_key, self.genesisPublicKey)
