import pytest

from dephell_versioning import bump_version


@pytest.mark.parametrize('rule, old, new', [
    ('init', '', '0.1.0'),
    ('major', '1.2.3', '2.0.0'),
    ('minor', '1.2.3', '1.3.0'),
    ('patch', '1.2.3', '1.2.4'),

    # special part
    ('pre',   '1.2.3', '1.2.3-rc.1'),
    ('local', '1.2.3', '1.2.3+1'),

    # bump special part
    ('pre',   '1.2.3-rc.1', '1.2.3-rc.2'),
    ('local', '1.2.3+1', '1.2.3+2'),

    # release
    ('release', '1.2.3', '1.2.3'),
    ('release', '1.2.3-rc.1', '1.2.3'),
    ('release', '1.2.3+1', '1.2.3'),
    ('release', '1.2.3-rc.1+1', '1.2.3'),
])
def test_bump_version(rule, old, new):
    assert bump_version(rule=rule, version=old, scheme='semver') == new
