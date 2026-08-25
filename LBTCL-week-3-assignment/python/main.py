from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def main():

    try:
        # Connect to Bitcoin Core RPC with basic credentials
        rpc_user = "alice"
        rpc_password = "password"
        rpc_host = "127.0.0.1"
        rpc_port = 18443
        base_rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"

        # General client for non-wallet-specific commands
        client = AuthServiceProxy(base_rpc_url)

        # Get blockchain info
        blockchain_info = client.getblockchaininfo()
        print("Blockchain Info:", blockchain_info)

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

if __name__ == "__main__":
    main()