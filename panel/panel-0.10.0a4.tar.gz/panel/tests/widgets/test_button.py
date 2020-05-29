from __future__ import absolute_import, division, unicode_literals

from panel.widgets import Button, Toggle


def test_button(document, comm):
    button = Button(name='Button')

    widget = button.get_root(document, comm=comm)

    assert isinstance(widget, button._widget_type)
    assert widget.label == 'Button'

    button._process_events({'clicks': 1})
    assert button.clicks == 1


def test_toggle(document, comm):
    toggle = Toggle(name='Toggle', value=True)

    widget = toggle.get_root(document, comm=comm)

    assert isinstance(widget, toggle._widget_type)
    assert widget.active == True
    assert widget.label == 'Toggle'

    widget.active = False
    toggle._process_events({'active': widget.active})
    assert toggle.value == False

    toggle.value = True
    assert widget.active == True
