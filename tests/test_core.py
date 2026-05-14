import pytest
import tempfile
import shutil
from pathlib import Path
from promptforge.core import PromptStore, PromptVersion, ForgeConfig


@pytest.fixture
def tmp_project():
    d = tempfile.mkdtemp()
    Path(d, ".promptforge").mkdir()
    Path(d, ".promptforge", "prompts").mkdir()
    Path(d, ".promptforge", "meta").mkdir()
    yield d
    shutil.rmtree(d)


def test_prompt_add(tmp_project):
    store = PromptStore(tmp_project)
    pv = store.add("test-prompt", "You are a helpful assistant.", "Initial commit", "test")
    
    assert pv.name == "test-prompt"
    assert pv.prompt_text == "You are a helpful assistant."
    assert pv.version_id.startswith("v1_")
    assert pv.parent_id is None


def test_prompt_versioning(tmp_project):
    store = PromptStore(tmp_project)
    v1 = store.add("test-prompt", "You are helpful.", "v1", "test")
    v2 = store.add("test-prompt", "You are very helpful.", "v2", "test")
    
    assert v2.parent_id == v1.version_id
    assert v2.version_id.startswith("v2_")
    
    versions = store.log("test-prompt")
    assert len(versions) == 2


def test_prompt_retrieval(tmp_project):
    store = PromptStore(tmp_project)
    original = store.add("test-prompt", "Hello world.", "initial", "test")
    retrieved = store.get("test-prompt", original.version_id)
    
    assert retrieved is not None
    assert retrieved.prompt_text == original.prompt_text
    assert retrieved.version_id == original.version_id


def test_prompt_diff(tmp_project):
    store = PromptStore(tmp_project)
    v1 = store.add("test-prompt", "You are helpful.", "v1", "test")
    v2 = store.add("test-prompt", "You are very helpful.", "v2", "test")
    
    diff = store.diff("test-prompt", v1.version_id, v2.version_id)
    assert "helpful" in diff
    assert ("helpful." in diff) or ("very helpful" in diff)


def test_config(tmp_project):
    cfg = ForgeConfig(tmp_project)
    cfg.set("default_author", "aman")
    assert cfg.get("default_author") == "aman"
    assert cfg.get("missing_key", "default") == "default"
