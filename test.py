import requests
from ape_hardhat import Contract, Network
from flask import Flask, render_template, request

abi = []
contract = Contract.from_abi('MyContract', abi, address)

network = Network({
    'name': 'hardhat',
    'chainId': 31337,
    'url': 'http://localhost:8545'
})

app = Flask(__name__, template_folder='pages')

@app.route('/')
def index():
    amount_raised = contract.functions.amountRaised().call()
    return render_template('index.html', amount_raised=amount_raised)

@app.route('/my-contract')
def my_contract_route():
    result = contract.functions.myFunction().call()
    return f"The result is {result}"

@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    if request.method == 'POST':
        address = request.form['address']
        amount = int(request.form['amount'])
        
        sender_private_key = b'...'  # Your private key goes here
        nonce = web3.eth.getTransactionCount(address)

        tx = contract.functions.contribute().buildTransaction({
            'from': address,
            'value': amount,
            'nonce': nonce,
            'gasPrice': web3.toWei('5', 'gwei')
        })

        signed_tx = web3.eth.account.signTransaction(tx, sender_private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return f'Transaction sent: {to_checksum_address(tx_hash)}'

    return render_template('contribute.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
