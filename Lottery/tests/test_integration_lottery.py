from brownie import network
import pytest
from scripts.helperFunctions import (
    _localBlockChainEnvironments,
    getAccount,
    fund_with_link,
)
from scripts.deploy import deployLottery
import time


def test_can_pick_winner():
    if network.show_active() in _localBlockChainEnvironments:
        pytest.skip()
    lotteryContract = deployLottery()
    account = getAccount()
    lotteryContract.startLottery({"from": account})
    lotteryContract.enterLottery(
        {"from": account, "value": lotteryContract.getMinEntry()}
    )
    lotteryContract.enterLottery(
        {"from": account, "value": lotteryContract.getMinEntry()}
    )
    fund_with_link(lotteryContract)
    lotteryContract.endLottery({"from": account})
    time.sleep(60)
    assert lotteryContract._recentWinner() == account
    assert lotteryContract.balance() == 0
