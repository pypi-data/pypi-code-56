import json
from pathlib import Path
from subprocess import getoutput
from IPython.display import HTML

_TEMPLATE = '''
<script src="//code.jquery.com/jquery-3.4.1.min.js"></script>
<link href="//cdn.jsdelivr.net/npm/jquery.fancytree@2.27/dist/skin-win8/ui.fancytree.min.css" rel="stylesheet">
<script src="//cdn.jsdelivr.net/npm/jquery.fancytree@2.27/dist/jquery.fancytree-all-deps.min.js"></script>
<div id='tree'></div>
<script>
$("#tree").fancytree({
  source: %s
})
</script>
'''

def fancytree(data):
    """ Display data with fancytree.

    Data should be in a correct format, i.e.
    data = [
        {"title": "Node 1", "key": "1"},
        {"title": "Folder 2", "key": "2", "folder": True, "children": [
            {"title": "Node 2.1", "key": "3"},
            {"title": "Node 2.2", "key": "4"}
        ]}
    ]
    """ 
    return HTML(_TEMPLATE % json.dumps(data))


def convert(node):
    """ Convert a compact format into fancytree data format """
    data = []
    for k, v in node.items():
        d = {'title': k}
        if v:
            d['folder'] = True
            d['children'] = convert(v)
            d['title'] = f"{k} ({len(d['children'])})"
        data.append(d)
    return data


def path_tree(path='.'):
    """ Given a path to a directory, display its tree """
    root = {}
    for p in Path(path).rglob('*'):
        node = root
        for part in p.parts:
            if part not in node:
                node[part] = {}
            node = node[part]
    data = convert(root)
    return fancytree(data)


def tar_tree(filename):
    """ Display contents inside a tar file using fancytree """
    root = {}
    lines = getoutput('tar -tzf '+filename).splitlines()
    for line in lines:
        if line.endswith('/'): continue
        node = root
        for part in line.split('/'):
            if part not in node:
                node[part] = {}
            node = node[part]
    data = convert(root)
    return fancytree(data)

