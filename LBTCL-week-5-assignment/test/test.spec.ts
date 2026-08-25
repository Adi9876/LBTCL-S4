import {readFileSync} from "fs";

describe('Evaluate submission', () => {
    let txid: string;

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
        txid = readFileSync('out.txt', 'utf-8').trim();

        expect(txid).toBeDefined();
        expect(txid).toMatch(hexRegex);
    });


    it('should validate refund transaction', async () => {
        const tx = await getRawTransaction(txid);

        expect(tx.txid).toBe(txid);

        expect(tx.vin).toHaveLength(1);
        expect(tx.vin[0].sequence).toBe(10)

        expect(tx.vout.length).toBeGreaterThanOrEqual(1);
        const refundOutput = tx.vout.find((output: any) => output.value === 10);
        expect(refundOutput).toBeDefined();
    });
});