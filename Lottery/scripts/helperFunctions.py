from brownie import (
    accounts,
    config,
    network,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
)
from web3 import Web3

_localBlockChainEnvironments = ["development", "ganace-local"]
_forkedLocalEnvironments = ["mainnet-fork", "mainnet-fork-dev"]
_ethPrice = 200000000000
_ethPrecision = 8


def getAccount():
    if (
        network.show_active() in _localBlockChainEnvironments
        or network.show_active() in _forkedLocalEnvironments
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["devPrivateKey"])


contractToMock = {
    "ethUSDPriceFeed": MockV3Aggregator,
    "vrfCoordinator": VRFCoordinatorMock,
    "linkToken": LinkToken,
}


def getContract(contractName):
    """Will get info from brownie conifg, otherwise it will
    return mocks
    """
    contractType = contractToMock[contractName]
    if network.show_active() in _localBlockChainEnvironments:
        if len(contractType) <= 0:
            deployMocks()
        contract = contractType[-1]
    else:
        contractAddress = config["networks"][network.show_active()][contractName]
        contract = Contract.from_abi(
            contractType._name, contractAddress, contractType.abi
        )
    return contract


def deployMocks():
    account = getAccount()
    print(f"Active Network is {network.show_active()}")
    print(f"Deploying Mocks")

    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(_ethPrecision, _ethPrice, {"from": account})
        linkTokenContract = LinkToken.deploy({"from": account})
        VRFCoordinatorMock.deploy(linkTokenContract.address, {"from": account})

    print(f"Mocks Deployed Successfully")
