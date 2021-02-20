"""Tests relating to the load module"""
import json

from app import load


def test_load_ff():
    site = load.get_global()
    assert site == json.load(open('tests/test_results/test_load_ff.json', 'r'))


def test_load_tf():
    site = load.get_global(True, False)
    assert site == json.load(open('tests/test_results/test_load_tf.json', 'r'))


def test_load_ft():
    site = load.get_global(False, True)
    assert site == json.load(open('tests/test_results/test_load_ft.json', 'r'))


def test_load_tt():
    site = load.get_global(True, True)
    assert site == json.load(open('tests/test_results/test_load_tt.json', 'r'))
