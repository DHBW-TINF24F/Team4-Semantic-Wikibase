#!/bin/sh
# ==============================================================================
# Extension Dependency Installer
# ==============================================================================
#
# This script automatically installs Composer dependencies for all MediaWiki
# extensions that require them. It runs as an init container before the 
# Wikibase service starts.
#
# The script is idempotent - it only installs dependencies if they don't 
# already exist, making it safe to run multiple times.
#
# Usage: Called automatically by the extension-installer service in 
#        docker-compose.yml
#
# ==============================================================================

set -e  # Exit on error

EXTENSIONS_DIR="/extensions"
INSTALLED_COUNT=0
SKIPPED_COUNT=0

echo "========================================"
echo "Extension Dependency Installer"
echo "========================================"
echo ""

# Check if extensions directory exists
if [ ! -d "$EXTENSIONS_DIR" ]; then
    echo "ERROR: Extensions directory not found at $EXTENSIONS_DIR"
    exit 1
fi

# Iterate through all subdirectories in the extensions folder
for ext_dir in "$EXTENSIONS_DIR"/*/; do
    # Skip if not a directory
    [ -d "$ext_dir" ] || continue
    
    ext_name=$(basename "$ext_dir")
    
    # Skip hidden directories
    if [ "$(echo "$ext_name" | cut -c1)" = "." ]; then
        continue
    fi
    
    # Check if extension has composer.json
    if [ -f "$ext_dir/composer.json" ]; then
        echo "Found extension: $ext_name"
        
        # Check if vendor directory already exists
        if [ -d "$ext_dir/vendor" ]; then
            echo "  ✓ Dependencies already installed, skipping..."
            SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        else
            echo "  → Installing Composer dependencies..."
            cd "$ext_dir"
            
            # Run composer install with appropriate flags
            if composer install --no-dev --no-interaction --optimize-autoloader 2>&1; then
                echo "  ✓ Successfully installed dependencies"
                INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
            else
                echo "  ✗ Failed to install dependencies"
                exit 1
            fi
        fi
        echo ""
    fi
done

echo "========================================"
echo "Installation Summary"
echo "========================================"
echo "Extensions processed: $((INSTALLED_COUNT + SKIPPED_COUNT))"
echo "  - Installed: $INSTALLED_COUNT"
echo "  - Skipped (already installed): $SKIPPED_COUNT"
echo ""
echo "Done! Extensions are ready to use."
echo "========================================"
