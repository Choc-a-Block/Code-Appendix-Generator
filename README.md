# Code-Appendix-Generator

A simple tool to generate a code appendix for a programming project. Run the script in the root directory of your project and it will generate a text file with a list of all files, their contents, and their directory structure.

---

## Usage

```bash
python3 generate_code_appendix.py [--whitelist or --blacklist] [--output] [--dir] [--no-overwrite]
```

### Appendix Files
The `.apdx` file is a file that you can choose to add to your project. The purpose of this is to stipulate to the appendix generator either which files to include or which to exclude from the appendix. Each line in the file should be a regular expression that will be matched against the file path. If the file path matches any of the regular expressions in the `.apdx` file, the file will be included in the appendix.


- `--whitelist`: Use the `.apdx` file to specify exactly which files to **include**. (Optional)
- `--blacklist`: Use the `.apdx` file to specify exactly which files to **exclude**. (Optional)
(The default behaviour is to use the .apdx file as an ignore list, similar to `.gitignore`)
- `--output`: Output file path. Default is `output.txt`. (Optional)
- `--dir`: Directory to process. De`ault is the current directory. (Optional)
- `--no-overwrite`: Do not overwrite existing output file. (Optional)

## Example usage:

> I want to generate an appendix for my project in the directory `/path/to/project` and I want to include only the files that match the regular expressions in my `.apdx`. I want the output to be written to `my_appendix.txt`.
```bash
python3 generate_code_appendix.py --whitelist --output my_appendix.txt --dir /path/to/project
```

