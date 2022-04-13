from scripts.helpful_scripts import fund_with_link, get_account
from brownie import createNFT


def main():
    account = get_account()
    nbaNFT = createNFT[-1]
    fund_with_link(nbaNFT.address, account)
    tx = nbaNFT.createCollectible({"from": account})
    tx.wait(1)
    
    print(f"You have created {nbaNFT.tokenCounter()} NFTS")
    print("NFT Created!")
    