#!/usr/bin/env python3
"""
Project Analyzer for CLAUDE.md Generation

Analyzes an existing project directory to extract:
- Tech stack (from package.json, pyproject.toml, etc.)
- Directory structure
- Available commands
- Project type classification

Usage:
    python analyze_project.py /path/to/project
    python analyze_project.py .
    python analyze_project.py . --json
"""

import json
import sys
from pathlib import Path
from typing import Any


def analyze_package_json(path: Path) -> dict[str, Any]:
    """Extract info from package.json."""
    pkg_path = path / "package.json"
    if not pkg_path.exists():
        return {}

    try:
        with open(pkg_path) as f:
            pkg = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

    result = {
        "name": pkg.get("name", ""),
        "type": "node",
        "scripts": pkg.get("scripts", {}),
        "dependencies": {},
        "devDependencies": {},
    }

    # Check for workspaces (monorepo)
    if "workspaces" in pkg:
        result["workspaces"] = True

    # Extract key dependencies
    deps = pkg.get("dependencies", {})
    dev_deps = pkg.get("devDependencies", {})

    # Frameworks
    frameworks = {
        "next": "Next.js",
        "react": "React",
        "vue": "Vue",
        "svelte": "Svelte",
        "@sveltejs/kit": "SvelteKit",
        "nuxt": "Nuxt",
        "express": "Express",
        "fastify": "Fastify",
        "hono": "Hono",
        "astro": "Astro",
    }

    for dep, name in frameworks.items():
        if dep in deps or dep in dev_deps:
            result["dependencies"][dep] = name

    # ORMs / Database
    db_tools = {
        "prisma": "Prisma",
        "@prisma/client": "Prisma",
        "drizzle-orm": "Drizzle",
        "typeorm": "TypeORM",
        "mongoose": "Mongoose",
        "pg": "PostgreSQL (pg)",
    }

    for dep, name in db_tools.items():
        if dep in deps or dep in dev_deps:
            result["dependencies"][dep] = name

    # Styling
    styling = {
        "tailwindcss": "Tailwind CSS",
        "styled-components": "styled-components",
        "@emotion/react": "Emotion",
    }

    for dep, name in styling.items():
        if dep in deps or dep in dev_deps:
            result["dependencies"][dep] = name

    # Testing
    testing = {
        "vitest": "Vitest",
        "jest": "Jest",
        "playwright": "Playwright",
        "cypress": "Cypress",
    }

    for dep, name in testing.items():
        if dep in deps or dep in dev_deps:
            result["devDependencies"][dep] = name

    # TypeScript
    if "typescript" in dev_deps or "typescript" in deps:
        result["language"] = "TypeScript"
    else:
        result["language"] = "JavaScript"

    return result


def analyze_pyproject(path: Path) -> dict[str, Any]:
    """Extract info from pyproject.toml."""
    pyproject_path = path / "pyproject.toml"
    if not pyproject_path.exists():
        return {}

    try:
        content = pyproject_path.read_text()
    except IOError:
        return {}

    result = {
        "type": "python",
        "language": "Python",
        "dependencies": {},
        "devDependencies": {},
    }

    # Check for common frameworks
    frameworks = {
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "starlette": "Starlette",
        "litestar": "Litestar",
    }

    for dep, name in frameworks.items():
        if dep in content.lower():
            result["dependencies"][dep] = name

    # ORMs
    orms = {
        "sqlalchemy": "SQLAlchemy",
        "prisma": "Prisma",
        "tortoise-orm": "Tortoise ORM",
        "sqlmodel": "SQLModel",
    }

    for dep, name in orms.items():
        if dep in content.lower():
            result["dependencies"][dep] = name

    # CLI
    cli_tools = {
        "typer": "Typer",
        "click": "Click",
        "argparse": "argparse",
    }

    for dep, name in cli_tools.items():
        if dep in content.lower():
            result["dependencies"][dep] = name

    # Testing
    if "pytest" in content.lower():
        result["devDependencies"]["pytest"] = "pytest"

    return result


def analyze_cargo_toml(path: Path) -> dict[str, Any]:
    """Extract info from Cargo.toml."""
    cargo_path = path / "Cargo.toml"
    if not cargo_path.exists():
        return {}

    try:
        content = cargo_path.read_text()
    except IOError:
        return {}

    result = {
        "type": "rust",
        "language": "Rust",
        "dependencies": {},
        "devDependencies": {},
    }

    # Common Rust dependencies
    deps = {
        "axum": "Axum",
        "actix-web": "Actix Web",
        "rocket": "Rocket",
        "tokio": "Tokio",
        "clap": "Clap (CLI)",
        "serde": "Serde",
        "sqlx": "SQLx",
        "diesel": "Diesel",
    }

    for dep, name in deps.items():
        if dep in content.lower():
            result["dependencies"][dep] = name

    return result


def analyze_go_mod(path: Path) -> dict[str, Any]:
    """Extract info from go.mod."""
    go_mod_path = path / "go.mod"
    if not go_mod_path.exists():
        return {}

    try:
        content = go_mod_path.read_text()
    except IOError:
        return {}

    result = {
        "type": "go",
        "language": "Go",
        "dependencies": {},
        "devDependencies": {},
    }

    # Common Go dependencies
    deps = {
        "gin-gonic/gin": "Gin",
        "gofiber/fiber": "Fiber",
        "labstack/echo": "Echo",
        "gorilla/mux": "Gorilla Mux",
        "go-gorm/gorm": "GORM",
        "spf13/cobra": "Cobra (CLI)",
    }

    for dep, name in deps.items():
        if dep in content:
            result["dependencies"][dep] = name

    return result


def analyze_directory_structure(path: Path) -> dict[str, str]:
    """Analyze directory structure to identify patterns."""
    structure = {}

    # Common directories and their meanings
    patterns = {
        "src": "Source code",
        "app": "Application code (Next.js App Router or similar)",
        "pages": "Page components (Next.js Pages Router or similar)",
        "components": "UI components",
        "lib": "Library/utility code",
        "utils": "Utility functions",
        "hooks": "Custom hooks",
        "api": "API routes/handlers",
        "server": "Server-side code",
        "services": "Business logic services",
        "models": "Data models",
        "schemas": "Validation schemas",
        "types": "Type definitions",
        "tests": "Test files",
        "__tests__": "Test files",
        "test": "Test files",
        "docs": "Documentation",
        "public": "Static assets",
        "static": "Static assets",
        "assets": "Asset files",
        "styles": "Stylesheets",
        "prisma": "Prisma schema and migrations",
        "migrations": "Database migrations",
        "scripts": "Utility scripts",
        "bin": "Executable scripts",
        "cmd": "Command entry points (Go)",
        "internal": "Internal packages (Go)",
        "pkg": "Public packages (Go)",
        "packages": "Monorepo packages",
        "apps": "Monorepo applications",
    }

    ignore_dirs = {
        "node_modules",
        "__pycache__",
        ".pycache",
        "dist",
        "build",
        ".next",
        ".git",
        ".venv",
        "venv",
        "target",
        ".turbo",
        ".cache",
    }

    for item in path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            name = item.name
            if name in ignore_dirs:
                continue
            if name in patterns:
                structure[name] = patterns[name]
            else:
                structure[name] = "Project directory"

    return structure


def classify_project_type(analysis: dict[str, Any]) -> str:
    """Classify the project type based on analysis."""
    deps = analysis.get("dependencies", {})
    dev_deps = analysis.get("devDependencies", {})
    all_deps = {**deps, **dev_deps}
    all_deps_str = str(all_deps).lower()

    # Check for monorepo indicators
    if analysis.get("workspaces"):
        return "monorepo"

    structure = analysis.get("structure", {})
    if "packages" in structure or "apps" in structure:
        return "monorepo"

    # Check for CLI indicators
    cli_indicators = ["clap", "cobra", "typer", "commander", "yargs"]
    if any(ind in all_deps_str for ind in cli_indicators):
        return "cli"

    # Check for library indicators
    if analysis.get("name", "").startswith("@") or "lib" in analysis.get("name", ""):
        # Could be a library, check for no framework
        frontend = ["next", "react", "vue", "svelte", "astro", "nuxt"]
        backend = ["express", "fastify", "fastapi", "django", "flask", "gin", "axum"]
        if not any(fw in all_deps_str for fw in frontend + backend):
            return "library"

    # Check for frontend frameworks
    frontend = ["next", "react", "vue", "svelte", "astro", "nuxt"]
    has_frontend = any(fw in all_deps_str for fw in frontend)

    # Check for backend frameworks
    backend = ["express", "fastify", "fastapi", "django", "flask", "gin", "axum", "actix", "hono"]
    has_backend = any(bw in all_deps_str for bw in backend)

    # Check for database/ORM
    has_db = any(
        db in all_deps_str
        for db in ["prisma", "drizzle", "typeorm", "sqlalchemy", "gorm", "mongoose", "sqlx"]
    )

    if has_frontend and (has_backend or has_db):
        return "fullstack"
    elif has_frontend:
        return "web-frontend"
    elif has_backend or has_db:
        return "web-backend"

    return "minimal"


def analyze_project(project_path: str) -> dict[str, Any]:
    """Main analysis function."""
    path = Path(project_path).resolve()

    if not path.exists():
        return {"error": f"Path does not exist: {path}"}

    if not path.is_dir():
        return {"error": f"Path is not a directory: {path}"}

    result = {
        "path": str(path),
        "name": path.name,
        "type": "unknown",
        "language": "unknown",
        "dependencies": {},
        "devDependencies": {},
        "scripts": {},
        "structure": {},
    }

    # Try different project types
    pkg_analysis = analyze_package_json(path)
    if pkg_analysis:
        result.update(pkg_analysis)

    py_analysis = analyze_pyproject(path)
    if py_analysis and result["type"] == "unknown":
        result.update(py_analysis)
    elif py_analysis:
        # Merge Python info if we have both (e.g., Node + Python in same repo)
        result["dependencies"].update(py_analysis.get("dependencies", {}))

    cargo_analysis = analyze_cargo_toml(path)
    if cargo_analysis and result["type"] == "unknown":
        result.update(cargo_analysis)

    go_analysis = analyze_go_mod(path)
    if go_analysis and result["type"] == "unknown":
        result.update(go_analysis)

    # Analyze directory structure
    result["structure"] = analyze_directory_structure(path)

    # Classify project type
    result["project_type"] = classify_project_type(result)

    return result


def format_output(analysis: dict[str, Any]) -> str:
    """Format analysis results for display."""
    lines = [
        "=" * 60,
        f"Project Analysis: {analysis.get('name', 'Unknown')}",
        "=" * 60,
        "",
        f"📁 Path: {analysis.get('path')}",
        f"🔤 Language: {analysis.get('language', 'Unknown')}",
        f"📦 Project Type: {analysis.get('project_type', 'Unknown')}",
        "",
    ]

    deps = analysis.get("dependencies", {})
    if deps:
        lines.append("📚 Key Dependencies:")
        for dep, name in deps.items():
            lines.append(f"   • {name}")
        lines.append("")

    dev_deps = analysis.get("devDependencies", {})
    if dev_deps:
        lines.append("🔧 Dev Tools:")
        for dep, name in dev_deps.items():
            lines.append(f"   • {name}")
        lines.append("")

    scripts = analysis.get("scripts", {})
    if scripts:
        lines.append("⚡ Available Scripts:")
        for script, cmd in list(scripts.items())[:10]:
            cmd_display = cmd[:40] + "..." if len(cmd) > 40 else cmd
            lines.append(f"   • {script}: {cmd_display}")
        if len(scripts) > 10:
            lines.append(f"   ... and {len(scripts) - 10} more")
        lines.append("")

    structure = analysis.get("structure", {})
    if structure:
        lines.append("📂 Directory Structure:")
        for dir_name, purpose in sorted(structure.items()):
            lines.append(f"   • {dir_name}/ - {purpose}")
        lines.append("")

    lines.append("=" * 60)
    lines.append(f"✨ Suggested template: {analysis.get('project_type', 'minimal')}.md")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_project.py <path> [--json]")
        print("")
        print("Examples:")
        print("  python analyze_project.py .")
        print("  python analyze_project.py /path/to/project")
        print("  python analyze_project.py . --json")
        sys.exit(1)

    project_path = sys.argv[1]

    print(f"🔍 Analyzing project: {project_path}")
    print()

    analysis = analyze_project(project_path)

    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        sys.exit(1)

    print(format_output(analysis))

    # Also output JSON for programmatic use
    if "--json" in sys.argv:
        print("\n--- JSON Output ---")
        print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
