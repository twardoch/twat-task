"""Test suite for twat_pipeline."""

def test_version():
    """Verify package exposes version."""
    import twat_pipeline
    assert twat_pipeline.__version__

def test_plugin():
    """Verify plugin functionality."""
    import twat_pipeline
    plugin = twat_pipeline.Plugin()
    plugin.set("test", "value")
    assert plugin.get("test") == "value"
 