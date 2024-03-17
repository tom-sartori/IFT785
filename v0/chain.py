#!/usr/bin/env python


import datetime
import random


from generic_block import GenericBlock




class Chain():
	"""
	Chain object to store block
	"""

	def __init__(self, genesis_block):
		"""
		initialized Chain object with genesis_block
		"""
		if not isinstance(genesis_block, GenericBlock):
			raise Exception("Chain must be initialized with a genesis Block")

		self._block_list = [genesis_block]


	def __repr__(self):
		"""
		Chain representation
		"""
		return f"<{type(self).__name__}>"


	def verify(self, public_key):
		"""
		verify Chain integrity for 0 to n-1 blocks
		and return a bool
		"""
		for i in range(len(self._block_list) - 1):
			block = self._block_list[i]
			if not block.verify_data():
				#raise Exception(f"Data verification failed for {i}th block : H={block.hash()}")
				print(f"Error: Data verification failed for {i}th block [{block.hash()}]")
				return False
			if not block.verify_signature(public_key):
				#raise Exception(f"Signature verification failed for {i}th block : H={block.hash()}")
				print(f"Error: Signature verification failed for {i}th block [{block.hash()}]")
				return False
			if block.hash() != self._block_list[i+1]._previous_hash:
				#raise Exception(f"Chain verification failed between {i}th and {i+1}th blocks")
				print(f"Error: Chain verification failed between {i}th and {i+1}th blocks")
				return False

		block = self._block_list[-1]
		if not block.verify_data():
			print(f"Warning: Data verification failed for last block [{block.hash()}]")
			return False
		if not block.verify_signature(public_key):
			print(f"Warning: Signature verification failed for last block [{block.hash()}]")
			return False

		return True


	def add_block(self, new_block):
		"""
		add new block to the chain
		"""

		pass

