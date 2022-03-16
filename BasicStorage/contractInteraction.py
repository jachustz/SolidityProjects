from solcx import compile_standard, install_solc
import json
from web3 import Web3

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


w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xF2DCCED22EEb74b306D601e1479758Ac3066f8Ff"  # ganache public key
private_key = "0x293ee3baec1a5dabf689f6b4806bb92a447b291cb2af5ad03bc1b82123e26e61"  # ganache private key
nonce = w3.eth.getTransactionCount(my_address)

storageContract = w3.eth.contract(
    address="0x4279F4340825F29ECa26D19Bc63Bbb827951CB40", abi=abi
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
