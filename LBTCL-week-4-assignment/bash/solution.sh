# Get blockchain info using bitcoin-cli
blockchain_info=$(bitcoin-cli getblockchaininfo)

# Print the blockchain info
echo "$blockchain_info"

# Create/Load the wallets, named 'Miner', 'Employee', and 'Employer'. Have logic to optionally create/load them if they do not exist or not loaded already.

# Generate spendable balances in the Miner wallet (≥ 150 BTC), then send some coins to Employer

# Create a salary transaction of 40 BTC, where the Employer pays the Employee
# Add an absolute timelock of 500 Blocks for the transaction

# Report in a comment what happens when you try to broadcast this transaction

# Mine up to 500th block and broadcast the transaction

# Print the final balances of Employee and Employer wallets

# Create a spending transaction where the Employee spends the fund to a new Employee wallet address
# Add an OP_RETURN output in the spending transaction with the string data "I got my salary, I am rich".

# Sign and broadcast the transaction

# Print the final balances of the Employee and the Employer wallets

# Output the txid of the timelocked funding transaction and the txid of the spending transaction to out.txt
# <txid_timelocked_funding>
# <txid_spending>