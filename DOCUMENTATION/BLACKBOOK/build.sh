#!/bin/bash

set -e

# Name of this script
SCRIPT_NAME="$(basename "$0")"

echo "Ensuring build directory exists..."
mkdir -p build

echo "Building BLACKBOOK PDF using pdflatex..."
pdflatex main.tex

# Move the generated PDF to build/
mv main.pdf build/BLACKBOOK.pdf

# Clean up LaTeX build artifacts
rm -f main.aux main.log main.toc main.out main.synctex.gz

echo "Cleaning up the project directory..."

# List of folders and files to keep
KEEP=("chapters" "frontmatter" "references" "assets" "build" "style" "main.tex" "$SCRIPT_NAME")

# Loop through all items in the current directory after build
for item in *; do
    skip=false
    for keep_item in "${KEEP[@]}"; do
        if [[ "$item" == "$keep_item" ]]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = false ]; then
        echo "Removing: $item"
        rm -rf "$item"
    fi
done

echo "Build complete and cleanup done. Final PDF: build/BLACKBOOK.pdf"
