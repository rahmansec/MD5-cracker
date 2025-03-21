
# MD5 Hash Cracker

A command-line tool to crack MD5 hashes using the [nitrxgen API](https://www.nitrxgen.net/md5db/). This project lets you either crack a single hash or a batch of hashes from a file, with support for custom output file names for both cracked and uncracked hashes.

## Features

- **Single Hash Cracking:** Provide a single MD5 hash from the CLI.
- **Batch Hash Cracking:** Read multiple MD5 hashes from a file (one per line) and process them concurrently.
- **Customizable Output Files:** Specify the names for the output files that will store cracked and uncracked hashes.
- **Multi-threaded Processing:** Uses Python’s `ThreadPoolExecutor` for concurrent requests.
- **Progress Visualization:** Displays real-time progress using the Rich library’s progress bar.
- **Easy CLI:** Uses the built-in `argparse` module for parsing command-line arguments.

## Requirements

- Python 3.7 or higher
- [Requests](https://pypi.org/project/requests/)
- [Rich](https://pypi.org/project/rich/)

Install the dependencies with pip:

```bash
pip install requests rich
```

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Ensure you have installed the required Python packages as mentioned above.

## Usage

This tool can be used via the command-line. You have two modes of operation: single hash mode and batch mode.

### Single Hash Mode

To crack a single MD5 hash, run:

```bash
py main.py --hash d6a6bc0db10694a2d90e3a69648f3a03
```

### Batch Mode

To crack hashes from a file and to specify custom names for the output files, run:

```bash
py main.py --list path.txt --output my_cracked.txt --no-crack my_not_cracked.txt
```

If no output file names are provided, the defaults are:
- Cracked hashes: `cracked.txt`
- Uncracked hashes: `no-crack.txt`

### Command-Line Arguments

- `--hash`: A single MD5 hash to crack.
- `--list`: The path to a file containing MD5 hashes (one per line).
- `--output`: *(Optional)* The output file name for storing cracked hashes. Default is `cracked.txt`.
- `--no-crack`: *(Optional)* The output file name for storing uncracked hashes. Default is `no-crack.txt`.

_Note: Only one of `--hash` or `--list` can be used at a time._