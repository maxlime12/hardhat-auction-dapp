// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./RefundVault.sol";

contract Auction {
    address public owner;
    address public highestBidder;
    uint public highestBid;
    uint public endTime;
    bool public ended;
    RefundVault public vault;

    event BidPlaced(address indexed bidder, uint amount);
    event AuctionEnded(address winner, uint amount);

    constructor(uint _durationInSeconds) {
        owner = msg.sender;
        endTime = block.timestamp + _durationInSeconds;
        vault = new RefundVault(payable(msg.sender));
    }

    function bid() external payable {
        require(block.timestamp < endTime, "Auction already ended.");
        require(msg.value > highestBid, "There already is a higher bid.");

        if (highestBid > 0) {
            vault.deposit{value: highestBid}(highestBidder);
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
        emit BidPlaced(msg.sender, msg.value);
    }

    function endAuction() external {
        require(block.timestamp >= endTime, "Auction not ended yet.");
        require(!ended, "AuctionEnd has already been called.");

        ended = true;
        emit AuctionEnded(highestBidder, highestBid);
        vault.closeAuction{value: highestBid}();
    }
}
