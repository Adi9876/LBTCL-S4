from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from decimal import Decimal

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

        # Create/Load the wallets, named 'Miner' and 'Trader'. Have logic to optionally create/load them if they do not exist or not loaded already.
        try:
            client.createwallet("Miner")
        except JSONRPCException:
            try: client.loadwallet("Miner")
            except JSONRPCException: pass
        
        try:
            client.createwallet("Trader")
        except JSONRPCException:
            try: client.loadwallet("Trader")
            except JSONRPCException: pass

        miner = AuthServiceProxy(f"{base_rpc_url}/wallet/Miner")
        trader = AuthServiceProxy(f"{base_rpc_url}/wallet/Trader")

        # Generate spendable balances in the Miner wallet. How many blocks needs to be mined?
        miner_addr = miner.getnewaddress()
        client.generatetoaddress(105, miner_addr)

        # Load Trader wallet and generate a new address
        trader_addr = trader.getnewaddress()
        miner_change = miner.getnewaddress()

        # Create parent transaction in the Miner wallet, sending 70 BTC to the Trader wallet address
        # Remember to signal for RBF
        valid_unspent = [u for u in miner.listunspent() if u['amount'] >= 50]
        in1, in2 = valid_unspent[0], valid_unspent[1]
        inputs = [
            {"txid": in1['txid'], "vout": in1['vout'], "sequence": 4294967293},
            {"txid": in2['txid'], "vout": in2['vout'], "sequence": 4294967293}
        ]
        outputs = {trader_addr: 70, miner_change: 29.99999}
        raw_parent = miner.createrawtransaction(inputs, outputs)

        # Sign and broadcast the transaction
        signed_parent = miner.signrawtransactionwithwallet(raw_parent)
        parent_txid = miner.sendrawtransaction(signed_parent['hex'])

        # Output the parent transaction in the specified format to parent.json
        decoded_parent = client.decoderawtransaction(signed_parent['hex'])
        mempool_parent = client.getmempoolentry(parent_txid)
        parent_json = {
            "txid": parent_txid,
            "input": [{"txid": vin['txid'], "vout": vin['vout']} for vin in decoded_parent['vin']],
            "output": [{"scriptpubkey": vout['scriptPubKey']['hex'], "amount": float(vout['value'])} for vout in decoded_parent['vout']],
            "fee": float(mempool_parent['fees']['base']),
            "weight": decoded_parent['weight']
        }
        with open('parent.json', 'w') as f:
            json.dump(parent_json, f, indent=3)

        # Create and child transaction that spends the parent transaction output
        change_vout = next(vout['n'] for vout in decoded_parent['vout'] if abs(float(vout['value']) - 29.99999) < 0.000001)
        child_addr = miner.getnewaddress()
        raw_child = miner.createrawtransaction([{"txid": parent_txid, "vout": change_vout}], {child_addr: 29.99998})
        
        signed_child = miner.signrawtransactionwithwallet(raw_child)
        child_txid = miner.sendrawtransaction(signed_child['hex'])

        # Output the child transaction in the specified format to child.json
        decoded_child = client.decoderawtransaction(signed_child['hex'])
        mempool_child = client.getmempoolentry(child_txid)
        child_json = {
            "txid": child_txid,
            "input": [{"txid": vin['txid'], "vout": vin['vout']} for vin in decoded_child['vin']],
            "output": [{"scriptpubkey": vout['scriptPubKey']['hex'], "amount": float(vout['value'])} for vout in decoded_child['vout']],
            "fee": float(mempool_child['fees']['base']),
            "weight": decoded_child['weight']
        }
        with open('child.json', 'w') as f:
            json.dump(child_json, f, indent=3)

        # Fee bump the Parent transaction using RBF. Do not use bitcoin-cli bumpfee
        outputs_rbf = {trader_addr: 70, miner_change: 29.99989}
        raw_rbf = miner.createrawtransaction(inputs, outputs_rbf)

        # Sign and broadcast the fee-bumped transaction
        signed_rbf = miner.signrawtransactionwithwallet(raw_rbf)
        txid_rbf_ = miner.sendrawtransaction(signed_rbf['hex'])

        # Output the fee-bumped parent transaction in the specified format to parent-rbf.json
        decoded_rbf = client.decoderawtransaction(signed_rbf['hex'])
        mempool_rbf = client.getmempoolentry(txid_rbf_)
        rbf_json = {
            "txid": txid_rbf_,
            "input": [{"txid": vin['txid'], "vout": vin['vout']} for vin in decoded_rbf['vin']],
            "output": [{"scriptpubkey": vout['scriptPubKey']['hex'], "amount": float(vout['value'])} for vout in decoded_rbf['vout']],
            "fee": float(mempool_rbf['fees']['base']),
            "weight": decoded_rbf['weight']
        }
        with open('parent-rbf.json', 'w') as f:
            json.dump(rbf_json, f, indent=3)

    except JSONRPCException as e:
        print(f"RPC Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()