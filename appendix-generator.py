import os
import re

def load_apdxignore():
    ignore_files = []
    with open(".apdxignore", 'r', encoding='utf-8') as f:
        for line in f:
            ignore_files.append(line.strip())
    return ignore_files


def check_file(file_path: str, ignore_files: list) -> bool:
    if ignore_files:
        for ignore in ignore_files:
            if re.match(ignore, file_path):
                return False
    return True
            

def main(use_apdxignore=True, output_file_path="output.txt", directory=".", overwrite=True):
    if overwrite and os.path.exists(output_file_path):
        os.remove(output_file_path)
    if use_apdxignore:
        if not os.path.exists(".apdxignore"):
            print("No .apdxignore file found, using default behavior.")
            ignore_files = []
        else:
            print("Using .apdxignore file.")
            ignore_files = load_apdxignore()
    with open(output_file_path, 'a') as output_file:
        for root, dirs, files in os.walk(directory):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    if check_file(file_path, ignore_files):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            output_file.write(f"File: {file}\nDirectory: {root}\n{'-' * 25 + 'Contents' + '-' * 25}\n{f.read()}\n{'-' * 24 + '/Contents' + "-"*25}\n\n")
                except Exception as e:
                    print(f"Error decoding file: {file_path}: {e}")

if __name__ == "__main__":
    main()
