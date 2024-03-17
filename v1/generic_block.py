#!/usr/bin/env python


import datetime
import random


from fake_crypto import sign, verify, sha, new_deterministic_hash, new_random_hash




class GenericBlock():
	"""
	Generic block object
	"""

	def __init__(self, data ,previous_block=None):
		"""
		initialized Block object with previous_hash and timestamp
		data must be added with add_data(...), then signed
		"""

		if previous_block is None:
			self._previous_hash = new_deterministic_hash()
		elif isinstance(previous_block, GenericBlock):
			self._previous_hash = previous_block.hash()
		else:
			raise Exception("previous_block must be GenericBlock or None")

		self._timestamp = datetime.datetime.now()
		self._data = data
		self._data["type"] = "Generic Block"
		self._hash_root = sha(self._data)
		self._signature = self.sign(self)


	def __str__(self):
		"""
		simple string representation of Block metadata
		"""

		rop = ""
		rop += f"hash:          {self.hash()}\n"		
		rop += f"previous hash: {self._previous_hash}\n"
		rop += f"timestamp:     {self._timestamp}\n"
		if self._signature is None:
			rop += f"not yet signed\n"
		else:
			rop += f"signed by:     {self._signature._signer}\n"
		return rop
	

	def __repr__(self):
		"""
		Block representation
		"""

		return f"<{type(self).__name__} [{self.hash()}]>"


	def header(self):
		"""
		return header as tuble
		"""

		return (self._previous_hash, self._timestamp, self._hash_root)

	def get_data(self, key=None):
		"""
		if key is specified, return data[key] else return the entire dict
		"""

		if key is None:
			return self._data
		else:
			return self._data[key]


	def hash(self):
		"""
		return hash of block header
		"""
		return sha(self.header())


	def sign(self, private_key):
		"""
		sign the Block header with a private key
		"""

		message = self.hash()
		self._signature = sign(message, private_key)


	def verify_signature(self, public_key):
		"""
		verify the signature and return a bool
		"""

		if self._signature is None:
			#print(f"Error: Block must be sign before verification.")
			return False
		else:
			message = sha(self.header())
			return verify(message, self._signature, public_key)


	def verify_data(self):
		"""
		check the validity of the hash_root and return a bool
		"""

		return self._hash_root == sha(self._data)




# Proposition d'utilser le builder pattern pour creer un block et ajouter du data a lamem occassion 