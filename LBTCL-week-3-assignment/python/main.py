from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import traceback

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
        # General client for non-wallet-specific commands
        client = get_rpc_client()

        # 1. Create/Load the wallets
        for w in ["Miner", "Alice", "Bob"]:
            try:
                client.createwallet(w)
            except JSONRPCException:
                try:
                    client.loadwallet(w)
                except JSONRPCException:
                    pass

        miner = get_rpc_client("Miner")
        alice = get_rpc_client("Alice")
        bob = get_rpc_client("Bob")

        # 2. Fund Miner and then Alice/Bob
        miner_addr = miner.getnewaddress()
        miner.generatetoaddress(151, miner_addr)

        a_addr = alice.getnewaddress()
        b_addr = bob.getnewaddress()

        miner.sendtoaddress(a_addr, 15.0)
        miner.sendtoaddress(b_addr, 15.0)
        miner.generatetoaddress(6, miner_addr)

        # 3. Construct 2-of-2 multisig
        a_pub = alice.getaddressinfo(alice.getnewaddress())['pubkey']
        b_pub = bob.getaddressinfo(bob.getnewaddress())['pubkey']
        
        msig = client.createmultisig(2, [a_pub, b_pub], "bech32")
        msig_addr = msig['address']
        msig_desc = msig['descriptor']

        # 4. Build funding PSBT
        a_unspent = alice.listunspent()
        b_unspent = bob.listunspent()

        a_utxo = next(u for u in a_unspent if float(u['amount']) >= 10.001)
        b_utxo = next(u for u in b_unspent if float(u['amount']) >= 10.001)

        fund_inputs = [
            {"txid": a_utxo['txid'], "vout": a_utxo['vout']},
            {"txid": b_utxo['txid'], "vout": b_utxo['vout']}
        ]
        
        a_change_addr = alice.getrawchangeaddress()
        b_change_addr = bob.getrawchangeaddress()

        a_change = round(float(a_utxo['amount']) - 10.0001, 8)
        b_change = round(float(b_utxo['amount']) - 10.0001, 8)

        fund_outputs = {
            msig_addr: 20.0,
            a_change_addr: a_change,
            b_change_addr: b_change
        }

        fund_psbt = client.createpsbt(fund_inputs, fund_outputs)

        # 5. Sign & broadcast funding PSBT
        a_fund_psbt = alice.walletprocesspsbt(fund_psbt)
        b_fund_psbt = bob.walletprocesspsbt(a_fund_psbt['psbt'])
        fund_tx = client.finalizepsbt(b_fund_psbt['psbt'])
        fund_txid = client.sendrawtransaction(fund_tx['hex'])

        # 6. Mine 6 blocks
        miner.generatetoaddress(6, miner.getnewaddress())

        # 7. Print balances
        print("Alice balance:", alice.getbalance())
        print("Bob balance:", bob.getbalance())

        # 8. Build spending PSBT
        raw_fund_tx = client.getrawtransaction(fund_txid, True)
        fund_vout = next(v['n'] for v in raw_fund_tx['vout'] if v['scriptPubKey'].get('address') == msig_addr)

        spend_inputs = [{"txid": fund_txid, "vout": fund_vout}]
        spend_outputs = {
            alice.getnewaddress(): 9.999,
            bob.getnewaddress(): 9.999
        }

        spend_psbt = client.createpsbt(spend_inputs, spend_outputs)
        spend_psbt = client.utxoupdatepsbt(spend_psbt, [msig_desc])

        # 9, 10. Sign spending PSBT
        a_spend_psbt = alice.walletprocesspsbt(spend_psbt)
        b_spend_psbt = bob.walletprocesspsbt(a_spend_psbt['psbt'])

        # 11. Extract and broadcast
        spend_tx = client.finalizepsbt(b_spend_psbt['psbt'])
        spend_txid = client.sendrawtransaction(spend_tx['hex'])

        # 12. Mine 6 blocks
        miner.generatetoaddress(6, miner.getnewaddress())

        # 13. Print final balances
        print("Final Alice balance:", alice.getbalance())
        print("Final Bob balance:", bob.getbalance())

        # Output format requires txid_multisig_funding and txid_multisig_spending in out.txt
        with open("out.txt", "w") as f:
            f.write(f"{fund_txid}\n{spend_txid}\n")

    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()