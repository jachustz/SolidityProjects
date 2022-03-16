from brownie import accounts


def deployBasicDataStorage():
    account = accounts.load("braveKey")
    print(account)


def main():
    print("hello")
    deployBasicDataStorage()
