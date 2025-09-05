#### install uv and dependencies
```bash
pip install uv
```

Create virtual env
```bash
uv venv
```

For linux/macos :
```bash
source .venv/bin/activate
```

For windows:
```bash
.venv\Scripts\activate
```

Install dependencies
```bash
uv sync --native-tls
```

For some platform like macos (darwin), uv may throw an error during the `uv sync` command, for example greenlet / onnxruntime ...etc.<br/>
In that case, you can specify compatible version to your platform in uv override environment section:
```yaml
[tool.uv]
override-dependencies = ["greenlet==3.2.2; sys_platform == 'darwin'"]
```

#### Run unit tests
```bash
uv sync --group dev
uv run pytest
```

#### Update lock file
```bash
uv lock 
```
