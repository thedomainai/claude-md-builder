#!/usr/bin/env python3
"""
CLAUDE.md Validator

Validates a CLAUDE.md file for:
- Required sections present
- Reasonable line count
- Common issues and anti-patterns

Usage:
    python validate_claude_md.py /path/to/CLAUDE.md
    python validate_claude_md.py .  # Looks for CLAUDE.md in current dir
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


def find_claude_md(path_arg: str) -> Optional[Path]:
    """Find CLAUDE.md file from path argument."""
    path = Path(path_arg)
    
    if path.is_file() and path.name.upper() == "CLAUDE.MD":
        return path
    
    if path.is_dir():
        # Check for CLAUDE.md in directory
        claude_md = path / "CLAUDE.md"
        if claude_md.exists():
            return claude_md
        # Also check lowercase
        claude_md_lower = path / "claude.md"
        if claude_md_lower.exists():
            return claude_md_lower
    
    return None


def count_lines(content: str) -> int:
    """Count non-empty lines."""
    return len([line for line in content.split("\n") if line.strip()])


def extract_sections(content: str) -> dict[str, str]:
    """Extract sections from markdown content."""
    sections = {}
    current_section = "preamble"
    current_content = []
    
    for line in content.split("\n"):
        # Check for h1 or h2 headers
        h1_match = re.match(r"^#\s+(.+)$", line)
        h2_match = re.match(r"^##\s+(.+)$", line)
        
        if h1_match or h2_match:
            # Save previous section
            if current_content:
                sections[current_section.lower()] = "\n".join(current_content)
            
            # Start new section
            current_section = (h1_match or h2_match).group(1).strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section.lower()] = "\n".join(current_content)
    
    return sections


def validate_required_sections(sections: dict[str, str]) -> list[ValidationResult]:
    """Check for required sections."""
    results = []
    
    # Required sections (case-insensitive)
    required = {
        "project": "Project identity/description",
        "tech stack": "Technology stack",
        "commands": "Available commands",
    }
    
    # Alternative names for sections
    alternatives = {
        "project": ["project", "overview", "about"],
        "tech stack": ["tech stack", "stack", "technology", "technologies"],
        "commands": ["commands", "scripts", "development"],
    }
    
    section_keys = list(sections.keys())
    
    for section, description in required.items():
        found = False
        for alt in alternatives.get(section, [section]):
            if any(alt in key for key in section_keys):
                found = True
                break
        
        if found:
            results.append(ValidationResult(
                passed=True,
                message=f"✓ Found {section} section",
                severity="info"
            ))
        else:
            results.append(ValidationResult(
                passed=False,
                message=f"✗ Missing {section} section ({description})",
                severity="error"
            ))
    
    return results


def validate_recommended_sections(sections: dict[str, str]) -> list[ValidationResult]:
    """Check for recommended sections."""
    results = []
    
    recommended = {
        "structure": "Directory structure helps Claude navigate",
        "principles": "Principles help Claude make decisions",
        "boundaries": "Boundaries prevent unwanted actions",
    }
    
    alternatives = {
        "structure": ["structure", "directory", "directories", "layout"],
        "principles": ["principles", "guidelines", "conventions"],
        "boundaries": ["boundaries", "constraints", "rules", "restrictions"],
    }
    
    section_keys = list(sections.keys())
    
    for section, description in recommended.items():
        found = False
        for alt in alternatives.get(section, [section]):
            if any(alt in key for key in section_keys):
                found = True
                break
        
        if not found:
            results.append(ValidationResult(
                passed=True,  # Recommended, not required
                message=f"⚠ Consider adding {section} section - {description}",
                severity="warning"
            ))
    
    return results


def validate_line_count(content: str) -> list[ValidationResult]:
    """Check line count is reasonable."""
    results = []
    line_count = count_lines(content)
    
    if line_count < 10:
        results.append(ValidationResult(
            passed=True,
            message=f"⚠ Very short ({line_count} lines) - consider adding more context",
            severity="warning"
        ))
    elif line_count <= 100:
        results.append(ValidationResult(
            passed=True,
            message=f"✓ Good length ({line_count} lines)",
            severity="info"
        ))
    elif line_count <= 200:
        results.append(ValidationResult(
            passed=True,
            message=f"⚠ Getting long ({line_count} lines) - consider moving details to docs/",
            severity="warning"
        ))
    else:
        results.append(ValidationResult(
            passed=False,
            message=f"✗ Too long ({line_count} lines) - Claude reads this fully every time. Move details to referenced docs.",
            severity="error"
        ))
    
    return results


def validate_content_patterns(content: str) -> list[ValidationResult]:
    """Check for common issues and anti-patterns."""
    results = []
    
    # Check for overly generic descriptions
    generic_patterns = [
        (r"^#\s*Project\s*$", "Project section has no description"),
        (r"A\s+(?:web\s+)?(?:application|app|project)\s*[.\n]", "Description is too generic"),
    ]
    
    for pattern, message in generic_patterns:
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            results.append(ValidationResult(
                passed=True,
                message=f"⚠ {message}",
                severity="warning"
            ))
    
    # Check for potentially sensitive content
    sensitive_patterns = [
        (r"(?:password|secret|api[_-]?key|token)\s*[:=]\s*['\"]?\w+", "Possible secret in file"),
        (r"sk-[a-zA-Z0-9]{20,}", "Possible API key in file"),
    ]
    
    for pattern, message in sensitive_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            results.append(ValidationResult(
                passed=False,
                message=f"✗ {message} - remove sensitive data",
                severity="error"
            ))
    
    # Check for good practices
    if "NEVER" in content.upper() or "ASK FIRST" in content.upper():
        results.append(ValidationResult(
            passed=True,
            message="✓ Has explicit boundaries defined",
            severity="info"
        ))
    else:
        results.append(ValidationResult(
            passed=True,
            message="⚠ Consider adding NEVER/ASK FIRST boundaries",
            severity="warning"
        ))
    
    # Check for code blocks (commands section)
    if "```" in content:
        results.append(ValidationResult(
            passed=True,
            message="✓ Has code blocks (good for commands)",
            severity="info"
        ))
    
    return results


def validate_formatting(content: str) -> list[ValidationResult]:
    """Check markdown formatting."""
    results = []
    
    lines = content.split("\n")
    
    # Check for consistent header hierarchy
    h1_count = sum(1 for line in lines if re.match(r"^#\s+", line))
    h2_count = sum(1 for line in lines if re.match(r"^##\s+", line))
    
    if h1_count > 1:
        results.append(ValidationResult(
            passed=True,
            message="⚠ Multiple H1 headers - consider using single H1 for project name",
            severity="warning"
        ))
    
    if h2_count == 0 and len(content) > 500:
        results.append(ValidationResult(
            passed=True,
            message="⚠ No H2 sections - consider organizing with headers",
            severity="warning"
        ))
    
    return results


def validate_claude_md(file_path: Path) -> tuple[bool, list[ValidationResult]]:
    """Run all validations on a CLAUDE.md file."""
    try:
        content = file_path.read_text()
    except IOError as e:
        return False, [ValidationResult(
            passed=False,
            message=f"Could not read file: {e}",
            severity="error"
        )]
    
    results = []
    
    # Extract sections for section-based checks
    sections = extract_sections(content)
    
    # Run all validations
    results.extend(validate_line_count(content))
    results.extend(validate_required_sections(sections))
    results.extend(validate_recommended_sections(sections))
    results.extend(validate_content_patterns(content))
    results.extend(validate_formatting(content))
    
    # Determine overall pass/fail
    has_errors = any(r.severity == "error" and not r.passed for r in results)
    
    return not has_errors, results


def format_results(results: list[ValidationResult]) -> str:
    """Format validation results for display."""
    lines = []
    
    errors = [r for r in results if r.severity == "error" and not r.passed]
    warnings = [r for r in results if r.severity == "warning"]
    info = [r for r in results if r.severity == "info" and r.passed]
    
    if info:
        lines.append("📋 Status:")
        for r in info:
            lines.append(f"   {r.message}")
        lines.append("")
    
    if warnings:
        lines.append("⚠️  Warnings:")
        for r in warnings:
            lines.append(f"   {r.message}")
        lines.append("")
    
    if errors:
        lines.append("❌ Errors:")
        for r in errors:
            lines.append(f"   {r.message}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_claude_md.py <path>")
        print("")
        print("Examples:")
        print("  python validate_claude_md.py CLAUDE.md")
        print("  python validate_claude_md.py .")
        print("  python validate_claude_md.py /path/to/project")
        sys.exit(1)
    
    path_arg = sys.argv[1]
    
    claude_md = find_claude_md(path_arg)
    
    if not claude_md:
        print(f"❌ Could not find CLAUDE.md at: {path_arg}")
        sys.exit(1)
    
    print("=" * 60)
    print(f"Validating: {claude_md}")
    print("=" * 60)
    print()
    
    passed, results = validate_claude_md(claude_md)
    
    print(format_results(results))
    
    print("=" * 60)
    if passed:
        print("✅ Validation PASSED")
    else:
        print("❌ Validation FAILED")
    print("=" * 60)
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
