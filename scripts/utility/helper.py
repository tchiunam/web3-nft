from brownie import (Contract, LinkToken, VRFCoordinatorMock, accounts, config,
                     network)
from web3 import Web3

OPENSEA_ASSET_URL = "https://testnets.opensea.io/assets/{}/{}"
LOCAL_ENVIRONMENTS = [
    "development",
    "mainnet-fork"
]
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index: int = None, id: str = None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_ENVIRONMENTS:
        return accounts[0]
    elif network.show_active() == "ganache-local":
        return accounts.add(config["wallets"]["local-ui"][0]["private_key"])

    return accounts.add(config["wallets"]["metamask"][0]["private_key"])


contract_to_mock = {"link_token": LinkToken,
                    "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks ...")
    account = get_account()
    print("Deploying Mock LinkToken ...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator ...")
    vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("Mock deployed")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(
        contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx
