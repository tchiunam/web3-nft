from brownie import AdvancedCollectible
from scripts.utility.helper import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address,
                   amount=Web3.toWei(0.1, "ether"))
    creation_transaction = advanced_collectible.createCollectible({
                                                                  "from": account})
    creation_transaction.wait(1)
    print("Created collectible")