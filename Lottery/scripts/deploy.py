from inspect import getcomments
from scripts.helperFunctions import fund_with_link
from scripts.helperFunctions import getAccount, getContract
from brownie import Lottery, network, config
import time


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
    print("Lottery Contract Successfully Deployed")
    return lotteryContract


def startLottery():
    account = getAccount()
    lotteryContract = Lottery[-1]
    txn = lotteryContract.startLottery({"from": account})
    txn.wait(1)
    print("lottery is started")


def enterLottery():
    account = getAccount()
    lotteryContract = Lottery[-1]
    value = lotteryContract.getMinEntry() + 1000000000
    txn = lotteryContract.enterLottery({"from": account, "value": value})
    txn.wait(1)
    print("lottery was entered")


def runLottery():

    account = getAccount()
    lotteryContract = Lottery[-1]
    print(f"winner is {lotteryContract._recentWinner()}")
    txn = fund_with_link(lotteryContract.address)
    endingTransaction = lotteryContract.endLottery({"from": account})
    endingTransaction.wait(1)
    print("lottery Ran")
    time.sleep(60)
    print(f"winner is {lotteryContract._recentWinner()}")


def main():
    deployLottery()
    startLottery()
    enterLottery()
    runLottery()
