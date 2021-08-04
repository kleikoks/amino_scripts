
from time import time
from pathlib import Path

def get_file_path(path, filename):
    items = path.split('/')
    items.pop()
    items.append(filename)
    file_path = '/'.join(filter(None, items))
    return file_path
