---
title: CLI API
description: amplifier-app-cli API reference
---

# CLI API

The `amplifier-app-cli` package provides the reference CLI implementation.

**Source**: [github.com/microsoft/amplifier-app-cli](https://github.com/microsoft/amplifier-app-cli)

## Main Entry Point

The CLI entry point is `amplifier_app_cli.main:main`.

```python
from amplifier_app_cli.main import main

# Run the CLI
main()
```

## Commands

CLI commands are implemented in `amplifier_app_cli.commands`:

| Command | Description |
|---------|-------------|
| `run` | Execute prompts (single command or interactive) |
| `session` | Session management (list, show, continue) |
| `profile` | Profile management (list, use, show) |
| `provider` | Provider management (list, use, show) |
| `module` | Module management (list, show) |
| `collection` | Collection management (add, list, refresh) |

See [CLI Reference](../../user_guide/cli.md) for complete usage documentation.

## Architecture

```
amplifier-app-cli/
├── main.py              # Entry point, CLI group
├── commands/            # Command implementations
│   ├── run.py          # Run command
│   ├── session.py      # Session commands
│   ├── profile.py      # Profile commands
│   └── ...
└── utils/              # CLI utilities
```

For implementation details, see the [source repository](https://github.com/microsoft/amplifier-app-cli).
