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
        print("Blockchain Info:", blockchain_info)

        # Create/Load the wallets, named 'Miner', 'Employee', and 'Employer'. Have logic to optionally create/load them if they do not exist or not loaded already.
        for w in ["Miner", "Employee", "Employer"]:
            try:
                client.createwallet(w)
            except JSONRPCException:
                try:
                    client.loadwallet(w)
                except JSONRPCException:
                    pass

        miner = get_rpc_client("Miner")
        employee = get_rpc_client("Employee")
        employer = get_rpc_client("Employer")

        # Generate spendable balances in the Miner wallet (≥ 150 BTC), then send some coins to Employer
        miner_addr = miner.getnewaddress()
        miner.generatetoaddress(151, miner_addr)
        employer_addr = employer.getnewaddress()
        miner.sendtoaddress(employer_addr, 50.0)
        miner.generatetoaddress(6, miner_addr)

        # Create a salary transaction of 40 BTC, where the Employer pays the Employee
        # Add an absolute timelock of 500 Blocks for the transaction
        emp_unspent = employer.listunspent()
        emp_utxo = next(u for u in emp_unspent if float(u['amount']) > 40.0)

        inputs = [{
            "txid": emp_utxo['txid'],
            "vout": emp_utxo['vout'],
            "sequence": 0xfffffffe
        }]

        employee_addr = employee.getnewaddress()
        outputs = {
            employee_addr: 40.0,
            employer.getrawchangeaddress(): round(float(emp_utxo['amount']) - 40.0001, 8)
        }

        fund_psbt_raw = employer.createpsbt(inputs, outputs, 500)
        fund_signed = employer.walletprocesspsbt(fund_psbt_raw)
        fund_tx = employer.finalizepsbt(fund_signed['psbt'])

        # Report in a comment what happens when you try to broadcast this transaction
        # If we broadcast before block 500, the node rejects the transaction with a 'bad-txns-nonfinal' error.
        try:
            employer.sendrawtransaction(fund_tx['hex'])
        except JSONRPCException as e:
            print("Broadcast failed as expected:", e)

        # Mine up to 500th block and broadcast the transaction
        current_height = client.getblockchaininfo()['blocks']
        blocks_to_mine = max(0, 500 - current_height)
        if blocks_to_mine > 0:
            miner.generatetoaddress(blocks_to_mine, miner_addr)
        
        fund_txid = employer.sendrawtransaction(fund_tx['hex'])
        miner.generatetoaddress(6, miner_addr)

        # Print the final balances of Employee and Employer wallets
        print("Employee balance after funding:", employee.getbalance())
        print("Employer balance after funding:", employer.getbalance())

        # Create a spending transaction where the Employee spends the fund to a new Employee wallet address
        # Add an OP_RETURN output in the spending transaction with the string data "I got my salary, I am rich".
        emp_list = employee.listunspent()
        spend_utxo = next(u for u in emp_list if u['txid'] == fund_txid)
        
        spend_inputs = [{
            "txid": spend_utxo['txid'],
            "vout": spend_utxo['vout']
        }]
        
        op_return_data = "I got my salary, I am rich".encode('utf-8').hex()
        spend_outputs = [
            {employee.getnewaddress(): round(float(spend_utxo['amount']) - 0.0001, 8)},
            {"data": op_return_data}
        ]
        spend_psbt_raw = employee.createpsbt(spend_inputs, spend_outputs)

        # Sign and broadcast the transaction
        spend_signed = employee.walletprocesspsbt(spend_psbt_raw)
        spend_tx = employee.finalizepsbt(spend_signed['psbt'])
        spend_txid = employee.sendrawtransaction(spend_tx['hex'])
        miner.generatetoaddress(6, miner_addr)

        # Print the final balances of the Employee and the Employer wallets
        print("Employee final balance:", employee.getbalance())
        print("Employer final balance:", employer.getbalance())

        # Output the txid of the timelocked funding transaction and the txid of the spending transaction to out.txt
        # <txid_timelocked_funding>
        # <txid_spending>
        with open("out.txt", "w") as f:
            f.write(f"{fund_txid}\n{spend_txid}\n")

    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()