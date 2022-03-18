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
    address[] public funders;

    //addresses of who can claim
    address[] public claimers;

    //add the publisher and another wallet to the claimers list
    constructor() public {
        claimers.push(msg.sender);
        claimers.push(0xA528F58D716dC9a03487d7EEA1DBbD4a52AF4a23);
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
        funders.push(msg.sender);
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
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

    //modifier: https://medium.com/coinmonks/solidity-tutorial-all-about-modifiers-a86cf81c14cb
    modifier isClaimer() {
        bool isClaimer = false;
        //is the message sender one of the claimers
        for (uint256 i = 0; i < claimers.length; i++) {
            if (msg.sender == claimers[i]) {
                isClaimer = true;
            }
        }
        require(isClaimer);

        _;
    }

    // isClaimer modifer will first check the condition inside it
    // and
    // if true, withdraw function will be executed
    function withdraw() public payable isClaimer {
        msg.sender.transfer(address(this).balance);

        //iterate through all the funders to make them 0 since the contract is empty
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        funders = new address[](0);
    }
}
