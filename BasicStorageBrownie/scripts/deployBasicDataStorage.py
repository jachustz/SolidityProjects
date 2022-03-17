from brownie import accounts, config, BasicDataStorage


def deployBasicDataStorage():
    account = accounts[0]

    # deply
    basicStorage = BasicDataStorage.deploy({"from": account})

    # call retrieve to make sure it inits to 0
    favoriteNumber = basicStorage.retrieve()
    print(favoriteNumber)

    # create txn to update to 99
    transaction = basicStorage.store(99, {"from": account})
    transaction.wait(1)  # wait 1 block

    # call retrieve to ensure it was check if it was updated correctly
    favoriteNumber = basicStorage.retrieve()
    print(favoriteNumber)


def main():
    deployBasicDataStorage()
