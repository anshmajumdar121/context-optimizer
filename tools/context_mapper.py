#!/usr/bin/env python3
"""
Context Mapper - Generate structural manifests for Claude AI

Zero-dependency Python script that indexes your codebase and generates
a compressed structural manifest (CONTEXT_MANIFEST.md) for use with
Claude's Context Optimizer skill.

Usage:
    python context_mapper.py /path/to/project
    python context_mapper.py /path/to/project --output custom_manifest.md
    python context_mapper.py /path/to/project --extensions .py,.js,.ts

Features:
    - Indexes 15+ programming languages
    - Extracts function/class definitions and line numbers
    - Generates compressed manifest (5-15KB for 10K+ files)
    - Zero external dependencies (Python 3.8+)
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Configuration - Edit these to customize behavior
INDEX_EXTENSIONS = {
    ".py",      # Python
    ".js",      # JavaScript
    ".ts",      # TypeScript
    ".jsx",     # React JavaScript
    ".tsx",     # React TypeScript
    ".rs",      # Rust
    ".go",      # Go
    ".java",    # Java
    ".kt",      # Kotlin
    ".c",       # C
    ".cpp",     # C++
    ".h",       # C/C++ headers
    ".hpp",     # C++ headers
    ".rb",      # Ruby
    ".php",     # PHP
    ".swift",   # Swift
    ".scala",   # Scala
    ".r",       # R
    ".m",       # Objective-C
    ".cs",      # C#
}

SKIP_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    "target",  # Rust
    ".idea",
    ".vscode",
    "*.egg-info",
}

# Language-specific keywords to detect
KEYWORDS = {
    ".py": ["def ", "class ", "async def "],
    ".js": ["function ", "const ", "let ", "var ", "class "],
    ".ts": ["function ", "const ", "let ", "var ", "class ", "interface ", "type "],
    ".jsx": ["function ", "const ", "let ", "var ", "class "],
    ".tsx": ["function ", "const ", "let ", "var ", "class ", "interface ", "type "],
    ".rs": ["fn ", "impl ", "struct ", "trait ", "enum ", "mod "],
    ".go": ["func ", "type ", "interface ", "struct "],
    ".java": ["public ", "private ", "protected ", "class ", "interface ", "enum "],
    ".kt": ["fun ", "class ", "interface ", "object ", "data class "],
    ".c": ["void ", "int ", "char ", "float ", "double ", "struct "],
    ".cpp": ["void ", "int ", "char ", "class ", "struct ", "namespace "],
    ".h": ["void ", "int ", "char ", "class ", "struct "],
    ".hpp": ["void ", "int ", "char ", "class ", "struct ", "namespace "],
    ".rb": ["def ", "class ", "module "],
    ".php": ["function ", "class ", "public ", "private ", "protected "],
    ".swift": ["func ", "class ", "struct ", "enum ", "protocol "],
    ".scala": ["def ", "class ", "object ", "trait "],
    ".r": ["function ", "<- function"],
    ".m": ["void ", "int ", "char ", "float ", "double ", "@interface "],
    ".cs": ["void ", "int ", "string ", "public ", "private ", "class ", "interface "],
}


def should_skip_dir(dirname):
    """Check if directory should be skipped."""
    return dirname in SKIP_DIRS or dirname.startswith(".")


def should_index_file(filename):
    """Check if file should be indexed based on extension."""
    return any(filename.endswith(ext) for ext in INDEX_EXTENSIONS)


def get_keywords(filepath):
    """Get keywords for a specific file extension."""
    ext = Path(filepath).suffix.lower()
    return KEYWORDS.get(ext, [])


def extract_structure(filepath, project_root):
    """Extract structural information from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return None

    keywords = get_keywords(filepath)
    if not keywords:
        return None

    structure = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Check if line starts with any keyword
        if any(stripped.startswith(kw) for kw in keywords):
            # Extract just the definition line (truncate if too long)
            definition = stripped[:80] + "..." if len(stripped) > 80 else stripped
            structure.append((i, definition))

    return structure


def generate_manifest(project_path, output_path="CONTEXT_MANIFEST.md"):
    """Generate the manifest file."""
    project_path = Path(project_path).resolve()
    
    if not project_path.exists():
        print(f"Error: Path '{project_path}' does not exist.")
        sys.exit(1)
    
    if not project_path.is_dir():
        print(f"Error: Path '{project_path}' is not a directory.")
        sys.exit(1)

    manifest_lines = [
        "# Context Manifest",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"Project: {project_path.name}",
        f"Root: {project_path}",
        "",
        "## Usage",
        "",
        "1. Upload this file to a Claude Project (or paste into chat)",
        "2. Use the one-click prompt from the Context Optimizer repo",
        "3. Claude will request specific files/lines as needed",
        "",
        "---",
        "",
    ]

    file_count = 0
    total_symbols = 0

    # Walk the directory tree
    for root, dirs, files in os.walk(project_path):
        # Skip directories
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        
        for filename in files:
            if not should_index_file(filename):
                continue

            filepath = Path(root) / filename
            rel_path = filepath.relative_to(project_path)
            
            structure = extract_structure(filepath, project_path)
            if not structure:
                continue

            file_count += 1
            manifest_lines.append(f"📄 {rel_path}")
            
            for line_num, definition in structure:
                total_symbols += 1
                manifest_lines.append(f"L{line_num}: {definition}")
            
            manifest_lines.append("")  # Empty line between files

    # Add footer with stats
    manifest_lines.extend([
        "---",
        "",
        "## Statistics",
        "",
        f"- Files indexed: {file_count}",
        f"- Symbols found: {total_symbols}",
        f"- Manifest size: ~{sum(len(line) for line in manifest_lines) // 1024}KB",
        "",
        "*Generated by Context Optimizer*",
    ])

    # Write manifest
    output_file = Path(output_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(manifest_lines))

    print(f"✅ Manifest generated: {output_file}")
    print(f"   Files indexed: {file_count}")
    print(f"   Symbols found: {total_symbols}")
    print(f"   Size: ~{sum(len(line) for line in manifest_lines) // 1024}KB")
    print("")
    print("Next steps:")
    print("1. Upload this file to a Claude Project")
    print("2. Paste the one-click prompt from the Context Optimizer repo")
    print("3. Start chatting with optimized token usage!")


def main():
    parser = argparse.ArgumentParser(
        description="Generate structural manifest for Claude AI Context Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/project
  %(prog)s /path/to/project --output my_manifest.md
  %(prog)s /path/to/project --extensions .py,.js
        """
    )
    
    parser.add_argument(
        "project_path",
        help="Path to the project directory to index"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="CONTEXT_MANIFEST.md",
        help="Output file path (default: CONTEXT_MANIFEST.md)"
    )
    
    parser.add_argument(
        "-e", "--extensions",
        help="Comma-separated list of extensions to index (e.g., .py,.js,.ts)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be indexed without creating the file"
    )

    args = parser.parse_args()

    # Override extensions if provided
    global INDEX_EXTENSIONS
    if args.extensions:
        INDEX_EXTENSIONS = set(ext.strip() for ext in args.extensions.split(","))
        print(f"Using custom extensions: {INDEX_EXTENSIONS}")

    if args.dry_run:
        print("Dry run mode - would index:")
        project_path = Path(args.project_path).resolve()
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not should_skip_dir(d)]
            for filename in files:
                if should_index_file(filename):
                    print(f"  {Path(root) / filename}")
        return

    generate_manifest(args.project_path, args.output)


if __name__ == "__main__":
    main()
