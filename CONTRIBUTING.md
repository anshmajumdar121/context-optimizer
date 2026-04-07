# 🤝 Contributing to Context Optimizer

Thank you for your interest! This project maintains a **strict clean-room policy** to remain legally and ethically sound.

## 📋 Code of Conduct

By participating, you agree to our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and inclusive.

## 🚫 What We Do NOT Accept

| Category | Examples |
|----------|----------|
| **Leaked code** | Any content from proprietary Anthropic repositories |
| **Reverse-engineered APIs** | Unofficial endpoints, bypass methods |
| **Prompt injection attacks** | "Ignore previous instructions" tricks |
| **Obfuscated scripts** | Minified or encoded malicious code |
| **Unlicensed dependencies** | Third-party code without compatible licenses |

## ✅ What We Welcome

- **New language support** — Add extensions to `INDEX_EXTENSIONS`
- **Better keyword detection** — Improve structural parsing
- **Documentation improvements** — Clarify confusing sections
- **Bug fixes** — Any issue you discover
- **Benchmarks** — Real-world token measurements
- **Example workflows** — Show how you use it

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/context-optimizer.git
cd context-optimizer

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run tests (manual verification for now)
python tools/context_mapper.py ./test_project

# Make your changes
# ...

# Run the linter (if you have one)
# make lint
```

## 📝 Pull Request Process

1. **Fork** the repository
2. **Create a branch:** `git checkout -b feat/your-feature-name`
3. **Make changes** with clear commit messages
4. **Test locally** with at least 3 different codebases
5. **Update documentation** if you change behavior
6. **Open a Pull Request** with:
   - Clear description of changes
   - Before/after metrics if performance-related
   - Screenshots for UI changes (none expected)
7. **Wait for review** (usually within 48 hours)

## Commit Message Format

```
type(scope): short description

Longer explanation if needed.

Fixes #123
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

**Examples:**
- `feat(python): add async function detection`
- `fix(mapper): handle UTF-16 files gracefully`
- `docs(readme): add Rust installation instructions`

## 🧪 Testing Guidelines

Before submitting, verify:

```bash
# 1. Index a small project (< 100 files)
python tools/context_mapper.py ./small-project
# Check output format

# 2. Index a medium project (500-2000 files)
python tools/context_mapper.py ~/your-medium-project
# Verify no crashes

# 3. Run with custom extensions (if you added any)
python tools/context_mapper.py ./test-project-with-custom-ext

# 4. Ensure no external dependencies are required
python -c "import sys; print(sys.version)"  # Should show 3.8+
```

## 📜 License

By contributing, you agree that your contributions will be licensed under the **MIT License**.

## ❓ Questions?

Open a GitHub Discussion with the `Q&A` label. We're friendly!

Thank you for making AI-assisted coding more efficient for everyone!
