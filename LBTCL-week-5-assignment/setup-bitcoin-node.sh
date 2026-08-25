echo "Checking if Bitcoin Core is installed .... "
if ! command -v bitcoind > /dev/null 2>&1 || ! command -v bitcoin-cli > /dev/null 2>&1; then
    echo "Bitcoin Core not found. Installing Bitcoin Core .... "
    mkdir -p install
    cd install
    wget https://bitcoincore.org/bin/bitcoin-core-27.1/bitcoin-27.1-x86_64-linux-gnu.tar.gz > /dev/null 2>&1
    tar --extract -f bitcoin-27.1-x86_64-linux-gnu.tar.gz
    cp -r bitcoin-27.1/bin/* /usr/local/bin/
    mkdir -p ~/.bitcoin
    cd ..
else
    echo "Bitcoin Core is already installed."
fi
BITCOIN_CONF=~/.bitcoin/bitcoin.conf

if [ ! -f "$BITCOIN_CONF" ]; then
    echo "bitcoin.conf not found. Creating bitcoin.conf .... "
    touch "$BITCOIN_CONF"
fi
CONFIG_LINES="regtest=1
fallbackfee=0.0001
server=1
rest=1
txindex=1
rpcauth=alice:88cae77e34048eff8b9f0be35527dd91\$d5c4e7ff4dfe771808e9c00a1393b90d498f54dcab0ee74a2d77bd01230cd4cc"

if ! grep -Fxq "regtest=1" "$BITCOIN_CONF"; then
    echo "$CONFIG_LINES" >> "$BITCOIN_CONF"
    echo "Configuration added to bitcoin.conf"
else
    echo "Configuration already exists in bitcoin.conf"
fi
cd ..
bitcoind -daemon
sleep 5