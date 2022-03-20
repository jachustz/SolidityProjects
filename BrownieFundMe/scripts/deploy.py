from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helperFunctions import getAccount, deployMocks


def deployFundMe():
    account = getAccount()

    if network.show_active() != "development":
        priceFeedAddress = config["networks"][network.show_active()]["ethusdPriceFeed"]
    else:
        deployMocks()

    fundMe = FundMe.deploy(
        priceFeedAddress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fundMe.address}")


def main():
    deployFundMe()
