import {readFileSync} from "fs";

type Transaction = {
    txid: string,
    input: {
        txid: string,
        vout: number
    }[],
    output: {
        scriptpubkey: string,
        amount: number
    }[],
    fee: number,
    weight: number,
}

describe('Evaluate submission', () => {
    let parentTx: Transaction;
    let childTx: Transaction;
    let parentRbfTx: Transaction;

    const sanityCheckOutput = (tx: Transaction, inputLen: number, outputLen: number) => {
        expect(tx).toBeDefined();
        expect(tx.txid).toBeDefined();
        expect(tx.txid.length).toBe(64);
        expect(tx.input).toBeDefined();
        expect(tx.input.length).toBe(inputLen);
        tx.input.forEach(i => {
            expect(i.txid).toBeDefined();
            expect(i.txid.length).toBe(64);
            expect(i.vout).toBeDefined();
            expect(i.vout).toBeGreaterThanOrEqual(0);
        });
        expect(tx.output).toBeDefined();
        expect(tx.output.length).toBe(outputLen);
        tx.output.forEach(o => {
            expect(o.scriptpubkey).toBeDefined();
            expect(o.amount).toBeDefined();
            expect(o.amount).toBeGreaterThan(0);
        });
        expect(tx.fee).toBeDefined();
        expect(tx.fee).toBeGreaterThan(0);
        expect(tx.weight).toBeDefined();
        expect(tx.weight).toBeGreaterThan(0);
    }

    it('should read data from output files and perform sanity checks', () => {
        parentTx = JSON.parse(readFileSync('parent.json', 'utf8'));
        sanityCheckOutput(parentTx, 2, 2);
        childTx = JSON.parse(readFileSync('child.json', 'utf8'));
        sanityCheckOutput(childTx, 1, 1);
        parentRbfTx = JSON.parse(readFileSync('parent-rbf.json', 'utf8'));
        sanityCheckOutput(parentRbfTx, 2, 2);
    });

    it('should validate parent', () => {
        expect(parentTx.output.find(o => o.amount === 70)).toBeDefined()
        expect(parentTx.output.find(o => o.amount === 29.99999)).toBeDefined()
        expect(parentTx.fee).toBe(0.00001)
    });

    it('should validate child', () => {
        expect(childTx.output.find(o => o.amount === 29.99998)).toBeDefined()
        expect(childTx.fee).toBe(0.00001)
        expect(childTx.input[0].txid).toBe(parentTx.txid)
        expect(childTx.input[0].vout).toBeLessThanOrEqual(1)
    });

    it('should validate parent RBF', () => {
        for (const output of parentRbfTx.output) {
            if (output.amount === 70) expect(output.scriptpubkey).toBe(parentTx.output.find(o => o.amount === 70).scriptpubkey);
            else expect(output.amount).toBeLessThan(29.99999);
        }
        expect(parentRbfTx.input).toStrictEqual(parentTx.input);
        expect(parentRbfTx.fee).toBeGreaterThanOrEqual(0.00011);
    });


    it('should have evicted parent', async () => {
        const RPC_USER="alice";
        const RPC_PASSWORD="password";
        const RPC_HOST="http://127.0.0.1:18443";

        const response = await fetch(RPC_HOST, {
            method: 'post',
            body: JSON.stringify({
                jsonrpc: '1.0',
                id: 'curltest',
                method: 'getmempoolentry',
                params: [parentTx.txid]
            }),
            headers: {
                'Content-Type': 'text/plain',
                'Authorization': 'Basic ' + Buffer.from(`${RPC_USER}:${RPC_PASSWORD}`).toString('base64'),
            }
        });

        const jsonResponse = await response.json();
        expect(jsonResponse).toBeDefined();
        expect(jsonResponse.result).toBeNull();
        expect(jsonResponse.error?.message).toBe("Transaction not in mempool");
    });

    it('should have evicted child', async () => {
        const RPC_USER="alice";
        const RPC_PASSWORD="password";
        const RPC_HOST="http://127.0.0.1:18443";

        const response = await fetch(RPC_HOST, {
            method: 'post',
            body: JSON.stringify({
                jsonrpc: '1.0',
                id: 'curltest',
                method: 'getmempoolentry',
                params: [childTx.txid]
            }),
            headers: {
                'Content-Type': 'text/plain',
                'Authorization': 'Basic ' + Buffer.from(`${RPC_USER}:${RPC_PASSWORD}`).toString('base64'),
            }
        });

        const jsonResponse = await response.json();
        expect(jsonResponse).toBeDefined();
        expect(jsonResponse.result).toBeNull();
        expect(jsonResponse.error?.message).toBe("Transaction not in mempool");
    });
});