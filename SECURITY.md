# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Active |
| < 1.0   | ❌ No     |

## Reporting a Vulnerability

**Do NOT report security vulnerabilities through public GitHub issues.**

Email the maintainer directly at **anshmajumdar100@gmail.com** with the subject line `[SECURITY] Context Optimizer — <brief description>`.

Please include:
- A clear description of the vulnerability
- Steps to reproduce (if applicable)
- The potential impact or attack scenario
- Your suggested fix (optional but appreciated)

**Response timeline:**

| Stage | Time |
|-------|------|
| Acknowledgment | Within 24 hours |
| Preliminary assessment | Within 48 hours |
| Fix or mitigation (critical) | Within 7 days |
| Public disclosure | Coordinated with reporter |

We follow [responsible disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure) — report privately first, give us time to fix, then we coordinate public disclosure together.

## Security Design of This Tool

Context Optimizer is designed to be safe by construction:

| Property | Detail |
|----------|--------|
| **Runs entirely locally** | `context_mapper.py` makes zero network calls |
| **No data transmission** | Your code never leaves your machine |
| **Zero external dependencies** | Pure Python 3.7+ standard library only |
| **No full source in manifest** | `CONTEXT_MANIFEST.md` contains file paths, line counts, import lists, and 20-line previews — not full file contents |
| **Read-only operation** | The mapper only reads files; it never modifies your codebase |
| **Idempotent installer** | `install.sh` only appends markers, never overwrites existing content blindly |

## What the Manifest Contains

Before uploading `CONTEXT_MANIFEST.md` to Claude Projects, be aware it includes:

- ✅ File paths and directory structure
- ✅ Language, line counts, file sizes
- ✅ Import/dependency relationships
- ✅ First 20 lines of each indexed file (preview)
- ❌ No full file contents
- ❌ No environment variables or secrets (as long as `.env` files are in `.claudeignore`)

**Recommendation:** Always review your `.claudeignore` before running the mapper to ensure secrets, `.env` files, and private config are excluded.

## Best Practices for Users

1. **Never paste secrets into Claude** — the manifest does not include secrets, but don't add them manually
2. **Keep `.claudeignore` updated** — exclude `.env`, `*.key`, `secrets/`, and similar paths
3. **Run the mapper only on trusted codebases** — the 20-line preview will be visible in Claude's context
4. **Use Claude Projects** for manifest upload rather than pasting into public chats
5. **Rotate tokens regularly** — if you use PATs to push updates, revoke them after use

## Known Limitations

- The 20-line file preview in `CONTEXT_MANIFEST.md` may expose internal logic, function signatures, or sensitive identifiers if they appear in the first 20 lines of a file
- Function and class names in the dependency graph may reveal architectural details of your codebase

These are by design (Claude needs structural context to work efficiently) — just be mindful of what you upload to shared Claude Projects.
