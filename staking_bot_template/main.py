import os

from dotenv import load_dotenv
from web3 import Web3

from staking_bot_template.contracts import AloePredictions

load_dotenv()

address = '0x0C9C402ee16aF7B389De11dA963E9A26a67e6e4B'
provider = Web3(Web3.WebsocketProvider(
    'wss://eth-kovan.ws.alchemyapi.io/v2/' + os.environ['PROVIDER_ALCHEMY_KEY']))

contract = AloePredictions(address, provider)

proposal = contract.get_proposal(2)
proposal.reset()

x = proposal.submit_to(contract)(147, 15000000000, os.environ['ACCOUNT_PRIVATE_KEY'])
print(x)
