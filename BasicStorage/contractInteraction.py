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

storageContract = w3.eth.contract(
    address="0x3ae47ddc7c1b5583C7145208240b6686f7024aFE", abi=abi
)

print(storageContract.functions.retrieve().call())
