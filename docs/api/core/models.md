---
title: Models API
description: Data model reference
---

# Models API

Core data models used throughout Amplifier.

**Source**: [amplifier_core/models.py](https://github.com/microsoft/amplifier-core/blob/main/amplifier_core/models.py)

## ToolResult

Result returned by tool execution.

```python
@dataclass
class ToolResult:
    output: str           # Tool output (success message or result)
    error: str = None     # Error message if failed
    success: bool = True  # Whether execution succeeded
```

### Example

```python
# Successful result
ToolResult(output="File created successfully", success=True)

# Failed result
ToolResult(output="", error="Permission denied", success=False)
```

## ToolCall

Represents an LLM's request to call a tool.

```python
@dataclass
class ToolCall:
    id: str           # Unique call ID
    name: str         # Tool name
    input: dict       # Tool input parameters
```

### Example

```python
ToolCall(
    id="call_123",
    name="bash",
    input={"command": "ls -la"}
)
```

## ProviderInfo

Information about a loaded provider.

```python
@dataclass
class ProviderInfo:
    name: str              # Provider name (e.g., "anthropic")
    models: list[str]      # Available model IDs
    default_model: str     # Default model to use
```

## ModelInfo

Information about an AI model.

```python
@dataclass
class ModelInfo:
    id: str                    # Model identifier
    name: str                  # Display name
    context_window: int        # Max context tokens
    max_output_tokens: int     # Max output tokens
    supports_tools: bool       # Tool calling support
    supports_vision: bool      # Image input support
```

## ModuleInfo

Information about a loaded module.

```python
@dataclass
class ModuleInfo:
    name: str          # Module name
    type: str          # Module type (provider, tool, hook, etc.)
    version: str       # Module version
    source: str        # Source URL or path
```

## HookResult

See [Hooks API](hooks.md) for HookResult documentation.
