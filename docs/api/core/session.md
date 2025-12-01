---
title: Session API
description: AmplifierSession class reference
---

# Session API

The `AmplifierSession` class is the main interface for interacting with Amplifier.

**Source**: [amplifier_core/session.py](https://github.com/microsoft/amplifier-core/blob/main/amplifier_core/session.py)

## AmplifierSession

```python
from amplifier_core import AmplifierSession

async with AmplifierSession(config=mount_plan) as session:
    response = await session.execute("Hello, world!")
```

### Constructor

```python
AmplifierSession(
    config: dict,           # Mount plan configuration
    session_id: str = None  # Optional session ID (auto-generated if not provided)
)
```

### Methods

#### `initialize()`

Initialize the session, loading all modules specified in the mount plan.

```python
await session.initialize()
```

#### `execute(prompt: str) -> str`

Execute a prompt and return the response.

```python
response = await session.execute("Explain this code")
```

#### `fork(agent_config: dict) -> AmplifierSession`

Create a sub-session with a different configuration (for agent delegation).

```python
sub_session = await session.fork(agent_config)
```

#### `cleanup()`

Clean up session resources.

```python
await session.cleanup()
```

### Context Manager

`AmplifierSession` supports async context manager for automatic initialization and cleanup:

```python
async with AmplifierSession(config=config) as session:
    # Session is initialized
    response = await session.execute(prompt)
# Session is cleaned up
```

## Example

```python
import asyncio
from amplifier_core import AmplifierSession

config = {
    "session": {
        "orchestrator": "loop-basic",
        "context": "context-simple"
    },
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
        "config": {"model": "claude-sonnet-4-5"}
    }],
    "tools": []
}

async def main():
    async with AmplifierSession(config=config) as session:
        response = await session.execute("What is 2 + 2?")
        print(response)

asyncio.run(main())
```
