import os
from web3 import Web3
from rich.console import Console

console = Console()

class MonadAutomator:
    def __init__(self, rpc_url, private_key):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.private_key = private_key
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address

    def check_balance(self):
        try:
            balance_wei = self.w3.eth.get_balance(self.address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return balance_eth
        except Exception as e:
            console.print(f"[red]Error checking balance: {e}[/red]")
            return 0

    def send_keep_alive(self):
        """Sends a 0.00001 MON transaction to self."""
        try:
            nonce = self.w3.eth.get_transaction_count(self.address)
            gas_price = self.w3.eth.gas_price

            tx = {
                'nonce': nonce,
                'to': self.address,
                'value': self.w3.to_wei(0.00001, 'ether'),
                'gas': 21000,
                'gasPrice': gas_price,
                'chainId': 10143 # Update if different on actual testnet
            }
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            # Try accessing rawTransaction by name, fallback to index for compatibility
            raw_tx = getattr(signed_tx, 'rawTransaction', None)
            if raw_tx is None and hasattr(signed_tx, '__getitem__'):
                 raw_tx = signed_tx[0]
            
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            console.print(f"[red]Transaction failed: {e}[/red]")
            return None

    def deploy_storage_contract(self):
        """Deploys a simple storage contract to qualify for developer activity."""
        # Simple Bytecode for a Storage Contract (pre-compiled for simplicity)
        # Verify source: contract SimpleStorage { uint public x; function set(uint _x) public { x = _x; } }
        bytecode = "608060405234801561001057600080fd5b5060df8061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c806360fe47b1146037578063c2985578146062575b600080fd5b606060048036036020811015604b57600080fd5b8101908080359060200190929190505050607e565b005b60666088565b6040518082815260200191505060405180910390f35b80600081905550565b6000548156fea26469706673582212204c35c82662c1995ec0319ef586dbba805177265287e0766324d67353f88950d264736f6c63430008070033"
        abi = [{"inputs":[],"name":"x","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_x","type":"uint256"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"}]

        try:
            Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
            nonce = self.w3.eth.get_transaction_count(self.address)
            gas_price = self.w3.eth.gas_price

            # Build construction transaction
            tx = Contract.constructor().build_transaction({
                'nonce': nonce,
                'gas': 200000, 
                'gasPrice': gas_price,
                'chainId': 10143
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            # Try accessing rawTransaction by name, fallback to index for compatibility
            raw_tx = getattr(signed_tx, 'rawTransaction', None)
            if raw_tx is None and hasattr(signed_tx, '__getitem__'):
                 raw_tx = signed_tx[0]
            
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            console.print(f"[red]Deployment failed: {e}[/red]")
            return None
