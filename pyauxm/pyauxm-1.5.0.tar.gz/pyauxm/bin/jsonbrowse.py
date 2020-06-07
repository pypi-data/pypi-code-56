#!/usr/bin/env python3
"""
TUI for browsing JSONable structures.
"""

import sys
import json

import urwid


SAMPLE_DATA = {
    "this_is_some_jsonbrowse_sample_data": True,
    "b": [
        2,
        {"c": 3},
        {"d" * 250: "e" * 2000},
    ],
    "f": ["g", 12] * 150,
    "h": 123456789.987654321,
}


class TreeMaker:
    """
    Configurable class to convert
    jsonable structures into tree display definitions
    """

    # This would work better
    # if 'selectable' and 'expandable'
    # were separate states.
    selectable_scalars = False

    def dumps(self, value):
        return json.dumps(
            value,
            ensure_ascii=False)

    def scalar_name(self, data, context=None):
        return [self.dumps(data)]

    def handle_scalar(self, data):
        result = dict(
            name=self.scalar_name(data),
        )
        if self.selectable_scalars:
            result['children'] = []
        return result

    empty_list_name = '[]'
    simple_list_name = '[…]'

    def list_name(self, data):
        if not data:
            return [self.empty_list_name]
        return [self.simple_list_name]

    def handle_list(self, data):
        return dict(
            name=self.list_name(data),
            children=[
                self.make(item)
                for item in data])

    empty_dict_name = '{}'
    simple_dict_name = '{…}'

    def dict_name(self, data):
        if not data:
            return [self.empty_dict_name]
        return [self.simple_dict_name]

    def dict_key_prefix(self, key):
        return [
            self.scalar_name(key, context='key'),
            ': ']

    def handle_dict(self, data):
        return dict(
            name=self.dict_name(data),
            children=[
                self.make(
                    value,
                    name_prefix=self.dict_key_prefix(key))
                for key, value in data.items()])

    def make(self, data, name_prefix=''):
        result = dict(_data=data)
        if isinstance(data, dict):
            result.update(self.handle_dict(data))
        elif isinstance(data, (list, tuple)):
            result.update(self.handle_list(data))
        else:
            result.update(self.handle_scalar(data))
        if name_prefix:
            if not isinstance(result['name'], list): raise Exception('...', type(result['name']), result['name'], type(data))
            result['name'] = [name_prefix] + result['name']
        return result

    def __call__(self, data):
        return self.make(data)


class ColoredTreeMaker(TreeMaker):

    def scalar_name(self, data, context=None):
        result = super(ColoredTreeMaker, self).scalar_name(data)
        style = 'scalar_key' if context == 'key' else 'scalar'
        return [(style, result)]


class ExtensiveTreeMaker(ColoredTreeMaker):

    ellipsis = '…'
    # Tricky to do better, as in the perfect case it depends on the terminal
    # width and the position in the tree.
    width = 100
    min_left_width = 10

    def _cut(self, value, width=None, right=1):
        if width is None:
            width = self.width
        if len(value) <= width:
            return value
        left_width = width - right - len(self.ellipsis)
        if left_width <= self.min_left_width:
            return value
        return '{}{}{}'.format(
            value[:left_width],
            self.ellipsis,
            value[-right:])

    def _some_name(self, data):
        dumped = self.dumps(data)
        return [self._cut(dumped)]

    def list_name(self, data):
        return self._some_name(data)

    def dict_name(self, data):
        return self._some_name(data)

    # Could also be useful to allow expanding/collapsing of large leaf nodes
    # with cut/uncut toggle.


class SomeTreeWidget(urwid.TreeWidget):
    """ Display widget for nodes """

    _is_effectively_leaf = None

    def get_display_text(self):
        return self.get_node().get_value()['name']

    def keypress(self, size, key, **kwargs):
        if key == '=':
            key = '+'
            # -> super()
        elif key == 'left':
            if self._is_effectively_leaf:
                key = 'up'
                # -> super()
            elif self.expanded:
                self.expanded = False
                self.update_expanded_icon()
                return None
            # else -> super()
        elif key == 'right':
            if self.expanded:
                # hack to go to the next child (usually)
                # TODO: actually do 'next child if any'
                key = 'down'
            # -> super()
        elif key == 'enter':  # toggle expand
            self.expanded = not self.expanded
            self.update_expanded_icon()
            return None
        return super(SomeTreeWidget, self).keypress(size, key, **kwargs)


class SomeLeafTreeWidget(SomeTreeWidget):
    """ See `SomeLeafParentNode` """

    _is_effectively_leaf = True

    def __init__(self, *args, **kwargs):
        super(SomeLeafTreeWidget, self).__init__(*args, **kwargs)
        self.update_expanded_icon()

    def update_expanded_icon(self, *args, **kwargs):
        # Hax: force the node to keep the expanded status.
        # When there's no children, there's no sense to toggle anything.
        # `True` is displayed as '-', `False` is displayed as '+'.
        self.expanded = True
        return super(SomeLeafTreeWidget, self).update_expanded_icon(*args, **kwargs)


class SomeNode(urwid.TreeNode):
    """ Data storage object for leaf nodes """

    def load_widget(self):
        return SomeTreeWidget(self)


class SomeParentNode(urwid.ParentNode):
    """ Data storage object for interior/parent nodes """

    @classmethod
    def get_child_class(cls, grandchildren):
        if grandchildren:
            return SomeParentNode
        # return SomeNode
        return SomeLeafParentNode

    def _get_children(self):
        data = self.get_value()
        return data.get('children') or ()

    def load_widget(self):
        if not self._get_children():
            # Make empty structures behave more like scalars.
            return SomeLeafTreeWidget(self)
        return SomeTreeWidget(self)

    def load_child_keys(self):
        children = self._get_children()
        return range(len(children))

    def load_child_node(self, key):
        """Return either an SomeNode or SomeParentNode"""
        children = self._get_children()
        childdata = children[key]
        childdepth = self.get_depth() + 1
        grandchildren = childdata.get('children')
        childclass = self.get_child_class(grandchildren)
        return childclass(childdata, parent=self, key=key, depth=childdepth)


class SomeLeafParentNode(SomeParentNode):
    """
    A ParentNode to be used as a leaf,
    instead of TreeNode,
    for consistent behavior.
    """

    def load_widget(self):
        return SomeLeafTreeWidget(self)


class SomeTreeBrowser:

    palette = [
        # ('body', 'black', 'light gray'),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('head', 'yellow', 'black', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'white', 'black', 'bold'),
        ('flag', 'dark gray', 'light gray'),
        ('error', 'dark red', 'light gray'),

        ('scalar_key', 'dark blue', ''),
        ('scalar', 'dark green', ''),
    ]

    spacer = "  "
    sep = ","
    footer_text = [
        ('title', "Some Data Browser"), spacer, spacer,
        ('key', "up"), sep, ('key', "down"), sep,
        ('key', "pgup"), sep, ('key', "pgdn"),
        spacer,
        ('key', "+"), sep,
        ('key', "-"), spacer,
        ('key', "left"), spacer,
        ('key', "home"), spacer,
        ('key', "end"), spacer,
        ('key', "q"),
    ]

    def __init__(self, data=None):
        self.topnode = SomeParentNode(data)
        self.listbox = urwid.TreeListBox(
            urwid.TreeWalker(self.topnode))
        self.listbox.offset_rows = 1
        self.header = urwid.Text("")
        self.footer = urwid.AttrWrap(
            urwid.Text(self.footer_text),
            'foot')
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer,
        )


class SomeMainTreeBrowser(SomeTreeBrowser):
    """ Entry point logic slapped on top of the tree browser """

    def __init__(self, *args, **kwargs):
        super(SomeMainTreeBrowser, self).__init__(*args, **kwargs)
        self.loop = urwid.MainLoop(
            self.view,
            self.palette,
            unhandled_input=self.unhandled_input,
        )

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def main(self):
        """Run the program."""
        self.loop.run()



USAGE = """
Usage:

    jsonbrowse some_file.json

    jsonbrowse "$json_data"
"""


def main(data=None, maker_cls=ColoredTreeMaker):
    if len(sys.argv) != 2:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    if data is None:
        arg = sys.argv[1]
        if arg.startswith('{') or arg.startswith('{'):
            data = json.loads(arg)
        else:
            with open(arg) as fobj:
                data = json.load(fobj)

    tree = maker_cls().make(data)
    return SomeMainTreeBrowser(tree).main()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(SAMPLE_DATA)
    else:
        main()
