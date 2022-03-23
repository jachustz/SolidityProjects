from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_min_fee():
    account = accounts[0]
    lotteryContract = Lottery.deploy(
        config["networks"][network.show_active()]["ethusdPriceFeed"], {"from": account}
    )

    print(f"Entrace Fee {lotteryContract.getMinEntry()}")
    assert lotteryContract.getMinEntry() > Web3.toWei(0.017, "ether")
    assert lotteryContract.getMinEntry() < Web3.toWei(0.02, "ether")
