import os
import re
from colorama import Fore, Style


def find_constructors(path):
    if os.path.isdir(path):
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        files = [os.path.join(path, f) for f in files if f.endswith(".sol")]
    else:
        files = [path]
    for file in files:
        with open(file) as f:
            contents = f.read()
            matches = re.findall(r"constructor\s*\((.*?)\)\s*\{(.*?)\}", contents, re.DOTALL)
            for match in matches:
                args, code = match
                print(Fore.GREEN + f"Constructor in {os.path.basename(file)}:" + Style.RESET_ALL)
                if "== address(0)" in code or "!= address(0)" in code:
                    print(Fore.RED + "Potential 0 address check exists" + Style.RESET_ALL)
                print(Fore.YELLOW + f"Arguments: {args.strip()}" + Style.RESET_ALL)
                print(Fore.BLUE + f"Code: {code.strip()}" + Style.RESET_ALL)
                print("=" * 30)


if __name__ == "__main__":
    path = input("Enter file path or folder: ")
    find_constructors(path)
