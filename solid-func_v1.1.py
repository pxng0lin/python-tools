import os
import re
import time
import subprocess
import click
import multiprocessing
import itertools
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import asyncio
from tabulate import tabulate



# Install required dependencies
def install_dependencies():
    subprocess.run(['pip3', 'install', '--no-cache-dir', '--no-warn-script-location', '-r', 'requirements.txt'], check=True)


# Check if required dependencies are installed, and install them if any are missing
def check_dependencies():
    missing_deps = []
    try:
        import solcx  # Check if solcx is already installed
    except ImportError:
        missing_deps.append('solcx')
    try:
        import click  # Check if click is already installed
    except ImportError:
        missing_deps.append('click')
    if missing_deps:
        # If any required dependency is missing, install all missing dependencies
        click.echo(f"Missing dependencies: {missing_deps}. Installing...")
        install_dependencies()

def detect_functions(file_path):
    # Check if file exists and is a Solidity file
    if not os.path.isfile(file_path):
        raise ValueError("Invalid input file")

    if not file_path.endswith(".sol"):
        raise ValueError("Input file is not a Solidity file")

    with open(file_path, "r") as f:
        file_content = f.read()

    function_regex = re.compile(r"(function\s+(\w+)\s*\()")

    matches = []

    for match in function_regex.finditer(file_content):
        function_name = match.group(2)
        function_declaration = match.group(0) + file_content[match.end():]

        # Check if the function declaration has a return statement
        returns_regex = re.compile(r"\breturns\s+(.+)\b")
        returns_match = returns_regex.search(function_declaration)

        if returns_match:
            # If it does, extract the return type and remove it from the function declaration
            return_type = returns_match.group(1)
            function_declaration = function_declaration.replace(f"returns {return_type}", "")

        visibility_regex = re.compile(r"\b(public|external|internal|private|payable|view|pure)\b")
        visibility_match = visibility_regex.search(function_declaration)

        visibility = ''
        modifiers = []

        if visibility_match:
            visibility = visibility_match.group(1) + ' '
            modifiers_regex = re.compile(r"(?<!view)(?<!pure)(?<!virtual)(?<!override)(?<!returns)\b\w+\b")
            body_start_match = re.search(r"{", function_declaration)
            if body_start_match:
                body_start_index = body_start_match.start()
                modifiers_match = modifiers_regex.findall(function_declaration[visibility_match.end():body_start_index])
                modifiers = [modifier for modifier in modifiers_match if modifier not in ['override','virtual','view','pure','returns']]

        matches.append({
            "name": function_name,
            "visibility": visibility,
            "modifiers": modifiers,
            "file_path": file_path
        })

    return matches


# Detect functions in all Solidity files in a folder (and its subfolders)
import concurrent.futures

def detect_functions_for_folder(folder_path):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files = []
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.endswith('.sol'):
                    files.append(os.path.join(dirpath, filename))

        function_lists = executor.map(detect_functions, files)
        functions = list(itertools.chain.from_iterable(function_lists))

    return functions

# Print the details of a function (TABULAR)
async def print_function_details(func): 
    # Extract the function name, visibility, modifiers, and file name from the input argument
    name = func['name']
    visibility = func['visibility'].strip()
    modifiers = ' '.join(func['modifiers'])
    file_name = os.path.basename(func['file_path'])

    # Ignore function declarations that contain the word "returns"
    if 'returns' in modifiers:
        return

    # Map visibility values to their corresponding colors
    visibility_colors = {
        'public': 'blue',
        'external': 'red',
        'internal': 'green'
    }

    # Colorize the visibility text if necessary
    if visibility in visibility_colors:
        visibility = click.style(visibility, fg=visibility_colors[visibility])

    # Colorize the modifiers text if necessary
    if modifiers:
        modifiers = click.style(modifiers, fg='cyan')
    else:
        modifiers = 'none'

    # Append the function details to a list
    function_details = [name, visibility, modifiers, file_name]

    # Print the function details in a table format
    headers = ["Function Name", "Visibility", "Modifiers", "File Name"]
    table = [function_details]
    click.echo(tabulate(table, headers=headers, tablefmt="fancy_grid"))

@click.command()
@click.argument("folder_path", type=click.Path(exists=True))
def main(folder_path):
    """
    Displays all functions present in Solidity files in a folder.

    Args:
        folder_path (str): Path to the folder containing the Solidity files, or a path to a single Solidity file.
    """
    check_dependencies()

    start_time = time.time()

    if os.path.isfile(folder_path):
        # If the input path points to a file, detect functions in that file only
        functions = detect_functions(folder_path)
    elif os.path.isdir(folder_path):
        # If the input path points to a folder, detect functions in all Solidity files in that folder and its subfolders
        functions = detect_functions_for_folder(folder_path)
    else:
        raise ValueError("Invalid input path.")

    # Use asyncio to print the function details in parallel
    async def print_all_functions():
        loop = asyncio.get_running_loop()
        tasks = [loop.create_task(print_function_details(function)) for function in functions]
        await asyncio.gather(*tasks)

    asyncio.run(print_all_functions())

    elapsed_time = time.time() - start_time
    click.echo(f"Elapsed time: {elapsed_time:.3f} seconds.")


if __name__ == "__main__":
    main()

