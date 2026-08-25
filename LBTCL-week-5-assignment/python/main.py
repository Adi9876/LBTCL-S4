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

        # Create two wallets called Miner and Alice

        # Fund the Miner wallet

        # Send some coins to Alice's wallet

        # Create refund transaction where Alice pays 10 BTC to Miner
        # Additionally, add a relative timelock of 10 blocks

        # Sign and broadcast the transaction. Is the broadcast successful?

        # Generate 10 blocks

        # Broadcast the transaction again. Is the broadcast successful now?

        # Output the transaction ID to `out.txt`

if __name__ == "__main__":
    main()