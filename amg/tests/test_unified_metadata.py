import pytest

from amg import UnifiedMetadata

class Foo():
    @property
    def just_on_foo(self):
        return 'foo'

    @property
    def shared(self):
        return 'foobar'

    @property
    def override(self):
        return 'do not override me!'

    @property
    def too_much_sharing(self):
        return 'collision'

class Bar():
    @property
    def just_on_bar(self):
        return 'bar'
    
    @property
    def shared(self):
        return 'barfoo'

    @property
    def override(self):
        return 'do not override me either!'

    @property
    def too_much_sharing(self):
        return 'collision'

@pytest.fixture
def unified_metadata():
    sources = [Foo(), Bar()]
    overrides = {'override':'overridden'}
    mappings = {'shared':Bar}

    return UnifiedMetadata(sources=sources, overrides=overrides, mappings=mappings)

def test_get_property(unified_metadata):
    assert unified_metadata.just_on_foo == 'foo'

def test_mapping_shared_property(unified_metadata):
    assert unified_metadata.shared == 'barfoo'

def test_overridden_property(unified_metadata):
    assert unified_metadata.override == 'overridden'

def test_assert_warn_on_missing_property(unified_metadata):
    with pytest.warns(UserWarning) as warning:
        prop = unified_metadata.missing_property
        assert prop == None

def test_assert_warn_on_ambiguous_property(unified_metadata):
    with pytest.warns(UserWarning) as warning:
        prop = unified_metadata.too_much_sharing
        assert prop == None