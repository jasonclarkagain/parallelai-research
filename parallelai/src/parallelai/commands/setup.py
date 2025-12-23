"""
Setup and installation commands
"""
import os
import sys
import subprocess
import click
from pathlib import Path

@click.group()
def setup():
    """Setup and installation commands"""
    pass

@setup.command()
def install():
    """Install ParallelAI system"""
    click.echo("🚀 Installing ParallelAI...")
    
    # 1. Check Python
    click.echo("🔍 Checking Python version...")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        click.echo(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        click.echo("❌ Python 3.8+ required")
        return
    
    # 2. Install dependencies
    click.echo("📦 Installing dependencies...")
    try:
        requirements = Path(__file__).parent.parent.parent / 'requirements.txt'
        if requirements.exists():
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(requirements)])
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                                 'click', 'requests', 'python-dotenv', 'colorama'])
        click.echo("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to install dependencies: {e}")
        return
    
    # 3. Create config directory
    config_dir = Path.home() / '.parallelai'
    config_dir.mkdir(exist_ok=True)
    click.echo(f"📁 Created config directory: {config_dir}")
    
    # 4. Make executable
    try:
        # Find the main CLI script
        cli_script = Path(__file__).parent.parent / 'cli' / 'main.py'
        if cli_script.exists():
            # Create symlink or executable wrapper
            bin_dir = Path.home() / '.local' / 'bin'
            bin_dir.mkdir(parents=True, exist_ok=True)
            
            # Create executable script
            executable = bin_dir / 'parallelai'
            with open(executable, 'w') as f:
                f.write(f'''#!/usr/bin/env python3
import sys
sys.path.insert(0, '{Path(__file__).parent.parent.parent}')
from parallelai.cli.main import cli

if __name__ == '__main__':
    cli()
''')
            executable.chmod(0o755)
            click.echo(f"✅ Created executable: {executable}")
    except Exception as e:
        click.echo(f"⚠️  Could not create executable: {e}")
    
    click.echo("\n🎉 Installation complete!")
    click.echo("\n📋 Next steps:")
    click.echo("   1. Setup API keys: parallelai keys setup")
    click.echo("   2. Test: parallelai keys test")
    click.echo("   3. Get help: parallelai --help")

@setup.command()
def doctor():
    """Diagnose installation issues"""
    click.echo("🩺 Running ParallelAI Doctor...")
    click.echo("=" * 50)
    
    issues = []
    
    # Check Python
    python_version = sys.version_info
    if not (python_version.major == 3 and python_version.minor >= 8):
        issues.append(f"Python version {python_version.major}.{python_version.minor} < 3.8")
    
    # Check dependencies
    try:
        import click
        import requests
        click.echo("✅ Dependencies: click, requests")
    except ImportError as e:
        issues.append(f"Missing dependency: {e}")
    
    # Check config directory
    config_dir = Path.home() / '.parallelai'
    if not config_dir.exists():
        issues.append(f"Config directory missing: {config_dir}")
    else:
        click.echo(f"✅ Config directory: {config_dir}")
    
    # Check executable
    bin_dirs = ['/usr/local/bin', '/usr/bin', str(Path.home() / '.local' / 'bin')]
    found = False
    for bin_dir in bin_dirs:
        if Path(bin_dir).exists() and (Path(bin_dir) / 'parallelai').exists():
            click.echo(f"✅ Executable found in: {bin_dir}")
            found = True
            break
    
    if not found:
        issues.append("Executable 'parallelai' not found in PATH")
    
    # Report issues
    if issues:
        click.echo("\n❌ Found issues:")
        for issue in issues:
            click.echo(f"   • {issue}")
        click.echo("\n💡 Run 'parallelai setup install' to fix")
    else:
        click.echo("\n✅ All checks passed!")

@setup.command()
@click.option('--upgrade/--no-upgrade', default=True, help='Upgrade existing installation')
def update(upgrade):
    """Update ParallelAI to latest version"""
    click.echo("🔄 Updating ParallelAI...")
    
    try:
        # Update from git if this is a git repo
        repo_dir = Path(__file__).parent.parent.parent.parent
        if (repo_dir / '.git').exists():
            click.echo("📥 Pulling latest changes from git...")
            subprocess.check_call(['git', 'pull'], cwd=repo_dir)
        
        # Reinstall
        click.echo("📦 Reinstalling...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'])
        
        click.echo("✅ Update complete!")
    except Exception as e:
        click.echo(f"❌ Update failed: {e}")
