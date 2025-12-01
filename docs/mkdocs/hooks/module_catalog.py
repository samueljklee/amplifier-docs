"""
MkDocs hook for auto-generating module catalog from repository structure.

This hook scans the amplifier-dev directory for module repositories and generates
documentation pages for each module type (providers, tools, hooks, orchestrators, contexts).
"""

import logging
from pathlib import Path
from typing import Any

try:
    import tomli
except ImportError:
    tomli = None

try:
    import yaml
except ImportError:
    yaml = None

log = logging.getLogger("mkdocs.hooks.module_catalog")

# Module type mappings
MODULE_TYPES = {
    "provider": {
        "prefix": "amplifier-module-provider-",
        "docs_path": "modules/providers",
        "display_name": "Providers",
        "description": "LLM backend integrations",
    },
    "tool": {
        "prefix": "amplifier-module-tool-",
        "docs_path": "modules/tools",
        "display_name": "Tools",
        "description": "Agent capabilities",
    },
    "hooks": {
        "prefix": "amplifier-module-hooks-",
        "docs_path": "modules/hooks",
        "display_name": "Hooks",
        "description": "Observability and control",
    },
    "loop": {
        "prefix": "amplifier-module-loop-",
        "docs_path": "modules/orchestrators",
        "display_name": "Orchestrators",
        "description": "Execution loop strategies",
    },
    "context": {
        "prefix": "amplifier-module-context-",
        "docs_path": "modules/contexts",
        "display_name": "Contexts",
        "description": "Memory management",
    },
}


def get_module_info(module_path: Path) -> dict[str, Any] | None:
    """Extract module information from pyproject.toml and README."""
    pyproject_path = module_path / "pyproject.toml"
    readme_path = module_path / "README.md"

    if not pyproject_path.exists():
        return None

    info = {
        "name": module_path.name,
        "path": str(module_path),
        "description": "",
        "version": "",
        "entry_point": "",
        "readme_content": "",
    }

    # Parse pyproject.toml
    if tomli:
        try:
            with open(pyproject_path, "rb") as f:
                data = tomli.load(f)
                project = data.get("project", {})
                info["description"] = project.get("description", "")
                info["version"] = project.get("version", "")

                # Get entry point
                entry_points = project.get("entry-points", {})
                amplifier_modules = entry_points.get("amplifier.modules", {})
                if amplifier_modules:
                    info["entry_point"] = list(amplifier_modules.keys())[0]
        except Exception as e:
            log.warning(f"Failed to parse {pyproject_path}: {e}")

    # Read README
    if readme_path.exists():
        try:
            info["readme_content"] = readme_path.read_text()
        except Exception as e:
            log.warning(f"Failed to read {readme_path}: {e}")

    return info


def discover_modules(base_path: Path) -> dict[str, list[dict[str, Any]]]:
    """Discover all Amplifier modules in the repository."""
    modules_by_type: dict[str, list[dict[str, Any]]] = {
        key: [] for key in MODULE_TYPES
    }

    for module_type, config in MODULE_TYPES.items():
        prefix = config["prefix"]
        for path in base_path.iterdir():
            if path.is_dir() and path.name.startswith(prefix):
                info = get_module_info(path)
                if info:
                    # Extract the module name without prefix
                    info["short_name"] = path.name[len(prefix):]
                    modules_by_type[module_type].append(info)

        # Sort by name
        modules_by_type[module_type].sort(key=lambda x: x["short_name"])

    return modules_by_type


def generate_module_page(module_info: dict[str, Any], module_type: str) -> str:
    """Generate a documentation page for a module."""
    config = MODULE_TYPES[module_type]
    name = module_info["short_name"]
    full_name = module_info["name"]
    description = module_info["description"]
    entry_point = module_info["entry_point"]
    readme = module_info["readme_content"]

    # Generate page content
    content = f"""# {name.replace("-", " ").title()}

{description}

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `{entry_point}` |
| **Package** | `{full_name}` |
| **Type** | {config["display_name"]} |
| **Repository** | [github.com/microsoft/{full_name}](https://github.com/microsoft/{full_name}) |

## Installation

This module is installed automatically when referenced in a profile or mount plan.

```yaml
{module_type}s:
  - module: {entry_point}
    source: git+https://github.com/microsoft/{full_name}@main
```

## Documentation

The full documentation for this module is maintained in its repository:

**[View Full Documentation →](https://github.com/microsoft/{full_name})**

---

"""

    # Include README content if available (after first heading)
    if readme:
        # Skip the first heading (# Module Name) if present
        lines = readme.split("\n")
        skip_first_heading = False
        filtered_lines = []
        for line in lines:
            if line.startswith("# ") and not skip_first_heading:
                skip_first_heading = True
                continue
            filtered_lines.append(line)

        if filtered_lines:
            content += "\n".join(filtered_lines)

    return content


def on_config(config: dict[str, Any]) -> dict[str, Any]:
    """MkDocs hook called during configuration."""
    log.info("Module catalog hook: scanning for modules...")

    # Get the base path - try to find amplifier-dev parent directory
    # In standalone mode, this won't exist and we'll just have empty module lists
    docs_dir = Path(config.get("docs_dir", "docs"))
    base_path = docs_dir.parent.parent  # Go from amplifier-docs/docs to potential amplifier-dev

    # Check if we're in the amplifier-dev context (has module directories)
    has_modules = any(
        p.is_dir() and p.name.startswith("amplifier-module-")
        for p in base_path.iterdir()
    ) if base_path.exists() else False

    if has_modules:
        modules = discover_modules(base_path)
        # Log discovered modules
        for module_type, module_list in modules.items():
            if module_list:
                log.info(f"  Found {len(module_list)} {MODULE_TYPES[module_type]['display_name'].lower()}")
    else:
        log.info("  No local modules found (standalone mode)")
        modules = {key: [] for key in MODULE_TYPES}

    # Store modules in config for later use
    config["amplifier_modules"] = modules

    return config


def on_files(files: Any, config: dict[str, Any]) -> Any:
    """MkDocs hook called after files are collected."""
    # This hook could be used to dynamically generate module pages
    # For now, we rely on the static pages that link to module READMEs
    return files


def on_page_markdown(
    markdown: str, page: Any, config: dict[str, Any], files: Any
) -> str:
    """MkDocs hook called for each page's markdown content."""
    # Replace placeholder markers with dynamic content
    modules = config.get("amplifier_modules", {})

    # Replace module catalog placeholder
    if "<!-- MODULE_CATALOG -->" in markdown:
        catalog = generate_module_catalog(modules)
        markdown = markdown.replace("<!-- MODULE_CATALOG -->", catalog)

    # Replace specific module type placeholders
    for module_type, config_data in MODULE_TYPES.items():
        placeholder = f"<!-- MODULE_LIST_{module_type.upper()} -->"
        if placeholder in markdown:
            module_list = generate_module_list(modules.get(module_type, []), module_type)
            markdown = markdown.replace(placeholder, module_list)

    return markdown


def generate_module_catalog(modules: dict[str, list[dict[str, Any]]]) -> str:
    """Generate a full module catalog."""
    content = ""

    for module_type, module_list in modules.items():
        if not module_list:
            continue

        config = MODULE_TYPES[module_type]
        content += f"\n### {config['display_name']}\n\n"
        content += f"{config['description']}\n\n"
        content += "| Module | Description |\n"
        content += "|--------|-------------|\n"

        for module in module_list:
            name = module["short_name"]
            desc = module["description"][:80] + "..." if len(module["description"]) > 80 else module["description"]
            link = f"[{name}]({config['docs_path']}/{name.replace('-', '_')}.md)"
            content += f"| {link} | {desc} |\n"

        content += "\n"

    return content


def generate_module_list(modules: list[dict[str, Any]], module_type: str) -> str:
    """Generate a list of modules for a specific type."""
    if not modules:
        return "*No modules found.*"

    content = ""
    for module in modules:
        name = module["short_name"]
        desc = module["description"]
        entry_point = module["entry_point"]

        content += f"""
<div class="module-card">
<div class="content">
<h4><a href="{name.replace('-', '_')}.md">{name.replace("-", " ").title()}</a></h4>
<p>{desc}</p>
<code>{entry_point}</code>
</div>
</div>
"""

    return content
