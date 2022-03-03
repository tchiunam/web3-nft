from brownie import SimpleCollectible
from scripts.utility.helper import OPENSEA_ASSET_URL, get_account

token_uri = "https://ipfs.io/ipfs/QmUiYehkJqtFwUco6bpAdaKeZESHav5fvAJP7uzYJZRbCY"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(token_uri)
    tx.wait(1)
    print(
        f"Your NFT is available at {OPENSEA_ASSET_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    return simple_collectible


def main():
    deploy_and_create()
