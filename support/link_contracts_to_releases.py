import base64
import hashlib
import json
import re
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import requests

"""
This scripts tries to match xExchange contracts (as found on Mainnet) with GitHub releases.

This is a support script. It's not meant to be used by community developers, 
but may serve as a starting point (example) to recover mappings between contracts and releases, if needed.
"""


def main():
    contracts_config_url = 'https://raw.githubusercontent.com/multiversx/mx-exchange-service/main/src/config/mainnet.json'
    github_repository = 'multiversx/mx-exchange-sc'
    contract_summary_file = Path('workspace/contracts-summary.json')
    downloaded_contracts_folder = Path('workspace/downloaded_contracts')
    downloaded_contracts_folder.mkdir(parents=True, exist_ok=True)

    # Download contracts summary, if not already downloaded.
    if not contract_summary_file.exists():
        contracts_config = download_file(contracts_config_url).decode()
        contracts_addresses: List[str] = re.findall(r'erd1[a-z0-9]{58}', contracts_config)
        contracts_summary = download_contracts_summary(contracts_addresses)

        with open(contract_summary_file, 'w') as f:
            json.dump(contracts_summary, f)

    # Now let's download GitHub assets (WASM files)
    github_releases = download_json(f'https://api.github.com/repos/{github_repository}/releases?per_page=100')
    files_to_download: List[Tuple[str, Path]] = []

    for release in github_releases:
        tag = release['tag_name']
        assets = release['assets']
        for asset in assets:
            name = asset['name']
            if name.endswith('.wasm'):
                url = asset['browser_download_url']
                asset_path = downloaded_contracts_folder / tag / name
                asset_path.parent.mkdir(parents=True, exist_ok=True)
                if not asset_path.exists():
                    files_to_download.append((url, asset_path))

    def download_asset(tuple: Tuple[str, Path]):
        url, asset_path = tuple
        print('downloading', url)
        data = download_file(url)
        asset_path.write_bytes(data)

    print("Will download", len(files_to_download), "files")
    ThreadPool(32).map(download_asset, files_to_download)

    # Now let's find a matching asset (among the downloaded ones) for each contract.
    contracts_summary = json.load(open(contract_summary_file))
    wasm_files = list(downloaded_contracts_folder.glob('**/*.wasm'))

    codehashes_by_file: Dict[str, str] = dict()
    for wasm_file in wasm_files:
        bytecode = wasm_file.read_bytes()
        blake2b = hashlib.blake2b(bytecode, digest_size=32)
        codehashes_by_file[str(wasm_file)] = blake2b.hexdigest()

    releases_to_consider: Set[str] = set()

    for item in contracts_summary:
        contract_name = item['name']
        contract_address = item['address']
        on_chain_codehash = item['codehash']
        found = False

        for wasm_file, codehash in codehashes_by_file.items():
            release_tag = Path(wasm_file).parent.name
            if on_chain_codehash == codehash:
                print(f'[OK ] {contract_name}: {contract_address} -> {release_tag}')
                releases_to_consider.add(release_tag)
                found = True
                break

        if not found:
            print(f'[NOK] {contract_name}: {contract_address} -> !!! NOT FOUND on GitHub !!!')

    print("Releases to consider:")
    for release_tag in sorted(list(releases_to_consider)):
        print(release_tag)


def download_contracts_summary(addresses: List[str]) -> List[Dict[str, Any]]:
    contracts_summary: List[Dict[str, Any]] = []

    def download_contract_summary(address: str):
        print("downloading data for", address, "...")

        url = f'https://api.multiversx.com/accounts/{address}'

        data = download_json(url)
        name = data.get("assets", dict()).get("name", "")
        codehash = data["codeHash"]
        codehash = base64.b64decode(codehash).hex()

        contracts_summary.append({
            "name": name,
            "address": address,
            "codehash": codehash,
        })

    ThreadPool(2).map(download_contract_summary, addresses)
    contracts_summary.sort(key=lambda x: x["name"])
    return contracts_summary


def download_file(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def download_json(url: str) -> Any:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    main()
