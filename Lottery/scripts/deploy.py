from inspect import getcomments
from scripts.helperFunctions import getAccount, getContract
from brownie import Lottery, network, config


def deployLottery():
    account = getAccount()
    lotteryContract = Lottery.deploy(
        getContract("ethUSDPriceFeed").address,
        getContract("vrfCoordinator").address,
        getContract("linkToken"),
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyHash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Somehow this worked")


def main():
    deployLottery()
