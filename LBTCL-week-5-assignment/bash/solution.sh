# Get blockchain info using bitcoin-cli
blockchain_info=$(bitcoin-cli getblockchaininfo)

# Print the blockchain info
echo "$blockchain_info"

# Create two wallets called Miner and Alice

# Fund the Miner wallet

# Send some coins to Alice's wallet

# Create refund transaction where Alice pays 10 BTC to Miner
# Additionally, add a relative timelock of 10 blocks

# Sign and broadcast the transaction. Is the broadcast successful?

# Generate 10 blocks

# Broadcast the transaction again. Is the broadcast successful now?

# Output the transaction ID to `out.txt`