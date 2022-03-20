from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

_ethPrice = 3000
_ethPrecision = 18


def getAccount():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["devPrivateKey"])


def deployMocks():
    print(f"Active Network is {network.show_active()}")
    print(f"Deploying Mocks")

    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            _ethPrecision, Web3.toWei(_ethPrice, "ether"), {"from": getAccount()}
        )
    priceFeedAddress = MockV3Aggregator[-1].address
    print(f"Mocks Deployed Successfully")
