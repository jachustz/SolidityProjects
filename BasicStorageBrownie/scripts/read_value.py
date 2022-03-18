from brownie import accounts, config, BasicDataStorage, network


def readContract():
    basicStorage = BasicDataStorage[-1]
    print(basicStorage.retrieve())


def main():
    readContract()
