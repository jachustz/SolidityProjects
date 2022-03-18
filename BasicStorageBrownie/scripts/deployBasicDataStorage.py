from brownie import accounts, config, BasicDataStorage, network


def deployBasicDataStorage():
    account = get_account()

    # deply
    basicStorage = BasicDataStorage.deploy({"from": account}, publish_source=True)

    # call retrieve to make sure it inits to 0
    favoriteNumber = basicStorage.retrieve()
    print(favoriteNumber)

    # create txn to update to 99
    transaction = basicStorage.update(99, {"from": account})
    transaction.wait(1)  # wait 1 block

    # call retrieve to ensure it was check if it was updated correctly
    favoriteNumber = basicStorage.retrieve()
    print(favoriteNumber)
    print(config["wallets"]["devPrivateKey"])


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["devPrivateKey"])


def main():
    deployBasicDataStorage()
