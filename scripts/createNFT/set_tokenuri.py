
from brownie import createNFT, network
from scripts.helpful_scripts import get_player, get_account, OPENSEA_URL

metadata_dic = {
    
}

def main():
    print(f"Working on {network.show_active()}")
    nft = createNFT[-1]
    number_of_nfts = createNFT.tokenCounter()
    print(f"You have {number_of_nfts} tokenIds")
    
    for token in range(number_of_nfts):
        player = get_player(createNFT.tokenIdToPlayer(token))
        if not createNFT.tokenURI(token).startswith("https://"):
            print(f"Setting tokenURI of {token}")
            set_tokenURI(token, createNFT, metadata_dic)
            
def set_tokenURI(token, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token, tokenURI, {"from": account})
    tx.wait(1)
    print(f"You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token)}")
    print("Please wait up to 20 minutes and hit refresh metadata")