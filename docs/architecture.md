# 🏗️ Architecture Deep Dive

How Context Optimizer works under the hood — and why it's safe, efficient, and effective.

## Core Principle: Compression at the Workflow Level

Most token waste happens because **users paste entire files** and **Claude reads them fully**. Our solution doesn't change Claude's model — it changes the **interaction pattern**.

```
Traditional: User → Paste 500 lines → Claude reads all 500 → Answers
Optimized:  User → Manifest (5 lines) → Claude asks for L40-60 → Reads 20 lines → Answers
```

## Three Layers of Optimization

### Layer 1: Structural Index (`CONTEXT_MANIFEST.md`)

The manifest is **not a summary** — it's a **locator**. Each entry:

```markdown
📄 src/auth/login.py
L12: class LoginHandler:
L15: def authenticate(username, password):
L28: def verify_2fa(token):
L45: def _hash_password(pwd):
```

- **10-15KB** for a 50KLOC codebase
- Contains **zero function bodies** (just signatures + line numbers)
- Claude uses this like a **table of contents** — finds what it needs without reading code

### Layer 2: Prompt Constraints (Custom Instructions)

We don't ask Claude nicely — we **constrain its behavior** with clear rules:

```
Never request full files unless "READ FULL FILE:" is explicitly stated
Always ask for specific line ranges
Quote max 3-5 lines per file
If >3 files needed, pause and ask for priority
```

These are **hard rules** Claude follows because Custom Instructions override its default helpfulness behavior.

### Layer 3: Structured Output Format

Every response uses the same schema:

```markdown
📍 Scope: [files/functions analyzed]
🧠 Analysis: [structural reasoning, minimal quoting]
⚠️ Impact: [affected code, risks, tests needed]
✅ Next: [exact next action for user]
```

This **enforces compression** — Claude can't ramble or over-explain.

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│  USER ACTION                                                  │
│  "Why is my auth failing?"                                    │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  CLAUDE (with Custom Instructions)                           │
│  → Checks manifest for auth-related files                    │
│  → Sees: src/auth/login.py (L12-45)                          │
│  → Asks: "Please show me lines 40-60 of login.py"            │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  USER                                                         │
│  → Pastes lines 40-60 (20 lines instead of 200)              │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  CLAUDE                                                       │
│  → Analyzes only those lines                                 │
│  → Quotes L45: "return hashlib.sha256(pwd).hexdigest()"      │
│  → Outputs structured response                               │
│  → 400 tokens total instead of 8,000                         │
└──────────────────────────────────────────────────────────────┘
```

## Why This Isn't Possible With Simple "Be Concise" Prompts

| Generic "be concise" | Context Optimizer |
|---------------------|-------------------|
| Claude still reads full files | Claude is forbidden from doing so |
| No structural index | Manifest provides efficient lookup |
| No token budget tracking | Explicit "pause at >3 files" rule |
| Varies by Claude mood | Consistent behavior every time |

## Security Analysis

### What Claude Sees

**Manifest-only mode (recommended):**
- File paths (e.g., `src/auth/login.py`)
- Function/class names (e.g., `def authenticate()`)
- Line numbers (e.g., `L45`)
- **NO** function bodies
- **NO** variable values
- **NO** comments or strings

**When you paste requested lines:**
- Claude sees exactly what you paste (20-100 lines)
- Same as any normal Claude conversation

### What Leaves Your Machine

**Nothing.** The tool runs **entirely locally**.

- Manifest files stay on your disk.
- You control what you paste into Claude.

## Comparison to Alternatives

| Approach | Security | Efficiency | Complexity |
|----------|----------|------------|------------|
| Paste entire codebase | ❌ Low | ❌ Terrible | ✅ Simple |
| Use API with filtering | ⚠️ Medium | ⚠️ Medium | ❌ Complex |
| Context Optimizer | ✅ High | ✅ Great | ✅ Simple |

## Extending the Architecture

### Adding a New Language

```python
# In tools/context_mapper.py
INDEX_EXTENSIONS = {".py", ".js", ".custom"}

# Add keyword detection for your language
if any(stripped.startswith(kw) for kw in [
    "def ", "class ", "func ",
    "custom_keyword "  # ← add yours
]):
```

### Increasing Token Savings Further

- Lower `MAX_FILES_PER_TURN` from 3 → 2
- Reduce snippet length from 5 lines → 3 lines
- Enable risk scoring (forces extra compression)

### Decreasing Savings (for faster responses)

- Raise `MAX_FILES_PER_TURN` to 5
- Allow slightly larger snippets
- Disable the budget pause

## Limitations

| Limitation | Mitigation |
|------------|------------|
| Claude can't see entire file without being pasted | That's the point — but complex refactors need full context |
| Manifest only updates when you run the script | Run weekly or on major changes |
| Requires user cooperation to paste requested lines | Skill prompts remind Claude to ask specifically |

## Future Possibilities

- **Git hooks** to auto-regenerate manifest
- **Language servers** (LSP) integration for real-time indexing
- **VS Code extension** with one-click upload
- **GitHub Action** to validate PRs with minimal token usage

---

This architecture is intentionally simple. **Complexity adds token overhead** — exactly what we're trying to avoid.
