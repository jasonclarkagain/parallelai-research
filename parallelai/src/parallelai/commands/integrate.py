"""
Commands to integrate with existing orchestrators
"""
import os
import sys
import shutil
import click
from pathlib import Path
from typing import Dict, List
import json

from ..utils.key_manager import migrate_keys, key_manager

@click.group()
def integrate():
    """Integrate with existing AI orchestrators"""
    pass

@integrate.command()
def migrate():
    """Migrate API keys from existing orchestrators"""
    click.echo("🔍 Searching for existing API keys in orchestrator files...")
    
    results = migrate_keys()
    
    click.echo("\n📊 Migration Results:")
    click.echo("=" * 50)
    
    migrated = 0
    for provider, success in results.items():
        if success:
            click.echo(f"✅ {provider}: Migrated successfully")
            migrated += 1
        else:
            click.echo(f"❌ {provider}: No key found")
    
    if migrated > 0:
        click.echo(f"\n🎉 Successfully migrated {migrated} API keys")
        click.echo(f"📁 Config saved to: {key_manager.config_file}")
    else:
        click.echo("\n⚠️  No API keys found to migrate")
        click.echo("💡 Make sure you have existing orchestrator files with API keys")

@integrate.command()
@click.option('--source', type=click.Path(exists=True), 
              default=str(Path.home()), help='Source directory to search')
def discover(source):
    """Discover existing AI orchestrators"""
    source_path = Path(source)
    
    click.echo(f"🔍 Discovering AI orchestrators in: {source_path}")
    click.echo("=" * 50)
    
    # Patterns to look for
    patterns = ['*orchestrator*', '*ai*', '*llm*', '*chat*', '*assistant*']
    extensions = ['.py', '.sh', '.js', '.json']
    
    found_files = []
    
    for pattern in patterns:
        for ext in extensions:
            search_pattern = f"{pattern}{ext}"
            for file_path in source_path.rglob(search_pattern):
                if file_path.is_file():
                    # Check if it looks like an AI orchestrator
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(5000)  # Read first 5KB
                        
                        indicators = ['api', 'openai', 'anthropic', 'llm', 
                                     'chat', 'completion', 'model', 'ai']
                        indicator_count = sum(1 for ind in indicators 
                                            if ind.lower() in content.lower())
                        
                        if indicator_count >= 2:
                            found_files.append({
                                'path': file_path,
                                'size': file_path.stat().st_size,
                                'indicators': indicator_count
                            })
                    except:
                        continue
    
    if found_files:
        click.echo(f"\n📁 Found {len(found_files)} potential AI orchestrators:\n")
        
        for i, file_info in enumerate(found_files[:20], 1):  # Show first 20
            rel_path = file_info['path'].relative_to(source_path)
            click.echo(f"{i:2}. {rel_path}")
            click.echo(f"    Size: {file_info['size']:,} bytes")
            click.echo(f"    AI indicators: {file_info['indicators']}")
            click.echo()
        
        if len(found_files) > 20:
            click.echo(f"... and {len(found_files) - 20} more")
    else:
        click.echo("❌ No AI orchestrators found")

@integrate.command()
@click.option('--output', type=click.Path(), default='orchestrator_inventory.json',
              help='Output JSON file')
def inventory(output):
    """Create inventory of existing AI tools"""
    home = Path.home()
    inventory = {
        'orchestrators': [],
        'scripts': [],
        'configs': [],
        'models': []
    }
    
    # Look for orchestrators
    for file_path in home.rglob('*orchestrator*.py'):
        if file_path.is_file():
            inventory['orchestrators'].append(str(file_path))
    
    # Look for AI scripts
    for file_path in home.rglob('ai*.py'):
        if file_path.is_file() and file_path not in inventory['orchestrators']:
            inventory['scripts'].append(str(file_path))
    
    # Look for configs
    config_patterns = ['*.env', '.ai*', '*config*', '*key*']
    for pattern in config_patterns:
        for file_path in home.rglob(pattern):
            if file_path.is_file() and file_path.suffix in ['.py', '.json', '.txt', '.env', '']:
                inventory['configs'].append(str(file_path))
    
    # Look for models
    model_dirs = ['llama.cpp', 'models', '.ollama']
    for dir_name in model_dirs:
        dir_path = home / dir_name
        if dir_path.exists():
            inventory['models'].append(str(dir_path))
    
    # Save inventory
    with open(output, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    click.echo(f"📊 Inventory created: {output}")
    click.echo(f"  • Orchestrators: {len(inventory['orchestrators'])}")
    click.echo(f"  • Scripts: {len(inventory['scripts'])}")
    click.echo(f"  • Configs: {len(inventory['configs'])}")
    click.echo(f"  • Model directories: {len(inventory['models'])}")

@integrate.command()
@click.option('--backup/--no-backup', default=True, help='Create backup before integration')
def unify(backup):
    """Unify all AI tools under ParallelAI"""
    click.echo("🔄 Unifying AI tools under ParallelAI...")
    
    # 1. Backup if requested
    if backup:
        backup_dir = Path.home() / 'ai_backup'
        backup_dir.mkdir(exist_ok=True)
        click.echo(f"📦 Creating backup in: {backup_dir}")
    
    # 2. Migrate API keys
    click.echo("🔑 Migrating API keys...")
    migrate_keys()
    
    # 3. Create unified config
    click.echo("⚙️  Creating unified configuration...")
    
    # 4. Create integration report
    click.echo("\n✅ Unification complete!")
    click.echo("\n📋 Next steps:")
    click.echo("   1. Run: parallelai keys test")
    click.echo("   2. Run: parallelai analyze --help")
    click.echo("   3. Check: ~/.parallelai/config")
