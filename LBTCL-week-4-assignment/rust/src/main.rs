use bitcoin::hex::DisplayHex;
use bitcoincore_rpc::bitcoin::Amount;
use bitcoincore_rpc::{Auth, Client, RpcApi};
use serde::Deserialize;
use serde_json::json;
use std::fs::File;
use std::io::Write;

// Node access params
const RPC_URL: &str = "http://127.0.0.1:18443"; // Default regtest RPC port
const RPC_USER: &str = "alice";
const RPC_PASS: &str = "password";

// You can use calls not provided in RPC lib API using the generic `call` function.
// An example of using the `send` RPC call, which doesn't have exposed API.
// You can also use serde_json `Deserialize` derivation to capture the returned json result.
fn send(rpc: &Client, addr: &str) -> bitcoincore_rpc::Result<String> {
    let args = [
        json!([{addr : 100 }]), // recipient address
        json!(null),            // conf target
        json!(null),            // estimate mode
        json!(null),            // fee rate in sats/vb
        json!(null),            // Empty option object
    ];

    #[derive(Deserialize)]
    struct SendResult {
        complete: bool,
        txid: String,
    }
    let send_result = rpc.call::<SendResult>("send", &args)?;
    assert!(send_result.complete);
    Ok(send_result.txid)
}

fn main() -> bitcoincore_rpc::Result<()> {
    // Connect to Bitcoin Core RPC
    let rpc = Client::new(
        RPC_URL,
        Auth::UserPass(RPC_USER.to_owned(), RPC_PASS.to_owned()),
    )?;

    // Get blockchain info
    let blockchain_info = rpc.get_blockchain_info()?;
    println!("Blockchain Info: {:?}", blockchain_info);

    // Create/Load the wallets, named 'Miner', 'Employee', and 'Employer'. Have logic to optionally create/load them if they do not exist or not loaded already.

    // Generate spendable balances in the Miner wallet (≥ 150 BTC), then send some coins to Employer

    // Create a salary transaction of 40 BTC, where the Employer pays the Employee
    // Add an absolute timelock of 500 Blocks for the transaction

    // Report in a comment what happens when you try to broadcast this transaction

    // Mine up to 500th block and broadcast the transaction

    // Print the final balances of Employee and Employer wallets

    // Create a spending transaction where the Employee spends the fund to a new Employee wallet address
    // Add an OP_RETURN output in the spending transaction with the string data "I got my salary, I am rich".

    // Sign and broadcast the transaction

    // Print the final balances of the Employee and the Employer wallets

    // Output the txid of the timelocked funding transaction and the txid of the spending transaction to out.txt
    // <txid_timelocked_funding>
    // <txid_spending>

    Ok(())
}
