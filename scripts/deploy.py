from brownie import createNFT, config, network
from scripts.helpful_scripts import get_contract, get_account

from scripts.helpful_scripts import fund_with_link
import time

def deploy_createNFT():
    account = get_account()
    tx = createNFT.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account}
    )
    
    contract = fund_with_link(tx.address, account)
    contract.wait(1)
    creation_tx = tx.createCollectible({"from": account})
    creation_tx.wait(1)

    print(tx.tokenCounter())
    print("New token minted!")
    return tx, creation_tx
    



def main():
    deploy_createNFT()