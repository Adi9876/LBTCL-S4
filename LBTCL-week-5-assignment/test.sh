# Setup nvm and install pre-req
if command -v node > /dev/null 2>&1; then
  echo "Node.js is already installed. Current version: $(node -v)"
else
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
  source $HOME/.nvm/nvm.sh
  nvm install --lts
fi

if ! grep -q "# /bin/bash ./rust/run-rust.sh" run.sh; then
  if command -v cargo > /dev/null 2>&1; then
    echo "Cargo is already installed. Current version: $(cargo --version)"
  else
    curl https://sh.rustup.rs -sSf | sh -s -- -y
    source $HOME/.cargo/env
  fi
else
  echo "No specific language setup required."
fi

npm install # Install Node.js dependencies

set -e  # Exit immediately if any command fails

# Start the setup script and give access to all runners
chmod +x setup-bitcoin-node.sh
/bin/bash setup-bitcoin-node.sh

chmod +x ./bash/run-bash.sh
chmod +x ./python/run-python.sh
chmod +x ./javascript/run-javascript.sh
chmod +x ./rust/run-rust.sh
chmod +x ./run.sh

# Run the test scripts
/bin/bash run.sh
npm run test

# Stop the bitcoind
if pgrep -x "bitcoind" > /dev/null; then
  echo "Stopping bitcoind..."
  pkill -x "bitcoind"
  echo "bitcoind stopped."
else
  echo "bitcoind is not running."
fi