# Python-tools
A place for all my tools created using Python.

# solid-func
A Python script used to detect functions in solidity files, one or many. After detecting the existing functions the results are output to the cli

- v1.0: outputs the function information in one line with colour-coded outputs for each section detected
- v1.1: outputs the function information in a table format with colour-coded outputs for each section detected

#### Example Output:
```
For v1.0:
Function Name: claimRewards, Visibility: external, Modifiers: none, File Name: RewardsManager.sol

For v.1.1:
╒═════════════════════╤══════════════╤══════════════╤════════════════════╕
│ Function Name       │ Visibility   │ Modifiers    │ File Name          │
╞═════════════════════╪══════════════╪══════════════╪════════════════════╡
│ moveStakedLiquidity │ external     │ nonReentrant │ RewardsManager.sol │
╘═════════════════════╧══════════════╧══════════════╧════════════════════╛
```

## Prerequisites:
It's recommended to use a virtual environment as not to cause clashes with other tools you've installed or created. Use the following to create your own with Python venv (if installed)
```
python -m venv VIRTUALENVNAME
```
Then start the virtual environment from your cli
```
source VIRTUALENVNAME/bin/activate
```
You can stop the virtual environment with the following command in your cli
```
deactivate
```

Use the "requirements" file to install all dependencies for this tool
```
python3 install -r requirements.txt
```

## Commands:
#### single file detection:
```
python3 solid-func_v1.0.py /path/to/solidity-file.sol
```

#### multiple file detection:
```
python3 solid-func_v1.0.py /path/to/folder/with/solidity-files/
```

# solid-construct
Python script that searches for constructor functions in solidity files and prints information about the constructors found, including the filename, arguments, and code. It also checks if the code contains a potential 0 address check and prints a warning if it does. 

Output in different colors to differentiate the different elements identified from the constructor

#### Example Output:
```
For a single file:

Constructor in RewardsManager.sol:
Potential 0 address check exists
Arguments: address Token_, IPositionManager positionManager_
Code: if (Token_ == address(0)) revert DeployWithZeroAddress();

        Token = Token_;
        positionManager = positionManager_;
==============================

For multiple files:

Constructor in ERC20PoolFactory.sol:
Potential 0 address check exists
Arguments: address token_
Code: if (token_ == address(0)) revert DeployWithZeroAddress();

        token = token_;

        implementation = new ERC20Pool();
==============================
Constructor in PositionManager.sol:
Arguments: ERC20PoolFactory erc20Factory_,
        ERC721PoolFactory erc721Factory_
    ) PermitERC721("Ajna Positions NFT-V1", "TOKN-V1-POS", "1"
Code: erc20PoolFactory = erc20Factory_;
        erc721PoolFactory = erc721Factory_;
==============================
```

## Prerequisites:
It's recommended to use a virtual environment as not to cause clashes with other tools you've installed or created. Use the following to create your own with Python venv (if installed)
```
python -m venv VIRTUALENVNAME
```
Then start the virtual environment from your cli
```
source VIRTUALENVNAME/bin/activate
```
You can stop the virtual environment with the following command in your cli
```
deactivate
```

Use the "requirements" file to install all dependencies for this tool
```
python3 install -r requirements.txt
```

## Commands:
#### single file detection:
```
python3 solid-construct_v1.0.py
```
then when prompted enter:
```
/path/to/solidity-file.sol
```

#### multiple file detection:
```
python3 solid-construct_v1.0.py
```
then when prompted enter:
```
/path/to/folder/with/solidity-files/
```
