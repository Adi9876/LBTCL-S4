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

        expect(tx.vout.length).toBeGreaterThanOrEqual(1);
        const salaryOutput = tx.vout.find((output: any) => output.value === 40);
        expect(salaryOutput).toBeDefined();
        expect(tx.locktime).toBe(500);
    });

    it('should validate spending transaction', async () => {
        const tx = await getRawTransaction(spendingTxid);

        expect(tx.txid).toBe(spendingTxid);
        expect(tx.vin).toHaveLength(1);
        expect(tx.vin[0].txid).toBe(fundingTxid);

        const dataOutput = tx.vout.find((output: any) => output.scriptPubKey.type === 'nulldata');
        expect(dataOutput).toBeDefined();
        expect(dataOutput.scriptPubKey.hex).toBe('6a1a4920676f74206d792073616c6172792c204920616d2072696368');
    });
});