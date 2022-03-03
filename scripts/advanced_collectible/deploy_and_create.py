from brownie import AdvancedCollectible, config, network
from scripts.utility.helper import (OPENSEA_ASSET_URL, fund_with_link,
                                    get_account, get_contract)

token_uri = "https://ipfs.io/ipfs/QmUiYehkJqtFwUco6bpAdaKeZESHav5fvAJP7uzYJZRbCY"


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
