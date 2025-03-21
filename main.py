import time
import requests as req
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from rich.console import Console
from rich.progress import Progress

console = Console()

def read_file(path: Path) -> list:
    """Reads a file and returns a list of non-empty lines."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
        return lines
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        raise

def write_file(file_name: str, content: list) -> None:
    """Writes a list of lines to a file."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.writelines(content)
    except Exception as e:
        console.print(f"[red]Error writing file {file_name}: {e}[/red]")
        raise

def crack_hash(hash_value: str) -> (str, str):
    """
    Tries to crack the given MD5 hash using nitrxgen.net database.
    Returns a tuple of (hash, password) if found, otherwise (hash, None).
    """
    url = "https://www.nitrxgen.net/md5db/"
    full_url = url + hash_value
    retries = 5
    for i in range(retries):
        try:
            response = req.get(full_url)
            if response.ok:
                if response.text.strip():
                    return hash_value, response.text.strip()
                return hash_value, None
        except req.RequestException as e:
            console.print(f"[red]Error: {e}, retrying ({i+1}/{retries})...[/red]")
            time.sleep(2)
    return hash_value, None

def crack_single_hash(hash_input: str):
    """Crack a single hash and display the result."""
    console.print(f"[yellow]Cracking...[/yellow]")
    hash_input = hash_input.strip()
    hash_val, password = crack_hash(hash_input)
    if password:
        console.print(f"\n[yellow]Hash {hash_val} cracked:[/yellow] [bold green]{password}[/bold green]")
    else:
        console.print(f"\n[bold red]No password found for hash {hash_val}[/bold red]")

def crack_hashes_from_file(file_path_str: str, output_file: str, no_crack_file: str):
    """Crack hashes from a file and write the results to user-defined output files."""
    file_path = Path(file_path_str)
    try:
        hashes = read_file(file_path)
    except Exception:
        console.print("[red]Exiting due to file read error.[/red]")
        return

    cracked_list = []
    uncracked_list = []
    cracked_lock = Lock()
    uncracked_lock = Lock()

    with Progress() as progress:
        task = progress.add_task("[green]Cracking hashes...", total=len(hashes))
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(crack_hash, hash_val): hash_val for hash_val in hashes}
            for future in as_completed(futures):
                original_hash = futures[future]
                try:
                    hash_val, password = future.result()
                    if password:
                        with cracked_lock:
                            cracked_list.append(f"{hash_val}:{password}\n")
                    else:
                        with uncracked_lock:
                            uncracked_list.append(f"{hash_val}\n")
                except Exception as exc:
                    console.print(f"[red]{original_hash} generated an exception: {exc}[/red]")
                progress.update(task, advance=1)

    try:
        write_file(output_file, cracked_list)
        write_file(no_crack_file, uncracked_list)
    except Exception:
        console.print("[red]Error occurred while writing output files.[/red]")
        return
    console.print("[green]Hash cracking complete.[/green]")
    console.print(f"[green]Cracked hashes written to:[/green] {output_file}")
    console.print(f"[green]Uncracked hashes written to:[/green] {no_crack_file}")

def main():
    parser = argparse.ArgumentParser(
        description="CLI MD5 Hash Cracking Tool using nitrxgen.net API"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--hash",
        type=str,
        help="MD5 hash to crack",
    )
    group.add_argument(
        "--list",
        type=str,
        help="Path to the file containing MD5 hashes (one per line)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="cracked.txt",
        help="Output file name for cracked hashes (default: cracked.txt)",
    )
    parser.add_argument(
        "--no-crack",
        type=str,
        default="no-crack.txt",
        help="Output file name for uncracked hashes (default: no-crack.txt)",
    )
    args = parser.parse_args()

    if args.hash:
        crack_single_hash(args.hash)
    elif args.list:
        crack_hashes_from_file(args.list, args.output, args.no_crack)

if __name__ == "__main__":
    main()
