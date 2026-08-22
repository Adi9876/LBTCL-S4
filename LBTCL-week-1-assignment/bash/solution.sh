#!/usr/bin/env bash

# Get blockchain info using bitcoin-cli
blockchain_info=$(bitcoin-cli -regtest getblockchaininfo)

# Print the blockchain info
echo "$blockchain_info"

# Create/Load the wallets, named 'Miner' and 'Trader'. Have logic to optionally create/load them if they do not exist or not loaded already.
bitcoin-cli -regtest -named createwallet wallet_name="Miner" 2>/dev/null || bitcoin-cli -regtest -named loadwallet filename="Miner" 2>/dev/null || true
bitcoin-cli -regtest -named createwallet wallet_name="Trader" 2>/dev/null || bitcoin-cli -regtest -named loadwallet filename="Trader" 2>/dev/null || true

# Generate spendable balances in the Miner wallet. How many blocks needs to be mined?
# We need to mine at least 101 blocks because coinbase outputs require 100 confirmations to mature.
miner_address=$(bitcoin-cli -regtest -rpcwallet=Miner getnewaddress "Mining Reward")
bitcoin-cli -regtest generatetoaddress 101 "$miner_address" > /dev/null

# Print the balance of the Miner wallet
miner_balance=$(bitcoin-cli -regtest -rpcwallet=Miner getbalance)
echo "Miner balance: $miner_balance"

# Load Trader wallet and generate a new address
trader_address=$(bitcoin-cli -regtest -rpcwallet=Trader getnewaddress "Received")

# Send 20 BTC from Miner to Trader
txid=$(bitcoin-cli -regtest -rpcwallet=Miner sendtoaddress "$trader_address" 20)

# Check transaction in mempool
mempool_entry=$(bitcoin-cli -regtest getmempoolentry "$txid")
echo "$mempool_entry"

# Mine 1 block to confirm the transaction
bitcoin-cli -regtest generatetoaddress 1 "$miner_address" > /dev/null

# Extract all required transaction details
raw_tx=$(bitcoin-cli -regtest getrawtransaction "$txid" true)

blockhash=$(echo "$raw_tx" | jq -r '.blockhash')
block_info=$(bitcoin-cli -regtest getblock "$blockhash")
blockheight=$(echo "$block_info" | jq -r '.height')

vin_txid=$(echo "$raw_tx" | jq -r '.vin[0].txid')
vin_vout=$(echo "$raw_tx" | jq -r '.vin[0].vout')
vin_raw_tx=$(bitcoin-cli -regtest getrawtransaction "$vin_txid" true)
miner_input_address=$(echo "$vin_raw_tx" | jq -r ".vout[$vin_vout].scriptPubKey.address")
miner_input_amount=$(echo "$vin_raw_tx" | jq -r ".vout[$vin_vout].value")

trader_output_amount=20
miner_change_address=$(echo "$raw_tx" | jq -r ".vout[] | select(.scriptPubKey.address != \"$trader_address\") | .scriptPubKey.address")
miner_change_amount=$(echo "$raw_tx" | jq -r ".vout[] | select(.scriptPubKey.address != \"$trader_address\") | .value")

miner_tx_info=$(bitcoin-cli -regtest -rpcwallet=Miner gettransaction "$txid")
tx_fee=$(echo "$miner_tx_info" | jq -r '.fee')

# Write the data to out.txt in the specified format given in readme.md
cat <<EOF > out.txt
$txid
$miner_input_address
$miner_input_amount
$trader_address
$trader_output_amount
$miner_change_address
$miner_change_amount
$tx_fee
$blockheight
$blockhash
EOF