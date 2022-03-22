// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    address payable[] public _players;
    uint256 public _USDEntryFee;
    AggregatorV3Interface internal _priceFeed;
    enum LotteryState {
        Open,
        Closed,
        InProcess
    }
    LotteryState public _lotteryState;

    constructor(address priceFeedAddress) public {
        _USDEntryFee = 50 * 10**18;
        _priceFeed = AggregatorV3Interface(priceFeedAddress);
        _lotteryState = LotteryState.Closed;
    }

    function enterLottery() public payable {
        require(_lotteryState == LotteryState.Open);
        require(msg.value >= getMinEntry(), "Entry fee has not been met");
        _players.push(msg.sender);
    }

    function getMinEntry() public view returns (uint256) {
        (, int256 price, , , ) = _priceFeed.latestRoundData();

        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (_USDEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            _lotteryState == LotteryState.Closed,
            "Can't start a new lottery until current one is closed"
        );
        _lotteryState = LotteryState.Open;
    }

    function endLottery() public onlyOwner {
        require(
            _lotteryState == LotteryState.Open,
            "Can't close a lottery until one is started"
        );
    }

    function generateRandom() public returns (uint256) {}
}
