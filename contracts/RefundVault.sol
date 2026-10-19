// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract RefundVault {
    address payable public auctionContract;
    address payable public owner;
    mapping(address => uint) public refunds;

    constructor(address payable _owner) {
        auctionContract = payable(msg.sender);
        owner = _owner;
    }

    function deposit(address _bidder) external payable {
        require(msg.sender == auctionContract, "Only auction can deposit");
        refunds[_bidder] += msg.value;
    }

    function claimRefund() external {
        uint amount = refunds[msg.sender];
        require(amount > 0, "No refund available");

        refunds[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    function closeAuction() external payable {
        require(msg.sender == auctionContract, "Only auction can close");
        owner.transfer(msg.value);
    }
}
