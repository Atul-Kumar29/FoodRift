#!/usr/bin/env python3
"""Fund all KMD wallet accounts on LocalNet"""

from algokit_utils import get_localnet_default_account
from algosdk.v2client import algod
from algosdk.kmd import KMDClient
from algosdk.transaction import PaymentTxn

# Connect to LocalNet
algod_client = algod.AlgodClient(
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "http://localhost:4001"
)

kmd_client = KMDClient(
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "http://localhost:4002"
)

# Get dispenser account
dispenser = get_localnet_default_account(algod_client)
print(f"Dispenser: {dispenser.address}")

# Get all wallets
wallets = kmd_client.list_wallets()

# Find the unencrypted-default-wallet
wallet_id = None
for wallet in wallets:
    if wallet["name"] == "unencrypted-default-wallet":
        wallet_id = wallet["id"]
        break

if not wallet_id:
    print("Could not find unencrypted-default-wallet")
    exit(1)

# Get wallet handle
wallet_handle = kmd_client.init_wallet_handle(wallet_id, "")

# List all accounts in the wallet
accounts = kmd_client.list_keys(wallet_handle)

print(f"\nFunding {len(accounts)} accounts with 100 ALGO each...\n")

params = algod_client.suggested_params()

for account in accounts:
    if account == dispenser.address:
        print(f"Skipping dispenser account: {account}")
        continue
    
    try:
        # Check current balance
        account_info = algod_client.account_info(account)
        current_balance = account_info['amount'] / 1_000_000
        
        if current_balance >= 10:
            print(f"✓ {account} already has {current_balance} ALGO")
            continue
        
        # Send 100 ALGO
        txn = PaymentTxn(
            sender=dispenser.address,
            sp=params,
            receiver=account,
            amt=100_000_000  # 100 ALGO
        )
        
        signed_txn = txn.sign(dispenser.private_key)
        txid = algod_client.send_transaction(signed_txn)
        
        print(f"✓ Funded {account} with 100 ALGO (txid: {txid[:8]}...)")
        
    except Exception as e:
        print(f"✗ Failed to fund {account}: {e}")

print("\nDone! All accounts funded.")
