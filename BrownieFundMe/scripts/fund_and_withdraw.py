from brownie import FundMe, network
from scripts.helperFunctions import getAccount


def fund():
    fundMeContract = FundMe[-1]
    account = getAccount()
    entranceFee = fundMeContract.getEntranceFee()
    print(f"Entrace fee is {entranceFee}")
    print("Funding")
    fundMeContract.fund({"from": account, "value": entranceFee})
    print("Funding Completed")


def withdraw():
    fundMeContract = FundMe[-1]
    print("withdrawing")
    account = getAccount()
    fundMeContract.withdraw({"from": account})
    print("withdraw completed")


def main():
    print("run main")
    fund()
    withdraw()
