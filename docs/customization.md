# Customization Guide

Tailor Context Optimizer for your specific needs.

## Customizing the Indexer

### Add New File Extensions

Edit `tools/context_mapper.py`:

```python
INDEX_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    # Add your extensions:
    ".lua",
    ".vim",
    ".custom",
}
```

### Add Keywords for New Languages

```python
KEYWORDS = {
    # ... existing languages ...
    ".lua": ["function ", "local function ", "local "],
    ".vim": ["function! ", "def ", "class "],
}
```

### Skip Additional Directories

```python
SKIP_DIRS = {
    "node_modules",
    ".git",
    # Add your directories:
    "vendor",
    "third_party",
    "legacy_code",
}
```

## Customizing the Skill

### Adjust Token Budgets

Edit `skill/claude-custom-instructions.md`:

```markdown
### Token Budget

- **Soft limit:** 300 tokens per response  # Lower = more savings
- **Hard limit:** 800 tokens per response
- **Pause rule:** If you need >2 files, pause and ask for priority
```

### Change Response Format

Modify the structure to match your workflow:

```markdown
### Response Format

```markdown
📍 Scope: [files/functions]
🔍 Issue: [problem identified]
💡 Solution: [proposed fix]
🧪 Test: [how to verify]
⏭️ Next: [specific action]
```
```

### Add Language-Specific Rules

```markdown
### Python-Specific

- Type hints: Skip unless relevant to the issue
- Docstrings: Never quote full docstrings
- Focus on: Function signatures and logic flow

### JavaScript-Specific

- Skip: JSDoc comments
- Focus on: Async/await patterns, import chains
```

## Customizing the One-Click Prompt

### For Code Reviews

```markdown
🔒 SESSION MODE: CODE REVIEW (TOKEN-OPTIMIZED)

Focus on:
- Security vulnerabilities
- Performance bottlenecks
- Logic errors

Skip:
- Style issues
- Formatting
- Naming preferences

[rest of prompt...]
```

### For Learning/Exploration

```markdown
🔒 SESSION MODE: EXPLORATION (TOKEN-OPTIMIZED)

Be concise but thorough:
- Explain concepts simply
- Use analogies
- Ask clarifying questions

Budget: Standard (not minimal) for better explanations
```

### For Debugging

```markdown
🔒 SESSION MODE: DEBUGGING (TOKEN-OPTIMIZED)

Priority:
1. Root cause identification
2. Minimal reproduction case
3. Fix suggestion

Skip:
- Explanations of working code
- Alternative approaches (unless asked)
```

## Project-Specific Configurations

### Monorepo Setup

For large monorepos, create separate manifests:

```bash
# Frontend
python tools/context_mapper.py /monorepo/frontend --output FRONTEND_MANIFEST.md

# Backend
python tools/context_mapper.py /monorepo/backend --output BACKEND_MANIFEST.md

# Shared
python tools/context_mapper.py /monorepo/shared --output SHARED_MANIFEST.md
```

Upload all three to your Claude Project.

### Microservices Setup

Create a manifest per service:

```bash
for service in services/*; do
    python tools/context_mapper.py "$service" --output "${service}_MANIFEST.md"
done
```

### Legacy Codebase

Exclude legacy directories:

```python
SKIP_DIRS = {
    # ... defaults ...
    "legacy",
    "deprecated",
    "old_version",
}
```

## Advanced Customization

### Pre-Process Manifest

Add a script to filter the manifest:

```python
# filter_manifest.py
import re

with open('CONTEXT_MANIFEST.md', 'r') as f:
    content = f.read()

# Remove test files
content = re.sub(r'📄 .*test.*\.py\n(?:L\d+: .*\n)*', '', content)

# Remove internal utilities
content = re.sub(r'📄 .*_internal/.*\n(?:L\d+: .*\n)*', '', content)

with open('CONTEXT_MANIFEST_FILTERED.md', 'w') as f:
    f.write(content)
```

### Post-Process Claude's Output

Create a script to extract actionable items:

```python
# extract_actions.py
import re

claude_output = """[paste Claude's response]"""

# Extract "Next" sections
next_steps = re.findall(r'✅ Next:\n(.+?)(?=\n📍|$)', claude_output, re.DOTALL)

for i, step in enumerate(next_steps, 1):
    print(f"{i}. {step.strip()}")
```

## Sharing Customizations

If you create useful customizations:

1. Fork the repository
2. Add your customization to `examples/customizations/`
3. Submit a pull request
4. Share in GitHub Discussions

## Examples

See the `examples/` directory for:
- Python FastAPI setup
- React TypeScript setup
- Rust CLI setup

Each includes customized configurations for that stack.
