from brownie import accounts, BasicDataStorage


def test_deploy():
    # Tests the deployment of the contract and the initialization of favoriteNumber variable to 0

    # setup
    account = accounts[0]
    expectedValue = 0

    # actions
    basicStorageContract = BasicDataStorage.deploy({"from": account})
    initialValue = basicStorageContract.retrieve()

    # testing
    assert initialValue == expectedValue


def test_update():
    # Tests the deployment of the contract and the update function

    # setup
    account = accounts[0]
    basicStorageContract = BasicDataStorage.deploy({"from": account})
    expectedValue = 33

    # actions
    basicStorageContract.update(expectedValue, {"from": account})

    # testing
    assert expectedValue == basicStorageContract.retrieve()
