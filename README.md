# Minimal harvester for Project Guthenberg

This small script comes handy to download books from [Project Guthenberg](https://www.gutenberg.org). There are not many options for now, it may change in the future.

## Installation

* Clone the repository into a new local directory,
* (Optional) Create a virtual environment in the same directory and activate it,
* Install the packages from `requirements.txt`.

## Usage

There are three arguments:

* `-t` or `--filetype` for the output type you want,
* `-l` or `--language` for the output language you want,
* `-m` or `--max` for the maximum number of documents you want.

The script will create an output folder `./data/language/` in the root directory and store the output in multiple `.zip` files.

More [info](https://www.gutenberg.org/policy/robot_access.html) on the harvester.

## Example

Here is an example for querying at most 10 (`-m 10`) documents in English (`-l en`) with `.txt` format (`-t txt`).

```bash
python3 main.py -t txt -l en -m 10
```