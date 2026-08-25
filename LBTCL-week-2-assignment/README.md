# Learning Bitcoin from the Command Line - Week 2: Fee bumping a transaction

## Overview
In this second week you will:
1. **Create** two wallets (`Miner` and `Trader`) and fund them on `regtest`. 
2. **Build & broadcast** a _Parent_ transaction that is RBF-enabled. 
3. **Craft & broadcast** a _Child_ transaction that spends from the parent (CPFP). 
4. **Replace** the original parent with a higher-fee RBF transaction. 
5. **Record** all three transactions in neatly formatted JSON files (parent.json, child.json, parent-rbf.json).
6. **Target Locations** for the solution code for each languages are given below:
   1. Bash: [solution.sh](./bash/solution.sh)
   2. Javascript: [index.js](./javascript/index.js)
   3. Python: [main.py](./python/main.py)
   4. Rust: [main.rs](./rust/src/main.rs)

## Problem Statement

Wallets sometimes need to “fee-bump” transactions when the mempool is congested. Two common strategies are:
- **Replace-By-Fee (RBF):** broadcast a new transaction with the same inputs and a higher fee.
- **Child-Pays-for-Parent (CPFP):** spend an output of the low-fee transaction with a high-fee child so miners collect both fees.

Because an RBF replacement invalidates the parent’s outputs, RBF and CPFP cannot safely be combined on the **same** parent.
This assignment demonstrates that interaction.

## Solution Requirements

Implement the following tasks in exactly one of the language-specific directories: `bash`, `javascript`, `python`, or `rust`.

1. Create two wallets named `Miner` and `Trader`.
2. Fund the `Miner` wallet with at least 3 block rewards worth of satoshis (Starting balance: 150 BTC).
3. Craft a transaction from `Miner` to `Trader` with the following structure (let's call it the `Parent` transaction):
   - Input[0]: 50 BTC block reward.
   - Input[1]: 50 BTC block reward.
   - Output[0]: 70 BTC to `Trader`.
   - Output[1]: 29.99999 BTC change-back to `Miner`.
   - Signal for RBF (Enable RBF for the transaction).
4. Sign and broadcast the `Parent` transaction but do not mine it yet.
5. Make queries to the node's mempool to get the `Parent` transaction details.
   - Use `bitcoin-cli help` to get all the category-specific commands (wallet, mempool, chain, etc.).
   - Use `bitcoin-cli help <command-name>` to get usage information of specific commands.
   - Use `jq` to fetch data from `bitcoin-cli` output into bash variables and use `jq` again to craft your JSON from the variables.
   - You might have to make multiple CLI calls to get all the details.
   - Use the details to craft a JSON variable with the format mentioned below in the [Output Format](#output-format) section.
6. Output the above JSON to a file named `parent.json`.
7. Create and broadcast new transaction that spends from the above transaction (the `Parent`). Let's call it the `Child` transaction.
   - Input[0]: `Miner`'s output of the `Parent` transaction.
   - Output[0]: `Miner`'s new address. 29.99998 BTC.
8. Get the `Child` transaction details and output them to a file named `child.json`.
9. Now, fee bump the `Parent` transaction using RBF. Do not use `bitcoin-cli bumpfee`, instead hand-craft a conflicting transaction, that has the same inputs as the `Parent` but different outputs, adjusting their values to bump the fee of `Parent` by 10,000 satoshis.
10. Sign and broadcast the new Parent transaction.
11. Get the replaced `Parent` transaction details and output them to a file named `parent-rbf.json`.

> **Note:** To connect to bitcoin core rpc, via various language specific clients, use the following credentials
> username: alice
> password: password

### Output Format

```json
{
   "txid": "<txid>",
   "input": [
      {
         "txid": "<txid>", 
         "vout": "<num>"
      }
   ],
   "output": [
      {
         "scriptpubkey": "<scriptpubkey>", 
         "amount": "<amount in BTC>"
      }
   ],
   "fee": "<num>",
   "weight": "<num>"
}
```

## Local Testing

### Prerequisites

| Language       | Prerequisite packages       |
| -------------- | --------------------------- |
| **Bash**       | `jq`, `curl`, `wget`, `tar` |
| **JavaScript** | Node.js ≥ 20, `npm`         |
| **Python**     | Python ≥ 3.9                |
| **Rust**       | Rust stable toolchain       |


- Install `jq` tool for parsing JSON data if you don't have it installed.
- Install Node.js and npm to run the test script.
- Node version 20 or higher is recommended. You can install Node.js using the following command:
  ```
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
  source ~/.nvm/nvm.sh
  nvm install --lts
  ```
- Install the required npm packages by running `npm install`.

### Local Testing Steps
It's a good idea to run the whole test locally to ensure your code is working properly.
- Uncomment the specific line in [run.sh](./run.sh) corresponding to your language of choice.
- Grant execution permission to [test.sh](./test.sh), by running `chmod +x ./test.sh`.
- Execute `./test.sh`.
- The test script will run your script and verify the output. If the test script passes, you have successfully completed the challenge and are ready to submit your solution.

> **Note:** There is a pre-cooked setup script available [here](./setup-bitcoin-node.sh) to download and start bitcoind. You may use that script for all local testing purposes. 

### Common Issues
- Your submission should not stop the Bitcoin Core daemon at any point.
- Linux and MacOS are the recommended operating systems for this challenge. If you are using Windows, you may face compatibility issues.
- The autograder will run the test script on an Ubuntu 22.04 environment. Make sure your script is compatible with this environment.
- If you are unable to run the test script locally, you can submit your solution and check the results on the Github.

## Submission

- Commit all code inside the appropriate language directory and the modified `run.sh`.
  ```
  git add .
  git commit -m "Week 2 solution"
  ```
- Push to the main branch:
  ```
    git push origin main
  ```
- The autograder will run your script against a test script to verify the functionality.
- Check the status of the autograder on the Github Classroom portal to see if it passed successfully or failed. Once you pass the autograder with a score of 100, you have successfully completed the challenge.
- You can submit multiple times before the deadline. The latest submission before the deadline will be considered your final submission.
- You will lose access to the repository after the deadline.

## Resources

- Useful bash script examples: [https://linuxhint.com/30_bash_script_examples/](https://linuxhint.com/30_bash_script_examples/)
- Useful `jq` examples: [https://www.baeldung.com/linux/jq-command-json](https://www.baeldung.com/linux/jq-command-json)
- Use `jq` to create JSON: [https://spin.atomicobject.com/2021/06/08/jq-creating-updating-json/](https://spin.atomicobject.com/2021/06/08/jq-creating-updating-json/)

## Evaluation Criteria
Your submission will be evaluated based on:
- **Autograder**: Your code must pass the autograder [test script](./test/test.spec.ts).
- **Explainer Comments**: Include comments explaining each step of your code.
- **Code Quality**: Your code should be well-organized, commented, and adhere to best practices.

### Plagiarism Policy
Our plagiarism detection checker thoroughly identifies any instances of copying or cheating. Participants are required to publish their solutions in the designated repository, which is private and accessible only to the individual and the administrator. Solutions should not be shared publicly or with peers. In case of plagiarism, both parties involved will be directly disqualified to maintain fairness and integrity.

### AI Usage Disclaimer
You may use AI tools like ChatGPT to gather information and explore alternative approaches, but avoid relying solely on AI for complete solutions. Verify and validate any insights obtained and maintain a balance between AI assistance and independent problem-solving.

## Why These Restrictions?
These rules are designed to enhance your understanding of the technical aspects of Bitcoin. By completing this assignment, you gain practical experience with the technology that secures and maintains the trustlessness of Bitcoin. This challenge not only tests your ability to develop functional Bitcoin applications but also encourages deep engagement with the core elements of Bitcoin technology.