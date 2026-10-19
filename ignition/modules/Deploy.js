import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("AuctionModule", (m) => {
  const auction = m.contract("Auction", [3600]);

  return { auction };
});
