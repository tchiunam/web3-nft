import time

import pytest
from brownie import network
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.utility.helper import (LOCAL_ENVIRONMENTS, get_account,
                                    get_contract)


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_ENVIRONMENTS:
        pytest.skip("This is for integration testing")
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(60)
    assert advanced_collectible.tokenCounter() == 1
