# Get blockchain info using bitcoin-cli
blockchain_info=$(bitcoin-cli getblockchaininfo)

# Print the blockchain info
echo "$blockchain_info"

# Create/Load the wallets, named 'Miner', 'Alice' and 'Bob'. Have logic to optionally create/load them if they do not exist or not loaded already.

# Generate spendable balances in the Miner wallet (≥ 150 BTC), then send 15 BTC each to Alice and Bob

# Construct 2-of-2 multisig (Alice & Bob) and build funding PSBT to contribute 20 BTC total

# Sign & broadcast the funding PSBT

# Mine 6 blocks to confirm

# Print balances for Alice and Bob

# Build spending PSBT to spend funds from the multisig, ensuring 10 BTC is equally distributed back between Alice and Bob after accounting for fees

# Sign & broadcast the spending PSBT

# Mine 6 blocks to confirm the spending transaction

# Print final balances for Alice and Bob