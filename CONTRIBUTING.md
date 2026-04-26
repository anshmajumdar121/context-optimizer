# Contributing to Context Optimizer

Thank you for your interest in improving Context Optimizer! This project maintains a **strict clean-room policy** to remain legally and ethically sound. Please read this guide before submitting anything.

## Code of Conduct

By participating, you agree to our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and inclusive.

## What We Welcome

- **New language support** — Add file extensions and import parsers to `context_mapper.py`
- **Better import detection** — Improve parsing for existing languages
- **Documentation improvements** — Clarify confusing sections, fix typos
- **Bug fixes** — Any reproducible issue you find
- **Real-world benchmarks** — Token savings measurements from actual codebases
- **Example workflows** — Show how you use Context Optimizer in your stack
- **Installer improvements** — Better agent detection, new editor integrations

## What We Do NOT Accept

| Category | Examples |
|----------|----------|
| Leaked code | Any content from proprietary Anthropic repositories |
| Reverse-engineered APIs | Unofficial endpoints, undocumented Claude internals |
| Prompt injection | "Ignore previous instructions" or jailbreak techniques |
| Obfuscated scripts | Minified, encoded, or intentionally unreadable code |
| Unlicensed dependencies | Third-party code without a compatible open-source license |
| External network calls | Any addition that phones home or calls external APIs at runtime |

## Development Setup

```bash
# Fork and clone
git clone https://github.com/<your-username>/context-optimizer.git
cd context-optimizer

# No install required — zero external dependencies
# Python 3.7+ only, pure standard library

# Test the mapper on a small project
python3 tools/context_mapper.py ./examples

# Test blast-radius
python3 tools/context_mapper.py ./examples --blast-radius tools/context_mapper.py

# Test the installer (safe, idempotent)
bash scripts/install.sh /tmp/test-project
```

## Commit Message Format

```
type(scope): short description

Longer explanation if needed.

Fixes #123
```

| Type | When to use |
|------|-------------|
| `feat` | New feature or language support |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change with no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Tooling, CI, dependency bumps |

**Examples:**
- `feat(mapper): add Kotlin import parser`
- `fix(mapper): handle UTF-16 encoded files gracefully`
- `docs(readme): add Windows WSL setup instructions`
- `perf(mapper): skip binary files without reading content`

## Pull Request Process

1. **Fork** the repository and create a branch: `git checkout -b feat/your-feature`
2. **Make your changes** — keep commits small and focused
3. **Test locally** against at least 2–3 different codebases of varying sizes
4. **Update docs** if you change any behavior or add new flags
5. **Open a Pull Request** with:
   - A clear description of what changed and why
   - Before/after token measurements if performance-related
   - Confirmation that no external dependencies were added
6. A maintainer will review within 48 hours

## Testing Checklist

Before submitting, run through this manually:

```bash
# 1. Small project (< 50 files)
python3 tools/context_mapper.py ./examples
# ✓ CONTEXT_MANIFEST.md generated
# ✓ .claude/graph.json generated
# ✓ No crash, no external calls

# 2. Blast-radius works
python3 tools/context_mapper.py ./examples --blast-radius tools/context_mapper.py
# ✓ JSON output with affected/changed/total_files/estimated_tokens

# 3. Zero dependencies confirmed
python3 -c "
import ast, json, os, re, sys
from pathlib import Path
from datetime import datetime
print('All stdlib imports OK')
"

# 4. Installer is idempotent
bash scripts/install.sh /tmp/test1
bash scripts/install.sh /tmp/test1  # second run should not error or duplicate
```

## Adding a New Language

To add support for a new language in `context_mapper.py`:

1. Add the file extension(s) to `EXTENSION_MAP`
2. Add an import extractor function: `extract_<lang>_imports(content) -> list`
3. Wire it into `extract_generic_imports()` with the correct language key
4. Test with a real codebase in that language
5. Add an entry to the `examples/` folder showing sample output

## License

By contributing, you agree that your contributions will be licensed under the **MIT License** — the same license as this project.

## Questions?

Open a [GitHub Discussion](https://github.com/anshmajumdar121/context-optimizer/discussions) with the `Q&A` label, or email **anshmajumdar100@gmail.com**.
