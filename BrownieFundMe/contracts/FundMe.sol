// SPDX-License-Identifier: MIT

//Deposit Eth into a contract, use a list to determine who can claim
//storing a larger list of users is not efficient and would cause gas issues
//if we needed to loop through all entries, this is for learning purposes only
pragma solidity ^0.6.0;

// Get ETH to USD from Chainlink
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // safemath to check for int overflows
    using SafeMathChainlink for uint256;

    //Address to deposit amount mapping
    mapping(address => uint256) public addressToAmountFunded;

    // array of deposit wallets
    address[] public _funders;

    //addresses of who can claim
    address[] public _claimers;

    //ChainLink Price feed
    AggregatorV3Interface public _priceFeed;

    //add the publisher and another wallet to the claimers list
    constructor(address priceFeed) public {
        _priceFeed = AggregatorV3Interface(priceFeed);
        _claimers.push(msg.sender);
        //hard coded wallet to test mutliple allowed claimers
        _claimers.push(0xA528F58D716dC9a03487d7EEA1DBbD4a52AF4a23);
    }

    function fund() public payable {
        // 18 digit number to be compared with donated amount
        uint256 minimumUSD = 10 * 10**18;

        //is the donated amount less than 10USD?
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "A minimum of $10 USD worth of ETH is required, please increase your funding"
        );

        //if not upsert amount to funders array
        addressToAmountFunded[msg.sender] += msg.value;
        _funders.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = _priceFeed.latestRoundData();
        //ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
    }

    //gets the version of the chainlink pricefeed
    function getVersion() public view returns (uint256) {
        return _priceFeed.version();
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd;
    }

    modifier isClaimer() {
        bool isClaimer = false;
        //is the message sender one of the claimers
        for (uint256 i = 0; i < _claimers.length; i++) {
            if (msg.sender == _claimers[i]) {
                isClaimer = true;
            }
        }
        require(isClaimer);

        _;
    }

    //must pass the isClaimer check to execute
    function withdraw() public payable isClaimer {
        msg.sender.transfer(address(this).balance);

        //iterate through all the funders to make them 0 since the contract is empty
        for (
            uint256 funderIndex = 0;
            funderIndex < _funders.length;
            funderIndex++
        ) {
            address funder = _funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        _funders = new address[](0);
    }
}
