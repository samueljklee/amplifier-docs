---
title: Coordinator API
description: ModuleCoordinator class reference
---

# Coordinator API

The `ModuleCoordinator` manages module lifecycle and provides access to loaded modules.

**Source**: [amplifier_core/coordinator.py](https://github.com/microsoft/amplifier-core/blob/main/amplifier_core/coordinator.py)

## ModuleCoordinator

The coordinator is created by `AmplifierSession` and provides access to:

- Loaded providers
- Loaded tools
- Hook registry
- Context manager

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `providers` | `list[Provider]` | Loaded provider modules |
| `tools` | `dict[str, Tool]` | Loaded tools by name |
| `hooks` | `HookRegistry` | Hook registry for event emission |
| `context` | `ContextManager` | Context/memory manager |
| `orchestrator` | `Orchestrator` | Execution orchestrator |

### Methods

#### `register_provider(provider)`

Register a provider module.

#### `register_tool(name, tool)`

Register a tool module with a name.

#### `get_tool(name) -> Tool`

Get a registered tool by name.

#### `emit(event, data)`

Emit an event through the hook registry.

```python
await coordinator.emit("tool:pre", {"name": "bash", "input": "ls"})
```

### Module Loading

Modules are loaded via the mount plan during session initialization:

```python
# Mount plan specifies modules to load
config = {
    "providers": [{"module": "provider-anthropic", ...}],
    "tools": [{"module": "tool-bash", ...}],
    ...
}

# Coordinator loads modules during session.initialize()
async with AmplifierSession(config=config) as session:
    # session.coordinator has all modules loaded
    pass
```

For implementation details, see the [source](https://github.com/microsoft/amplifier-core/blob/main/amplifier_core/coordinator.py).
