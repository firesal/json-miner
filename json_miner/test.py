from .miner import JsonMiner
from os.path import abspath
with open(abspath('json_miner/test.html'), 'r') as file:
    m_text = file.read()
    # pairs = JsonMiner(m_text).get_pairs()
    for text in JsonMiner(m_text).get_blocks():
        print(text)
