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

    // Create two wallets called Miner and Alice

    // Fund the Miner wallet

    // Send some coins to Alice's wallet

    // Create refund transaction where Alice pays 10 BTC to Miner
    // Additionally, add a relative timelock of 10 blocks

    // Sign and broadcast the transaction. Is the broadcast successful?

    // Generate 10 blocks

    // Broadcast the transaction again. Is the broadcast successful now?

    // Output the transaction ID to `out.txt`

}

main().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});