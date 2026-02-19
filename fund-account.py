#!/usr/bin/env python3
"""Quick script to fund an account on LocalNet"""

from algokit_utils import get_localnet_default_account
from algosdk.v2client import algod

# Connect to LocalNet
algod_client = algod.AlgodClient(
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "http://localhost:4001"
)

# Get a funded dispenser account
dispenser = get_localnet_default_account(algod_client)

# Account to fund
receiver = "SW4BTZGCCNMSDYSANRLKFQOZNYRKH4B7J6DNSEUAYPSRGOYZRGKQEAW5EY"

# Send 10 ALGO
from algosdk.transaction import PaymentTxn

params = algod_client.suggested_params()
txn = PaymentTxn(
    sender=dispenser.address,
    sp=params,
    receiver=receiver,
    amt=10_000_000  # 10 ALGO in microAlgos
)

signed_txn = txn.sign(dispenser.private_key)
txid = algod_client.send_transaction(signed_txn)

print(f"Funded {receiver} with 10 ALGO")
print(f"Transaction ID: {txid}")
