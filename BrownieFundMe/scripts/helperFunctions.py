from brownie import accounts, config, network


def getAccount():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["devPrivateKey"])
