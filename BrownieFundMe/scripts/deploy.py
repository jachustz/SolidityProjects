from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helperFunctions import (
    getAccount,
    deployMocks,
    _localBlockChainEnvironments,
)


def deployFundMe():
    account = getAccount()

    if network.show_active() not in _localBlockChainEnvironments:
        priceFeedAddress = config["networks"][network.show_active()]["ethusdPriceFeed"]
    else:
        deployMocks()
        priceFeedAddress = MockV3Aggregator[-1].address

    fundMe = FundMe.deploy(
        priceFeedAddress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fundMe.address}")
    return fundMe


def main():
    deployFundMe()
