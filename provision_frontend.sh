echo "Installing nvm"  # See https://github.com/nvm-sh/nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.nvm/nvm.sh

echo "Installing Node"
nvm install node
nvm use node

echo "Installing necessary packages"
npm run provision --prefix ~/hknweb/hknweb/frontend
npm run $1 --prefix ~/hknweb/hknweb/frontend  # See hknweb/frontend/package.json
