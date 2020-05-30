def nodeChildren(node):
    return [child for child in node.children if not isinstance(child, str)]

def firstChild(node):
    children = nodeChildren(node)

    if len(children) == 1:
        return children[0]
    else:
        raise ValueError("Error - can only have one child")