#!/usr/bin/env python3
"""
ParallelAI CLI - Main Entry Point
"""
import sys
import click
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from parallelai.commands.keys import keys
    from parallelai.commands.analyze import analyze
    from parallelai.commands.experiment import experiment
    from parallelai.commands.setup import setup
    HAS_COMMANDS = True
except ImportError as e:
    HAS_COMMANDS = False
    print(f"⚠️  Command modules not loaded: {e}")

@click.group()
@click.version_option(version='1.0.0', prog_name='ParallelAI')
def cli():
    """🔬 ParallelAI - Multi-LLM Security Analysis Framework
    
    A comprehensive tool for AI security research and analysis
    using multiple LLM providers with academic methodology.
    """
    pass

# Add commands if available
if HAS_COMMANDS:
    cli.add_command(keys)
    cli.add_command(analyze)
    cli.add_command(experiment)
    cli.add_command(setup)
else:
    @cli.command()
    def setup():
        """Install and configure ParallelAI"""
        click.echo("Installing ParallelAI...")
        # This will be implemented

@cli.command()
def status():
    """Check ParallelAI system status"""
    from parallelai.utils.system import check_system_status
    check_system_status()

@cli.command()
def doctor():
    """Diagnose and fix common issues"""
    from parallelai.utils.system import run_diagnosis
    run_diagnosis()

if __name__ == '__main__':
    cli()
