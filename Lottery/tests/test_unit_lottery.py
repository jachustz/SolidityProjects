from brownie import Lottery, accounts, config, network, exceptions
from scripts.helperFunctions import getContract
from scripts.helperFunctions import getAccount, fund_with_link
from scripts.deploy import deployLottery
from scripts.helperFunctions import _localBlockChainEnvironments
from web3 import Web3
import pytest


def test_get_min_fee():
    if network.show_active() not in _localBlockChainEnvironments:
        print("skipping b/c not local")
        pytest.skip()
    lotteryContract = deployLottery()
    entranceFee = lotteryContract.getMinEntry()
    exceptedFee = Web3.toWei(0.025, "ether")
    assert exceptedFee == entranceFee


def test_entry_block_unless_started():
    if network.show_active() not in _localBlockChainEnvironments:
        print("skipping b/c not local")
        pytest.skip()
    lotteryContract = deployLottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lotteryContract.enterLottery(
            {"from": getAccount(), "value": lotteryContract.getMinEntry()}
        )


def test_can_start_and_enter():
    if network.show_active() not in _localBlockChainEnvironments:
        print("skipping b/c not local")
        pytest.skip()
    lotteryContract = deployLottery()
    lotteryContract.startLottery({"from": getAccount()})
    lotteryContract.enterLottery(
        {"from": getAccount(), "value": lotteryContract.getMinEntry()}
    )
    print(f"{lotteryContract._players(0)}")
    assert lotteryContract._players(0) == getAccount()


def test_can_end_lottery():
    if network.show_active() not in _localBlockChainEnvironments:
        print("skipping b/c not local")
        pytest.skip()
    lotteryContract = deployLottery()
    lotteryContract.startLottery({"from": getAccount()})
    lotteryContract.enterLottery(
        {"from": getAccount(), "value": lotteryContract.getMinEntry()}
    )
    fund_with_link(lotteryContract)
    lotteryContract.endLottery({"from": getAccount()})
    assert lotteryContract._lotteryState() == 2


def test_choose_winner():
    if network.show_active() not in _localBlockChainEnvironments:
        print("skipping b/c not local")
        pytest.skip()
    print("yyyyyyyyyooooooooooooo")
    startingBalance = getAccount().balance()
    lotteryContract = deployLottery()
    lotteryContract.startLottery({"from": getAccount()})
    lotteryContract.enterLottery(
        {"from": getAccount(), "value": lotteryContract.getMinEntry()}
    )
    lotteryContract.enterLottery(
        {"from": getAccount(index=1), "value": lotteryContract.getMinEntry()}
    )
    lotteryContract.enterLottery(
        {"from": getAccount(index=2), "value": lotteryContract.getMinEntry()}
    )
    lotteryBalance = lotteryContract.balance()
    afterfundingBalance = getAccount().balance()
    print(f"lotter balance is {lotteryBalance}")
    print(f"startingBalance is {startingBalance}")
    print(f"afterfundingBalance is {afterfundingBalance}")

    fund_with_link(lotteryContract)
    txn = lotteryContract.endLottery({"from": getAccount()})
    requestId = txn.events["RequestedRandomness"]["requestId"]
    staticRNG = 777
    getContract("vrfCoordinator").callBackWithRandomness(
        requestId, staticRNG, lotteryContract.address, {"from": getAccount()}
    )

    assert lotteryContract._recentWinner() == getAccount()
    assert lotteryContract.balance() == 0
    assert getAccount().balance() == afterfundingBalance + lotteryBalance
