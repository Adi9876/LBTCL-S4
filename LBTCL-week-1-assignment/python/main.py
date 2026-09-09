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

        # Create/Load the wallets, named 'Miner' and 'Trader'.
        def create_or_load_wallet(name):
            try:
                client.createwallet(name)
            except JSONRPCException as e:
                # 103 means it's already created but not loaded? Wait, let's just try loading.
                try:
                    client.loadwallet(name)
                except JSONRPCException:
                    pass
        
        create_or_load_wallet("Miner")
        create_or_load_wallet("Trader")

        miner_client = AuthServiceProxy(f"{base_rpc_url}/wallet/Miner")
        trader_client = AuthServiceProxy(f"{base_rpc_url}/wallet/Trader")

        # Generate spendable balances in the Miner wallet. Determine how many blocks need to be mined.
        # Coinbase outputs require 100 confirmations to mature (BIP 34) before becoming spendable.
        miner_address = miner_client.getnewaddress("Mining Reward")
        client.generatetoaddress(101, miner_address)
        print("Miner balance:", miner_client.getbalance())

        # Load the Trader wallet and generate a new address.
        trader_address = trader_client.getnewaddress("Received")

        # Select 1 mature UTXO > 20 BTC to guarantee exactly 1 vin and 2 vouts (Trader + change)
        unspent = miner_client.listunspent()
        candidate = None
        for u in unspent:
            if u["spendable"] and u["amount"] >= 50:
                candidate = u
                break
        if not candidate:
            for u in unspent:
                if u["spendable"] and u["amount"] > 20:
                    candidate = u
                    break

        to_lock = []
        if candidate:
            to_lock = [
                {"txid": u["txid"], "vout": u["vout"]}
                for u in unspent
                if not (u["txid"] == candidate["txid"] and u["vout"] == candidate["vout"])
            ]
            if to_lock:
                miner_client.lockunspent(False, to_lock)

        # Send 20 BTC from Miner to Trader.
        txid = miner_client.sendtoaddress(trader_address, 20)

        if to_lock:
            miner_client.lockunspent(True, to_lock)

        # Check the transaction in the mempool.
        mempool_entry = client.getmempoolentry(txid)
        print("Mempool entry:", mempool_entry)

        # Mine 1 block to confirm the transaction.
        client.generatetoaddress(1, miner_address)

        # Extract all required transaction details.
        raw_tx = client.getrawtransaction(txid, True)
        
        blockhash = raw_tx["blockhash"]
        block_info = client.getblock(blockhash)
        blockheight = block_info["height"]

        vin_txid = raw_tx["vin"][0]["txid"]
        vin_vout = raw_tx["vin"][0]["vout"]
        vin_raw_tx = client.getrawtransaction(vin_txid, True)
        
        miner_input_address = vin_raw_tx["vout"][vin_vout]["scriptPubKey"]["address"]
        miner_input_amount = vin_raw_tx["vout"][vin_vout]["value"]

        trader_output_amount = 20
        miner_change_address = ""
        miner_change_amount = 0

        for vout in raw_tx["vout"]:
            addr = vout["scriptPubKey"].get("address")
            if addr and addr != trader_address:
                miner_change_address = addr
                miner_change_amount = vout["value"]

        miner_tx_info = miner_client.gettransaction(txid)
        tx_fee = miner_tx_info["fee"]

        # Write the data to out.txt in the specified format given in readme.md.
        with open("out.txt", "w") as f:
            f.write(f"{txid}\n")
            f.write(f"{miner_input_address}\n")
            f.write(f"{miner_input_amount}\n")
            f.write(f"{trader_address}\n")
            f.write(f"{trader_output_amount}\n")
            f.write(f"{miner_change_address}\n")
            f.write(f"{miner_change_amount}\n")
            f.write(f"{tx_fee}\n")
            f.write(f"{blockheight}\n")
            f.write(f"{blockhash}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()