"""YAML load/dump utilities with consistent formatting."""
import json
import yaml
from pathlib import Path
from typing import Any


class _LiteralStr(str):
    """String subclass for YAML literal block scalar output."""
    pass


def _literal_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


# Register the representer
yaml.add_representer(_LiteralStr, _literal_representer)


def load_yaml(path: str) -> dict:
    """Load a YAML file and return its contents as a dict."""
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    return data


def dump_yaml(data: dict, path: str) -> None:
    """Write a dict to a YAML file with consistent formatting."""
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )


def dump_yaml_string(data: dict) -> str:
    """Serialize a dict to a YAML string."""
    return yaml.dump(
        data,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )


def load_json(path: str) -> dict:
    """Load a JSON file and return its contents as a dict."""
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if data is not None else {}


def dump_json(data: dict, path: str) -> None:
    """Write a dict to a JSON file with pretty formatting."""
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def literal_str(text: str) -> _LiteralStr:
    """Wrap text for YAML literal block scalar output (multiline strings)."""
    return _LiteralStr(text)


def safe_get(data: dict, *keys, default: Any = None) -> Any:
    """Safely navigate nested dict keys, returning default if any key is missing."""
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        elif isinstance(current, list) and isinstance(key, int) and key < len(current):
            current = current[key]
        else:
            return default
        if current is default:
            return default
    return current


def write_text(content: str, path: str) -> None:
    """Write text content to a file, creating parent directories as needed."""
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
