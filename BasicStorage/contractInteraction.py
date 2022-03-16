from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


# read/open contract code
with open("./BasicDataStorage.sol", "r") as file:
    contractCode = file.read()

# compile code
install_solc("0.6.0")
compiledCode = compile_standard(
    {
        "language": "Solidity",
        "sources": {"BasicDataStorage.sol": {"content": contractCode}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# save to JSON
with open("compiled_Code.json", "w") as file:
    json.dump(compiledCode, file)

# covert to bytecode
bytecode = compiledCode["contracts"]["BasicDataStorage.sol"]["BasicDataStorage"]["evm"][
    "bytecode"
]["object"]

# retrieve abi
abi = compiledCode["contracts"]["BasicDataStorage.sol"]["BasicDataStorage"]["abi"]


w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/68c0eea9aac94b61b9928ae4ad714add")
)
chain_id = 4  # Rinkeby/4
my_address = os.getenv("envWalletAddress")  # ganache public key
private_key = os.getenv("envPrivateKey")  # ganache private key
nonce = w3.eth.getTransactionCount(my_address)

storageContract = w3.eth.contract(
    address=w3.toChecksumAddress("0xe78a0f7e598cc8b0bb87894b0f60dd2a88d6a8ab"), abi=abi
)


print(storageContract.functions.retrieve().call())

storageTransaction = storageContract.functions.addTransmittal(
    "asdf", 6565, 6565
).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signedTransaction = w3.eth.account.sign_transaction(
    storageTransaction, private_key=private_key
)

sendTransaction = w3.eth.send_raw_transaction(signedTransaction.rawTransaction)
sendReceipt = w3.eth.wait_for_transaction_receipt(sendTransaction)
