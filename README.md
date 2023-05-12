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
python3 solid-func_v1.0.py ~/path/to/solidity-file.sol
```

#### multiple file detection:
```
python3 solid-func_v1.0.py ~/path/to/folder/with/solidity-files/
```
