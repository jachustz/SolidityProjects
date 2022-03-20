from brownie import FundMe, network, accounts, exceptions
from scripts.helperFunctions import getAccount, _localBlockChainEnvironments
from scripts.deploy import deployFundMe
import pytest


def test_FundAndWithdraw():
    account = getAccount()
    fundMeContract = deployFundMe()
    entranceFee = fundMeContract.getEntranceFee() + 1000
    txn = fundMeContract.fund({"from": account, "value": entranceFee})
    txn.wait(1)
    assert fundMeContract.addressToAmountFunded(account.address) == entranceFee
    txn2 = fundMeContract.fund({"from": account, "value": entranceFee})
    txn2.wait(1)
    assert fundMeContract.addressToAmountFunded(account.address) == entranceFee * 2
    txn3 = fundMeContract.withdraw({"from": account})
    txn3.wait(1)
    assert fundMeContract.addressToAmountFunded(account.address) == 0


def test_isClaimant_withdraw():
    if network.show_active() not in _localBlockChainEnvironments:
        pytest.skip("only for local testing")
    account = getAccount()
    nonClaimant = accounts[1]
    fundMeContract = deployFundMe()
    with pytest.raises(exceptions.VirtualMachineError):
        fundMeContract.withdraw({"from": nonClaimant})
