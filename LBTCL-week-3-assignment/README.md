# Learning Bitcoin from the Command Line - Week 3: Multisig and PSBT

## Overview

In this third week you will:

1. **Create** three wallets (`Miner`, `Alice`, and `Bob`) and fund them on `regtest`.
2. **Build** a 2-of-2 P2WSH multisig address from `Alice` and `Bob`’s public keys.
3. **Craft & broadcast** a *funding* PSBT that funds the multisig with 20 BTC (10 BTC from each party).
4. **Mine** blocks to confirm funding and **report** balances.
5. **Craft** a *spending* PSBT that spends the multisig UTXO, splitting 10 BTC back to each party (minus fees).
6. **Sign** the PSBT in turn with `Alice` and `Bob`, **extract** the final transaction, and **broadcast** it.
7. **Mine** blocks to confirm spending and **report** final balances.
8. **Target Locations** for the solution code for each languages are given below:
   1. Bash: [solution.sh](./bash/solution.sh)
   2. Javascript: [index.js](./javascript/index.js)
   3. Python: [main.py](./python/main.py)
   4. Rust: [main.rs](./rust/src/main.rs)

## Problem Statement

Multisig transactions enable joint control of Bitcoin funds—crucial for co-custody and Layer 2 protocols (e.g., Lightning channels). In this exercise, simulate a simple 2-of-2 multisig share transfer between two participants, Alice and Bob:

1. **Funding phase:** both deposit coins into a 2-of-2 P2WSH address.
2. **Spending phase:** both sign to split funds back.

## Solution Requirements

Implement the following tasks in exactly one of the language-specific directories (`bash`, `javascript`, `python`, or `rust`):

### Setup Multisig & Funding

1. **Create wallets**: `Miner`, `Alice`, `Bob`.
2. **Fund wallets**: generate blocks to credit `Miner` (≥ 150 BTC), then send 15 BTC each to `Alice` and `Bob`.
3. **Construct multisig**: fetch `Alice` and `Bob`’s public keys; create a 2-of-2 P2WSH address.
4. **Build funding PSBT**: to fund the multisig address with 20 BTC, taking 10 BTC each from `Alice` and `Bob`, and providing correct change back to each of them.
5. **Sign & broadcast** the funding PSBT.
6. **Mine** 6 blocks to confirm.
7. **Print balances** of `Alice` and `Bob`.

### Settle Multisig & Spending

1. **Build spending PSBT** to spend funds from the multisig, ensuring 10 BTC is equally distributed back between `Alice` and `Bob` after accounting for fees.
2. **Sign PSBT** with `Alice`.
3. **Sign PSBT** with `Bob`.
4. **Extract & broadcast** the fully signed transaction.
5. **Mine** 6 blocks to confirm.
6. **Print final balances** of `Alice` and `Bob`.


### Output Format

Write the two resulting txids to a file named `out.txt`, one per line:

```txt
<txid_multisig_funding>
<txid_multisig_spending>
```

## Submission

- Write your solution in `solution.sh`. Make sure to include comments explaining each step of your code.
- Commit your changes and push to the main branch:
    - Add your changes by running `git add solution.sh`.
    - Commit the changes by running `git commit -m "Solution"`.
    - Push the changes by running `git push origin main`.
- The autograder will run your script against a test script to verify the functionality.
- Check the status of the autograder on the Github Classroom portal to see if it passed successfully or failed. Once you pass the autograder with a score of 100, you have successfully completed the challenge.
- You can submit multiple times before the deadline. The last submission before the deadline will be considered your final submission.
- You will lose access to the repository after the deadline.

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