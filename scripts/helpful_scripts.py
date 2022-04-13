from brownie import accounts, config, network, VRFCoordinatorMock, LinkToken, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development" , "ganache-cli", "mainnet-fork", "hardhat"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
PLAYER_MAPPING = {0: "LeBron James",
                  1: "Devin Booker",
                  2: "Mason Plumlee"}


def get_player(player_id):
    return PLAYER_MAPPING[player_id]

def get_account(index=None, id=None):
    if index:
        account = accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        account = accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
        
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    
    return contract

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks")
    account = get_account()
    link_token_contract = LinkToken.deploy({"from": account})
    vrf_coordinator_contract = VRFCoordinatorMock.deploy(link_token_contract, {"from": account})
    print(f"VRF coordinator deployed to {vrf_coordinator_contract.address}")


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Contract funded with {amount} LINK")
    print(f"Funded address: {contract_address}")
    return funding_tx
