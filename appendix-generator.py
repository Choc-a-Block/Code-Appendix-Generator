import logging
import os
import argparse
import re

HEADER = '-' * 25 + 'Contents' + '-' * 25
FOOTER = '-' * 24 + '/Contents' + "-"*25
APDX = '.apdx'
CHUNK_SIZE = 1048576 # 1MB

def load_apdxignore():
    if os.path.exists(APDX):
        with open(APDX, 'r') as f:
            return f.read().splitlines()
    return []

def check_file(file_path, ignore_files, blacklist):
    if blacklist:
        return not any(re.search(ignore, file_path) for ignore in ignore_files)
    return any(re.search(ignore, file_path) for ignore in ignore_files)

def log_error(file_path, e):
    logging.error(f"Error decoding file: {file_path}: {e}")

def write_to_file(output_file, file, root, file_path):
    output_file.write(f"File: {file}\nDirectory: {root}\n{HEADER}\n")
    with open(file_path, 'r', encoding='utf-8') as f:
        if os.path.getsize(file_path) > CHUNK_SIZE: 
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                output_file.write(chunk)
        else:
            output_file.write(f.read())
    output_file.write(f"\n{FOOTER}\n\n")

def process_files(directory, ignore_files, output_file, blacklist):
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                if check_file(file_path, ignore_files, blacklist):
                    write_to_file(output_file, file, root, file_path)
            except (IOError, PermissionError) as e:
                log_error(file_path, e)
            except UnicodeDecodeError as e:
                logging.error(f"Error decoding file: {file_path}: {e}")
            except UnicodeEncodeError as e:
                logging.error(f"Error encoding file: {file_path}: {e}")

def main(blacklist=True, output_file_path="output.txt", directory=".", overwrite=True):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Parameters: apdx_operating_mode={'Blacklist' if blacklist else 'Whitelist'}, output_file_path={output_file_path}, directory={directory}, overwrite={overwrite}")
    if overwrite and os.path.exists(output_file_path):
        os.remove(output_file_path)
    ignore_files = load_apdxignore() if os.path.exists(APDX) else []
    with open(output_file_path, 'a') as output_file:
        process_files(directory, ignore_files, output_file, blacklist)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an appendix.')
    parser.add_argument('--blacklist', dest='apdx_blacklist', action='store_true', help='Use .apdx as a blacklist')
    parser.add_argument('--whitelist', dest='apdx_whitelist', action='store_true', help='Use .apdx as a whitelist')
    parser.add_argument('--output', dest='output_file_path', default='output.txt', help='Output file path')
    parser.add_argument('--dir', dest='directory', default='.', help='Directory to process')
    parser.add_argument('--no-overwrite', dest='overwrite', action='store_false', help='Do not overwrite existing output file')
    args = parser.parse_args()
    blacklist = args.apdx_blacklist
    whitelist = args.apdx_whitelist
    args.apdx_blacklist = blacklist or not whitelist
    main(args.apdx_blacklist, args.output_file_path, args.directory, args.overwrite)
