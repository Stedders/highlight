from app import load
import json

def test_load_ff():
    site = load.get_global()

    assert site == json.load(open('test_results/test_load_ff.json', 'r'))
