import typer
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax

# Import internal modules
# Adjust imports based on package structure or relative imports
try:
    from . import analyzer
    from . import validator
except ImportError:
    # Fallback for running directly
    import analyzer
    import validator

app = typer.Typer(
    name="claude-builder",
    help="Generate optimized CLAUDE.md files for Claude Code projects",
    add_completion=False,
)
console = Console()


def get_resource_path() -> Path:
    """Get path to resources directory."""
    # Assuming resources is a sibling of this file's directory (src/claude_builder/resources)
    # or inside the package
    return Path(__file__).parent / "resources"


def load_template(template_name: str) -> str:
    """Load a template file."""
    # Handle variations (e.g. "web-frontend" vs "web-frontend.md")
    if not template_name.endswith(".md"):
        template_name += ".md"
    
    template_path = get_resource_path() / "templates" / template_name
    
    if not template_path.exists():
        # Fallback to minimal if not found
        console.print(f"[yellow]⚠ Template '{template_name}' not found. Falling back to 'minimal'.[/yellow]")
        template_path = get_resource_path() / "templates" / "minimal.md"
        
    return template_path.read_text()


def generate_tech_stack_section(analysis: dict) -> str:
    """Generate Tech Stack section from analysis."""
    lines = ["## Tech Stack", ""]
    
    # Language
    lang = analysis.get("language")
    if lang and lang != "unknown":
        lines.append(f"- Language: {lang}")
    
    # Dependencies
    deps = analysis.get("dependencies", {})
    if deps:
        # Group by category if possible (simplified for now)
        frameworks = []
        databases = []
        others = []
        
        for key, name in deps.items():
            key_lower = key.lower()
            if any(x in key_lower for x in ["react", "vue", "svelte", "next", "nuxt", "express", "fastify", "django", "flask", "fastapi"]):
                frameworks.append(name)
            elif any(x in key_lower for x in ["prisma", "typeorm", "mongoose", "sequelize", "sql", "mongo", "pg", "mysql"]):
                databases.append(name)
            else:
                others.append(name)
        
        if frameworks:
            lines.append(f"- Framework: {', '.join(frameworks)}")
        if databases:
            lines.append(f"- Database: {', '.join(databases)}")
        
        # Add other interesting deps
        relevant_others = [name for name in others if name not in ["Typer", "Clap", "Cobra"]] # filtering some common ones we handled in text
        if relevant_others:
            lines.append(f"- Key Libraries: {', '.join(relevant_others[:5])}")

    return "\n".join(lines)


def generate_commands_section(analysis: dict) -> str:
    """Generate Commands section from analysis."""
    scripts = analysis.get("scripts", {})
    if not scripts:
        return ""

    lines = ["## Commands", "", "```bash"]
    
    # Prioritize common commands
    priority = ["dev", "start", "test", "build", "lint", "format"]
    
    for cmd_name in priority:
        if cmd_name in scripts:
            lines.append(f"# {cmd_name.capitalize()}")
            lines.append(f"npm run {cmd_name}") # Assuming npm/node for scripts dict usually
            lines.append("")
            
    # Add others if list is short
    if len(lines) < 10:
        for cmd_name, cmd_val in scripts.items():
            if cmd_name not in priority:
                lines.append(f"# {cmd_name}")
                lines.append(f"npm run {cmd_name}")
                lines.append("")
                if len(lines) > 20: break
                
    lines.append("```")
    return "\n".join(lines)


@app.command()
def generate(
    path: str = typer.Argument(".", help="Project path to analyze"),
    template: str = typer.Option(None, "--template", "-t", help="Force specific template"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing CLAUDE.md"),
):
    """Analyze project and generate CLAUDE.md."""
    project_path = Path(path).resolve()
    
    if not project_path.exists():
        console.print(f"[red]Error: Path '{project_path}' does not exist.[/red]")
        raise typer.Exit(1)

    claude_md_path = project_path / "CLAUDE.md"
    if claude_md_path.exists() and not force:
        if not Confirm.ask(f"[yellow]CLAUDE.md already exists at {claude_md_path}. Overwrite?[/yellow]"):
            raise typer.Exit(0)

    # 1. Analyze
    with console.status("[bold green]Analyzing project...[/bold green]"):
        analysis = analyzer.analyze_project(str(project_path))
    
    if "error" in analysis:
        console.print(f"[red]Analysis failed: {analysis['error']}[/red]")
        raise typer.Exit(1)

    console.print(Panel(analyzer.format_output(analysis), title="Project Analysis", border_style="blue"))

    # 2. Select Template
    suggested_type = analysis.get("project_type", "minimal")
    selected_template_name = template if template else suggested_type
    
    console.print(f"Using template: [bold cyan]{selected_template_name}[/bold cyan]")
    
    # 3. Prompt for details
    project_name = analysis.get("name") or project_path.name
    description = Prompt.ask("Project Description (one line)", default=f"{project_name} project")
    
    # 4. Process Template
    raw_template = load_template(selected_template_name)
    
    # Simple processing:
    # - Replace # Project
    #
    # [Description] -> # Project
    #
    # {description}
    # - Replace tech stack if we have data?
    # For now, let's keep it simple: Use the template structure but inject what we know.
    
    # Better approach: Modify the raw template text using regex or string replacement
    # 1. Identity
    import re
    content = re.sub(
        r"# Project\s*\n\s*\[.*?\]", 
        f"# Project\n\n{description}", 
        raw_template, 
        count=1, 
        flags=re.DOTALL
    )
    
    # 2. Tech Stack (Optional: If we detected stuff, replace the placeholder section)
    # This is harder to do safely without parsing markdown. 
    # Let's trust the template defaults for now, but maybe append a comment with detected stack?
    # Or replace if it matches the placeholder pattern exactly.
    
    # For now, we write the file as is (with identity filled) and let user refine, 
    # OR we could try to inject.
    
    # Let's try to inject the detected commands if it's a Node project (since we have script parsing)
    if analysis.get("type") == "node" and analysis.get("scripts"):
        # Find ## Commands section
        commands_section = generate_commands_section(analysis)
        if commands_section:
            # Replace ## Commands until next ## or end
            # Regex to match ## Commands until next ## or end
            content = re.sub(
                r"## Commands\s*```.*?```",
                commands_section,
                content,
                flags=re.DOTALL
            )

    # Write file
    try:
        claude_md_path.write_text(content)
        console.print(f"[green]✓ Generated CLAUDE.md at {claude_md_path}[/green]")
    except IOError as e:
        console.print(f"[red]Error writing file: {e}[/red]")
        raise typer.Exit(1)

    # 5. Validate
    console.print("\n[bold]Validating generated file...[/bold]")
    passed, results = validator.validate_claude_md(claude_md_path)
    console.print(validator.format_results(results))
    
    if not passed:
        console.print("[yellow]⚠ Generated file has issues. Please review and edit manually.[/yellow]")
    else:
        console.print("[bold green]✨ Done! CLAUDE.md is ready.[/bold green]")


@app.command()
def validate(
    path: str = typer.Argument(".", help="Path to CLAUDE.md or project directory"),
):
    """Validate an existing CLAUDE.md file."""
    claude_md = validator.find_claude_md(path)
    
    if not claude_md:
        console.print(f"[red]Could not find CLAUDE.md at: {path}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold]Validating: {claude_md}[/bold]\n")
    
    passed, results = validator.validate_claude_md(claude_md)
    console.print(validator.format_results(results))
    
    if passed:
        console.print("[bold green]✅ Validation PASSED[/bold green]")
    else:
        console.print("[bold red]❌ Validation FAILED[/bold red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
