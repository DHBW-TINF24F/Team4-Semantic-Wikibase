#!/usr/bin/env python3
"""
Monkey-patch script to replace hardcoded Wikidata URLs with the URL of the
Wikibase instance running in the same local (Docker) network.

This script is executed during Docker build to make the EntityShape API directly
work with the local Wikibase instance instead of wikidata.org.
"""
from pathlib import Path


def patch_file(filepath: Path) -> bool:
    """
    Patch a single Python file to replace hardcoded Wikidata URLs.
    
    Args:
        filepath: Path to the Python file to patch
        
    Returns:
        True if file was modified, False otherwise
    """
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Simple string replacements - replace all Wikidata URLs with http://wikibase
    replacements = [
        ('https://www.wikidata.org', 'http://wikibase'),
        ('http://www.wikidata.org', 'http://wikibase'),
    ]
    
    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            print(f"Replaced {count} occurrence(s) of '{old}'")
    
    # Only write if content was actually modified
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully patched {filepath.name}")
        return True
    else:
        print(f"No changes needed for {filepath.name}")
        return False


def main():
    """Main function to patch all relevant Python files."""
    print("=" * 70)
    print("EntityShape API - URL Monkey-Patching Script")
    print("Replacing Wikidata URLs with local Wikibase")
    print("=" * 70)
    print()
    
    # Find the entityshape package directory
    base_path = Path('/app/entityshape')
    
    if not base_path.exists():
        print(f"Error: Base path {base_path} does not exist!")
        return 1
    
    # Directories to patch
    api_dirs = ['api_v1', 'api_v2']
    total_patched = 0
    
    for api_dir in api_dirs:
        api_path = base_path / api_dir
        if not api_path.exists():
            print(f"Warning: {api_path} does not exist, skipping...")
            continue
        
        print(f"\nPatching files in {api_dir}/")
        print("-" * 70)
        
        # Process all Python files in the directory
        for py_file in sorted(api_path.glob('*.py')):
            if py_file.name.startswith('__'):
                continue  # Skip __init__.py and __pycache__
            
            if patch_file(py_file):
                total_patched += 1
    
    print()
    print("=" * 70)
    print(f"Patching complete! Modified {total_patched} file(s).")
    print("=" * 70)
    return 0


if __name__ == '__main__':
    exit(main())
