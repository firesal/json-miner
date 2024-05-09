# json-miner
Package used to extract json data from text content.

### Installation

You can clone the package and install using the following command

```
pip install -e json-miner
```

It uses `pyproject.toml` file to install directly to the `venv`.

Or directly from git using.

```bash
pip install git+https://github.com/firesal/json-miner
```



### Usage

```python
from json_miner import JsonMiner
# Needs text_to_be_mined as text that needs json extraction
for text in JsonMiner(text_to_be_mined).get_blocks():
    print(text) # Prints each JSON block found in text
```

`text_to_be_mined` should contain the text that needs json extraction. The above code prints all json from `text_to_be_mined`

### Testing Package

To test package with the test file with html in json in it, you can use

`python3 -m json_miner.test`

This loads html from miner folder which is test.html
