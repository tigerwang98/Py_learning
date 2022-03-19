from os.path import realpath, dirname, join
import json

def get_config(name):
    path = join(dirname(realpath(__file__)), 'configs', '%s.json' % name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())