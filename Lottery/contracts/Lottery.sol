// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public _players;
    uint256 public _USDEntryFee;
    uint256 public _fee;
    bytes32 public _keyHash;
    address payable public _recentWinner;
    uint256 public _randomness;

    AggregatorV3Interface internal _priceFeed;
    enum LotteryState {
        Open,
        Closed,
        InProcess
    }
    LotteryState public _lotteryState;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address priceFeedAddress,
        address vrfCoordinator,
        address linkToken,
        uint256 fee,
        bytes32 keyHash
    ) public VRFConsumerBase(vrfCoordinator, linkToken) {
        _USDEntryFee = 50 * 10**18;
        _priceFeed = AggregatorV3Interface(priceFeedAddress);
        _lotteryState = LotteryState.Closed;
        _fee = fee;
        _keyHash = keyHash;
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
        _lotteryState = LotteryState.InProcess;
        bytes32 requestId = requestRandomness(_keyHash, _fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 requestID, uint256 randomness)
        internal
        override
    {
        require(
            _lotteryState == LotteryState.InProcess,
            "Lottery not ready for processing"
        );

        require(randomness > 0, "Random not found");

        uint256 winnerIndex = randomness % _players.length;
        _recentWinner = _players[winnerIndex];
        _recentWinner.transfer(address(this).balance);
        //Restart the lottery
        _players = new address payable[](0);
        _lotteryState == LotteryState.Closed;
        _randomness = randomness;
    }
}
