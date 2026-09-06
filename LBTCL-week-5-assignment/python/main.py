import traceback
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def get_rpc_client(wallet_name=""):
    rpc_user = "alice"
    rpc_password = "password"
    rpc_host = "127.0.0.1"
    rpc_port = 18443
    url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
    if wallet_name:
        url += f"/wallet/{wallet_name}"
    return AuthServiceProxy(url)

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
        print("blockchain Info:", blockchain_info)

        # Create two wallets called Miner and Alice
        for w in ["Miner", "Alice"]:
            try:
                client.createwallet(w)
            except JSONRPCException:
                try:
                    client.loadwallet(w)
                except JSONRPCException:
                    pass
        miner = get_rpc_client("Miner")
        alice = get_rpc_client("Alice")

        # Fund the Miner wallet
        miner_addr = miner.getnewaddress()
        miner.generatetoaddress(151, miner_addr)

        # Send some coins to Alice's wallet
        alice_addr = alice.getnewaddress()
        miner.sendtoaddress(alice_addr, 20.0)
        miner.generatetoaddress(6, miner_addr)
        print("alice balance funds aftr:", alice.getbalance())

        # Create refund transaction where Alice pays 10 BTC to Miner
        # Additionally, add a relative timelock of 10 blocks
        alice_unspent = alice.listunspent()
        alice_utxo = next(u for u in alice_unspent if float(u['amount']) >= 10.0001)

        inputs = [{
            "txid": alice_utxo['txid'],
            "vout": alice_utxo['vout'],
            "sequence": 10  # 10 blocks relative timelock (BIP 68)
        }]

        miner_refnd_addr = miner.getnewaddress()
        outputs = {
            miner_refnd_addr: 10.0,
            alice.getrawchangeaddress(): round(float(alice_utxo['amount']) - 10.0001, 8)
        }

        psbt_raw = alice.createpsbt(inputs, outputs)
        psbt_signed = alice.walletprocesspsbt(psbt_raw)
        refund_tx = alice.finalizepsbt(psbt_signed['psbt'])

        # Sign and broadcast the transaction. Is the broadcast successful?
        try:
            alice.sendrawtransaction(refund_tx['hex'])
            print("broadcast successful earlier")
        except JSONRPCException as e:
            print("broadcast failed as expected (relative timelock not met):", e)

        # Generate 10 blocks
        miner.generatetoaddress(10, miner_addr)

        # Broadcast the transaction again. Is the broadcast successful now?
        refund_txid = alice.sendrawtransaction(refund_tx['hex'])
        print("broadcast succesful txid:", refund_txid)
        miner.generatetoaddress(1, miner_addr)
        print("alice fnial balance:", alice.getbalance())

        # Output the transaction ID to `out.txt`
        with open("out.txt", "w") as f:
            f.write(f"{refund_txid}\n")

    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()