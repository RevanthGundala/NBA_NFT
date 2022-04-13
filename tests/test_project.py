from brownie import createNFT, network
import pytest, time

from scripts.deploy import deploy_createNFT
from scripts.helpful_scripts import  LOCAL_BLOCKCHAIN_ENVIRONMENTS

def test_can_create_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    tx, creation_tx = deploy_createNFT()
    time.sleep(60)

    assert tx.tokenCounter() == 1

