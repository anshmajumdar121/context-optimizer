#!/usr/bin/env python3
"""
Context Mapper — Manifest Generator + Graph Builder
Generates CONTEXT_MANIFEST.md and a lightweight dependency graph.
Zero external dependencies. Pure Python 3.7+.
"""

import os
import sys
import json
import re
import ast
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────

IGNORE_PATTERNS = [
    ".git", ".gitignore", ".github",
    "__pycache__", "*.pyc", ".venv", "venv", "env",
    "*.egg-info", "dist", "build",
    "node_modules", "package-lock.json", "yarn.lock",
    ".vscode", ".idea", ".cursor", ".windsurf",
    "dist", "build", "target", ".next", ".output",
    "*.min.js", "*.min.css", "*.map",
    "coverage", ".coverage", "htmlcov",
    ".DS_Store", "Thumbs.db",
    ".claude/completions", ".claude/sessions",
    "docs/archive", "docs/learnings",
]

MAX_FILE_SIZE = 500_000
MAX_LINES_PREVIEW = 50

EXTENSION_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".jsx": "jsx", ".tsx": "tsx", ".go": "go", ".rs": "rust",
    ".java": "java", ".kt": "kotlin", ".rb": "ruby", ".php": "php",
    ".cs": "csharp", ".cpp": "cpp", ".c": "c", ".h": "c",
    ".swift": "swift", ".scala": "scala", ".r": "r", ".m": "objc",
    ".sh": "bash", ".sql": "sql", ".md": "markdown",
    ".yaml": "yaml", ".yml": "yaml", ".json": "json",
    ".toml": "toml", ".dockerfile": "dockerfile", ".tf": "terraform",
}


def should_ignore(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    parts = rel.parts
    name = path.name
    for pattern in IGNORE_PATTERNS:
        if pattern in parts:
            return True
        if pattern.startswith("*") and name.endswith(pattern[1:]):
            return True
        if name == pattern:
            return True
    return False


def detect_language(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext]
    if path.name.lower() == "dockerfile":
        return "dockerfile"
    if path.name.lower() == "makefile":
        return "makefile"
    return "unknown"


def get_file_preview(path: Path, max_lines: int = MAX_LINES_PREVIEW) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.rstrip())
            return "\n".join(lines)
    except Exception:
        return "[binary or unreadable]"


def parse_python_imports(path: Path) -> dict:
    imports = {"modules": [], "names": [], "local": []}
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read())
    except Exception:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports["modules"].append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level > 0:
                imports["local"].append(f"{'.' * node.level}{module}")
            else:
                imports["modules"].append(module.split(".")[0])
                for alias in node.names:
                    imports["names"].append(alias.name)
    return imports


def extract_js_imports(content: str) -> list:
    imports = []
    for match in re.finditer(r'import\s+.*?\s+from\s+["\']([^"\']+)["\']', content):
        imports.append(match.group(1))
    for match in re.finditer(r'require\(["\']([^"\']+)["\']\)', content):
        imports.append(match.group(1))
    return imports


def extract_go_imports(content: str) -> list:
    imports = []
    for match in re.finditer(r'import\s+\((.*?)\)', content, re.DOTALL):
        block = match.group(1)
        for line in block.split("\n"):
            line = line.strip().strip('"')
            if line and not line.startswith("//"):
                parts = line.split()
                if len(parts) >= 1:
                    imports.append(parts[-1].strip('"'))
    for match in re.finditer(r'import\s+["\']([^"\']+)["\']', content):
        imports.append(match.group(1))
    return imports


def extract_rust_imports(content: str) -> list:
    imports = []
    for match in re.finditer(r'use\s+([^;]+);', content):
        imports.append(match.group(1).strip())
    for match in re.finditer(r'extern\s+crate\s+(\w+)', content):
        imports.append(match.group(1))
    return imports


def extract_generic_imports(path: Path, content: str, lang: str) -> list:
    if lang in ("javascript", "typescript", "jsx", "tsx"):
        return extract_js_imports(content)
    elif lang == "go":
        return extract_go_imports(content)
    elif lang == "rust":
        return extract_rust_imports(content)
    elif lang == "python":
        result = parse_python_imports(path)
        return result["modules"] + result["local"]
    return []


class DependencyGraph:
    def __init__(self, root: Path):
        self.root = root
        self.nodes = {}
        self.edges = []

    def scan(self):
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            if should_ignore(path, self.root):
                continue
            if path.stat().st_size > MAX_FILE_SIZE:
                continue
            lang = detect_language(path)
            if lang == "unknown":
                continue

            rel_path = str(path.relative_to(self.root))
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                lines = content.count("\n") + 1
            except Exception:
                continue

            imports = extract_generic_imports(path, content, lang)
            self.nodes[rel_path] = {
                "language": lang,
                "size": path.stat().st_size,
                "lines": lines,
                "imports": imports,
                "preview": get_file_preview(path, 20),
            }
            for imp in imports:
                resolved = self._resolve_import(imp, path, lang)
                if resolved:
                    self.edges.append((rel_path, resolved, "imports"))

    def _resolve_import(self, imp: str, from_path: Path, lang: str) -> str:
        if lang == "python":
            if imp.startswith("."):
                base = from_path.parent
                dots = 0
                for c in imp:
                    if c == ".":
                        dots += 1
                    else:
                        break
                parts = imp[dots:].split(".")
                for _ in range(dots - 1):
                    base = base.parent
                candidate = base / "/".join(parts)
                if (candidate.with_suffix(".py")).exists():
                    return str(candidate.with_suffix(".py").relative_to(self.root))
                if (candidate / "__init__.py").exists():
                    return str((candidate / "__init__.py").relative_to(self.root))
            else:
                top = imp.split(".")[0]
                for p in self.root.rglob(f"{top}/__init__.py"):
                    return str(p.relative_to(self.root))
                for p in self.root.rglob(f"{top}.py"):
                    return str(p.relative_to(self.root))

        if lang in ("javascript", "typescript", "jsx", "tsx"):
            if imp.startswith("."):
                base = from_path.parent
                candidate = base / imp
                for ext in ["", ".js", ".ts", ".jsx", ".tsx", "/index.js", "/index.ts"]:
                    if ext.startswith("/"):
                        full = candidate / ext[1:]
                    else:
                        full = candidate.with_suffix(ext) if ext else candidate
                    if full.exists():
                        return str(full.relative_to(self.root))

        if lang == "go":
            if self.root.name in imp:
                local_part = imp.split(self.root.name, 1)[-1].lstrip("/")
                candidate = self.root / local_part
                candidate = candidate.with_suffix(".go")
                if candidate.exists():
                    return str(candidate.relative_to(self.root))

        return None

    def get_blast_radius(self, changed_files: list) -> dict:
        affected = set(changed_files)
        queue = list(changed_files)
        visited = set(changed_files)
        while queue:
            current = queue.pop(0)
            for src, dst, _ in self.edges:
                if dst == current and src not in visited:
                    visited.add(src)
                    affected.add(src)
                    queue.append(src)
            for src, dst, _ in self.edges:
                if src == current and dst not in visited:
                    visited.add(dst)
                    affected.add(dst)
                    queue.append(dst)
        return {
            "changed": changed_files,
            "affected": sorted(affected),
            "total_files": len(affected),
            "estimated_tokens": len(affected) * 400,
        }


def generate_manifest(root: Path, graph: DependencyGraph) -> str:
    lines = []
    lines.append("# CONTEXT_MANIFEST.md")
    lines.append(f"# Generated: {datetime.now().isoformat()}")
    lines.append(f"# Project: {root.name}")
    lines.append(f"# Files Indexed: {len(graph.nodes)}")
    lines.append(f"# Dependencies Mapped: {len(graph.edges)}")
    lines.append("")
    lines.append("## Project Overview")
    lines.append(f"- **Root:** `{root}`")
    lines.append(f"- **Total Files:** {len(graph.nodes)}")
    lines.append(f"- **Total Edges:** {len(graph.edges)}")
    lines.append("")

    lang_counts = {}
    for node in graph.nodes.values():
        lang = node["language"]
        lang_counts[lang] = lang_counts.get(lang, 0) + 1

    lines.append("## Language Breakdown")
    for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {lang}: {count} files")
    lines.append("")

    import_counts = {}
    for _, dst, _ in graph.edges:
        import_counts[dst] = import_counts.get(dst, 0) + 1

    lines.append("## High-Impact Files (Most Referenced)")
    for path, count in sorted(import_counts.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"- `{path}` — referenced by {count} files")
    lines.append("")

    lines.append("## Directory Structure")
    dirs = set()
    for path in graph.nodes:
        p = Path(path)
        dirs.add(str(p.parent))
    for d in sorted(dirs):
        lines.append(f"- `{d}/`")
    lines.append("")

    lines.append("## File Registry")
    lines.append("<!-- Use blast-radius queries to fetch only affected files -->")
    lines.append("")
    for path in sorted(graph.nodes):
        node = graph.nodes[path]
        lines.append(f"### `{path}`")
        lines.append(f"- **Language:** {node['language']}")
        lines.append(f"- **Lines:** {node['lines']}")
        lines.append(f"- **Size:** {node['size']} bytes")
        if node["imports"]:
            lines.append(f"- **Imports:** {', '.join(node['imports'][:5])}")
        lines.append("- **Preview:**")
        lines.append("```" + node["language"])
        lines.append(node["preview"])
        lines.append("```")
        lines.append("")

    lines.append("## Dependency Graph")
    lines.append("```")
    for src, dst, typ in graph.edges[:200]:
        lines.append(f"{src} --[{typ}]--> {dst}")
    if len(graph.edges) > 200:
        lines.append(f"... ({len(graph.edges) - 200} more edges)")
    lines.append("```")
    lines.append("")

    lines.append("## Blast Radius Query Template")
    lines.append("To find affected files for a change, run:")
    lines.append("```bash")
    lines.append("python tools/context_mapper.py /path/to/project --blast-radius file1.py,file2.py")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python context_mapper.py <project_root> [--blast-radius file1,file2,...]")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.exists():
        print(f"Error: {root} does not exist")
        sys.exit(1)

    print(f"[context-mapper] Scanning {root} ...")
    graph = DependencyGraph(root)
    graph.scan()
    print(f"[context-mapper] Indexed {len(graph.nodes)} files, {len(graph.edges)} edges")

    if "--blast-radius" in sys.argv:
        idx = sys.argv.index("--blast-radius")
        if idx + 1 < len(sys.argv):
            changed = sys.argv[idx + 1].split(",")
            result = graph.get_blast_radius(changed)
            print("\n--- Blast Radius ---")
            print(json.dumps(result, indent=2))
            return

    manifest = generate_manifest(root, graph)
    manifest_path = root / "CONTEXT_MANIFEST.md"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest)
    print(f"[context-mapper] Manifest written to {manifest_path}")

    graph_path = root / ".claude" / "graph.json"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump({"nodes": graph.nodes, "edges": graph.edges}, f, indent=2, default=str)
    print(f"[context-mapper] Graph JSON written to {graph_path}")


if __name__ == "__main__":
    main()
