from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

_ethPrice = 200000000000
_ethPrecision = 8
_localBlockChainEnvironments = ["development", "ganace-local"]
_forkedLocalEnvironments = ["mainnet-fork", "mainnet-fork-dev"]


def getAccount():
    if (
        network.show_active() in _localBlockChainEnvironments
        or network.show_active() in _forkedLocalEnvironments
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["devPrivateKey"])


def deployMocks():
    print(f"Active Network is {network.show_active()}")
    print(f"Deploying Mocks")

    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(_ethPrecision, _ethPrice, {"from": getAccount()})

    print(f"Mocks Deployed Successfully")
