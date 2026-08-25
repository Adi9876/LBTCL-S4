const Client = require('bitcoin-core');
const fs = require('fs');

const client = new Client({
    network: 'regtest',
    username: 'alice',
    password: 'password',
    host: '127.0.0.1', // Host should not include the protocol
    port: 18443 // Ensure the correct port for regtest is used
});

async function main() {
    // Example: Get blockchain info
    const blockchainInfo = await client.getBlockchainInfo();
    console.log('Blockchain Info:', blockchainInfo);

    // Create/Load the wallets, named 'Miner' and 'Trader'. Have logic to optionally create/load them if they do not exist or not loaded already.

    // Generate spendable balances in the Miner wallet. How many blocks needs to be mined?

    // Load Trader wallet and generate a new address

    // Create parent transaction in the Miner wallet, sending 70 BTC to the Trader wallet address
    // Remember to signal for RBF

    // Sign and broadcast the transaction

    // Output the parent transaction in the specified format to parent.json

    // Create and child transaction that spends the parent transaction output

    // Output the child transaction in the specified format to child.json

    // Fee bump the Parent transaction using RBF. Do not use bitcoin-cli bumpfee

    // Sign and broadcast the fee-bumped transaction

    // Output the fee-bumped parent transaction in the specified format to parent-rbf.json

}

main().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});