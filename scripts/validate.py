"""Validate the distributed template without launching model calls (Python 3.11+)."""
from pathlib import Path
import tomllib

root = Path(__file__).resolve().parents[1]
config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
assert config["agents"]["enabled"] is True
assert config["agents"]["max_concurrent_threads_per_session"] == 3
policy = (root / "AGENTS.md").read_text(encoding="utf-8")
expected = {
    "code-searcher": ("gpt-5.6-luna", "low", True),
    "docs-researcher": ("gpt-5.6-luna", "low", True),
    "test-runner": ("gpt-5.6-luna", "low", False),
    "implementer": ("gpt-5.6-terra", "medium", False),
    "deep-thinker": ("gpt-6-astra", "high", True),
    "advisor": ("gpt-6-astra", "high", True),
}
files = sorted((root / ".codex/agents").glob("*.toml"))
assert {p.stem for p in files} == set(expected)
for path in files:
    role = tomllib.loads(path.read_text(encoding="utf-8"))
    model, effort, read_only = expected[path.stem]
    assert role["name"] == path.stem and path.stem in policy, path
    assert role["description"].strip() and role["developer_instructions"].strip(), path
    assert (role["model"], role["model_reasoning_effort"]) == (model, effort), path
    assert (role.get("sandbox_mode") == "read-only") == read_only, path
print("PASS: project TOML, six agent definitions, routing names and model/effort settings")
