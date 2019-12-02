"""
counts.py

This class counts words/scenes in a file
"""
import re

def word_count(path):
    rv = True
    reason = "OK"
    words = 0
    try:
        with open(path, "r") as f:
            words = len(re.findall(r'\w+', f.read()))
    except Exception as e:
        rv = False
        reason = str(e)

    return (rv, reason, words)

def scene_count(path):
    rv = True
    reason = "OK"
    scenes = 0
    try:
        with open(path, "r") as f:
            line = f.readline()
            while line:
                scenes += len(re.findall(r'^#', line))
                line = f.readline()
    except Exception as e:
        rv = False
        reason = str(e)

    return (rv, reason, scenes)
