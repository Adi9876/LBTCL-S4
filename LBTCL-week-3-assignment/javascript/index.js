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

    // Create/Load the wallets, named 'Miner', 'Alice' and 'Bob'. Have logic to optionally create/load them if they do not exist or not loaded already.

    // Generate spendable balances in the Miner wallet (≥ 150 BTC), then send 15 BTC each to Alice and Bob

    // Construct 2-of-2 multisig (Alice & Bob) and build funding PSBT to contribute 20 BTC total

    // Sign & broadcast the funding PSBT

    // Mine 6 blocks to confirm

    // Print balances for Alice and Bob

    // Build spending PSBT to spend funds from the multisig, ensuring 10 BTC is equally distributed back between Alice and Bob after accounting for fees

    // Sign & broadcast the spending PSBT

    // Mine 6 blocks to confirm the spending transaction

    // Print final balances for Alice and Bob

}

main().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});