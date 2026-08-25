import {readFileSync} from "fs";

describe('Evaluate submission', () => {
    let fundingTxid: string;
    let spendingTxid: string;

    const hexRegex = /^[0-9a-fA-F]{64}$/;

    const getRawTransaction = async (txid: string) => {
        const RPC_USER="alice";
        const RPC_PASSWORD="password";
        const RPC_HOST="http://127.0.0.1:18443";

        const response = await fetch(RPC_HOST, {
            method: 'post',
            body: JSON.stringify({
                jsonrpc: '1.0',
                id: 'curltest',
                method: 'getrawtransaction',
                params: [txid, true],
            }),
            headers: {
                'Content-Type': 'text/plain',
                'Authorization': 'Basic ' + Buffer.from(`${RPC_USER}:${RPC_PASSWORD}`).toString('base64'),
            }
        });

        const jsonResponse = await response.json();
        expect(jsonResponse?.result).toBeDefined();

        return jsonResponse.result;
    }

    it('should read data from output files and perform sanity checks', () => {
        const [fundingTxidFile, spendingTxidFile] = readFileSync('out.txt', 'utf-8').trim().split('\n');

        expect(fundingTxidFile).toBeDefined();
        expect(spendingTxidFile).toBeDefined();
        fundingTxid = fundingTxidFile.trim();
        spendingTxid = spendingTxidFile.trim();

        expect(fundingTxid).toMatch(hexRegex);
        expect(spendingTxid).toMatch(hexRegex);
    });


    it('should validate funding transaction', async () => {
        const tx = await getRawTransaction(fundingTxid);

        expect(tx.txid).toBe(fundingTxid);
        expect(tx.vin).toHaveLength(2);
        expect(tx.vout).toHaveLength(3);

        const multisigOutput = tx.vout.find((output: any) => output.value === 20);
        expect(multisigOutput).toBeDefined();
        expect(multisigOutput.scriptPubKey.type).toBe('witness_v0_scripthash');

        const changeOutputs = tx.vout.filter((output: any) => output.value !== 20);
        expect(changeOutputs).toHaveLength(2);
        expect(changeOutputs[0].value).toBe(changeOutputs[1].value);
    });

    it('should validate spending transaction', async () => {
        const tx = await getRawTransaction(spendingTxid);

        expect(tx.txid).toBe(spendingTxid);
        expect(tx.vin).toHaveLength(1);
        expect(tx.vout.length).toBeGreaterThanOrEqual(2);
        expect(tx.vout.length).toBeLessThanOrEqual(3);

        expect(tx.vin[0].txid).toBe(fundingTxid);
        expect(tx.vin[0].scriptSig.hex).toBe('');
        expect(tx.vin[0].scriptSig.asm).toBe('');
        expect(tx.vin[0].txinwitness).toHaveLength(4);
        expect(tx.vin[0].txinwitness[0]).toBe('');
        expect(tx.vin[0].txinwitness[1].startsWith('30440220')).toBe(true);
        expect(tx.vin[0].txinwitness[2].startsWith('30440220')).toBe(true);
        expect(tx.vin[0].txinwitness[3].startsWith('5221')).toBe(true);
        expect(tx.vin[0].txinwitness[1].endsWith('01')).toBe(true);
        expect(tx.vin[0].txinwitness[2].endsWith('01')).toBe(true);
        expect(tx.vin[0].txinwitness[3].endsWith('52ae')).toBe(true);
    });
});