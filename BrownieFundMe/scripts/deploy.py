from brownie import FundMe
from scripts.helperFunctions import getAccount


def deployFundMe():
    account = getAccount()
    fundMe = FundMe.deploy({"from": account}, publish_source=True)
    print(f"Contract deployed to {fundMe.address}")


def main():
    deployFundMe()
