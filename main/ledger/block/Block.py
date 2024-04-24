import copy
import json
from abc import ABC
from textwrap import indent

from main.dsl.Action import Action
from main.dsl.Verification import Verification
from main.ledger.Ledger import Ledger
from main.ledger.block.Header import Header
from main.utils.fake_crypto import new_deterministic_hash, sha, Signature, sign, PrivateKey, PublicKey


class Block(ABC):

    @property
    def hash(self):
        return sha(self._header)

    @property
    def is_signed(self):
        return self._signature is not None
    
    @property
    def previous_block(self) -> 'Block' or None:
        if self._header.previous_hash is None:
            return None

        previous_hash = self._header.previous_hash
        return Ledger().get_block(previous_hash)

    @property
    def account_public_key(self) -> str:
        block = self
        while block._header.previous_hash is not None:
            # While the block is not the genesis block.
            block = block.previous_block

        return block.data['account']

    def __init__(self, previous_block: 'Block'):
        if previous_block is None:
            previous_hash: str = new_deterministic_hash()
        elif isinstance(previous_block, Block):
            previous_hash: str = previous_block.hash
        else:
            raise Exception("previous_block must be Block or None. ")

        self._header = Header(previous_hash=previous_hash)
        self._signature: Signature or None = None
        if not hasattr(self, 'data_initial'):
            self.data = dict()
        else:
            self.data = copy.deepcopy(self.data_initial)  # From metaclass.
        self.add_data('block_type', type(self).__name__)

    def __str__(self):
        result = ''
        result += f'previous hash: {self._header.previous_hash}\n'
        result += f'hash:          {self.hash}\n'
        result += f'timestamp:     {self._header.timestamp}\n'
        result += f'signed by:     {self._signature.signer if self.is_signed else "not yet signed"}\n'

        data = copy.deepcopy(self.data)
        data.pop('on_sign_verifications', None)
        data.pop('on_sign_actions', None)
        data.pop('parameters', None)
        result += f'data:\n' + indent(json.dumps(data, indent=4), '\t') + '\n'

        return result

    def add_data(self, new_key: str, new_value: any) -> 'Block':
        if self._signature is not None:
            raise Exception("Can't add data to a signed block. ")

        self.data[new_key] = new_value
        return self

    def sign(self, private_key: PrivateKey) -> None:
        if self._signature is not None:
            raise Exception("Block already signed. ")

        self._on_sign_actions()

        if not self._can_interact_with_open():
            raise Exception("Block can't interact with his open block. ")

        if not self._on_sign_verifications():
            raise Exception("Block verification failed. ")

        self._header.hash_root = sha(self.data)
        self._signature = sign(self.hash, private_key)

    def _can_interact_with_open(self) -> bool:
        """
        Check if the current block his in the interact_with section of his correspondant open block.

        :return: True if the block can interact with his open block, False otherwise.
        """
        if self._is_genesis_block() or self._is_open_block():
            return True

        open_block = Ledger().get_block(self.data['open_hash'])
        return type(self).__name__ in open_block.data['interact_with']

    def _on_sign_verifications(self) -> bool:
        """
        Verify if all the on_sign_verifications are valid. If there is no on_sign_verifications, return True.

        :return: True if all the on_sign_verifications are valid, False otherwise.
        """

        if 'on_sign_verifications' not in self.data.keys():
            return True

        return all(
            self._on_sign_verification(on_sign_object['method_name'], on_sign_object['args'])
            for on_sign_object in self.data['on_sign_verifications']
        )

    def _on_sign_verification(self, method_name: str, args: [str]) -> bool:
        """
        Verify with the corresponding method in the Verification class if the block is valid.
        :param method_name: name of the method in the Verification class.
        :param args: arguments of the method.
        :return: True if the block is valid, False otherwise.
        """

        computed_args = self._compute_args(args)
        return Verification()[method_name](*computed_args)

    def _on_sign_actions(self) -> None:
        """
        Execute all the on_sign_actions.
        :return: None
        """

        if 'on_sign_actions' not in self.data.keys():
            return

        for on_sign_object in self.data['on_sign_actions']:
            self._on_sign_action(on_sign_object['method_name'], on_sign_object['args'])

    def _on_sign_action(self, method_name: str, args: [str]) -> None:
        """
        Execute the corresponding method in the Action class.

        :param method_name: name of the method in the Action class.
        :param args: arguments of the method.
        :return: None
        """

        computed_args = self._compute_args(args)
        Action()[method_name](*computed_args)

    def _compute_args(self, args: [str]):
        """
        Compute the arguments of the on_sign_actions and on_sign_verifications.
        For the args, the checking order is the next one :
            - if the arg is in the data, take the value from the data.
            - if the arg is a variable in the block, take the value from the block.
            - if f'self.{arg}' is a variable in the block, take the value from the block.
            - Otherwise, None.

        :param args:
        :return:
        """
        computed_args = []
        for arg in args:
            if arg in self.data.keys():
                computed_args.append(self.data[arg])
                continue
            try:
                computed_args.append(eval(f'{arg}'))
            except (AttributeError, NameError):
                try:
                    computed_args.append(eval(f'self.{arg}'))
                except (AttributeError, NameError):
                    computed_args.append(None)
        return computed_args

    def verify(self, public_key: PublicKey) -> bool:
        return (self.is_signed and
                self.verify_signature(public_key) and
                self._header.hash_root == sha(self.data))

    def verify_signature(self, public_key: PublicKey) -> bool:
        if self._signature is None:
            return False

        return self._signature.verify(self.hash, public_key)

    def is_previous_of(self, next_block: 'Block') -> bool:
        return self.hash == next_block._header.previous_hash

    def _is_genesis_block(self) -> bool:
        return self._header.previous_hash is None

    def _is_open_block(self) -> bool:
        return 'interact_with' in self.data.keys()
