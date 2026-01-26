#!/bin/bash
# Compile LaTeX on remote system and retrieve PDF

set -e

# Configuration
REMOTE_HOST="${LATEX_HOST:-thingamajig}"
REMOTE_DIR="${LATEX_DIR:-/Users/schaferk/TeX}"
REMOTE_TEXIT="${LATEX_TEXIT:-/Users/schaferk/bin/texit.s}"
REMOTE_TEXPATH="${LATEX_TEXPATH:-/Library/TeX/texbin}"

usage() {
    echo "Usage: $0 <file.tex> [output_dir]"
    echo ""
    echo "Compile LaTeX on remote system and retrieve PDF."
    echo ""
    echo "Arguments:"
    echo "  file.tex    Path to the .tex file to compile"
    echo "  output_dir  Directory to save PDF (default: same as input)"
    echo ""
    echo "Environment variables:"
    echo "  LATEX_HOST    Remote host (default: thingamajig)"
    echo "  LATEX_DIR     Remote working directory (default: /Users/schaferk/TeX)"
    echo "  LATEX_TEXIT   Path to texit.s (default: /Users/schaferk/bin/texit.s)"
    echo "  LATEX_TEXPATH Path to TeX binaries (default: /Library/TeX/texbin)"
    exit 1
}

if [ -z "$1" ]; then
    usage
fi

TEX_FILE="$1"
OUTPUT_DIR="${2:-$(dirname "$TEX_FILE")}"

if [ ! -f "$TEX_FILE" ]; then
    echo "Error: File not found: $TEX_FILE"
    exit 1
fi

BASENAME=$(basename "$TEX_FILE")
NAME="${BASENAME%.tex}"

echo "==> Uploading $TEX_FILE to $REMOTE_HOST:$REMOTE_DIR/"
rsync -av "$TEX_FILE" "$REMOTE_HOST:$REMOTE_DIR/"

echo "==> Compiling on $REMOTE_HOST..."
ssh "$REMOTE_HOST" "cd $REMOTE_DIR && PATH=$REMOTE_TEXPATH:\$PATH $REMOTE_TEXIT $BASENAME"

echo "==> Downloading PDF..."
rsync -av "$REMOTE_HOST:$REMOTE_DIR/$NAME.pdf" "$OUTPUT_DIR/"

echo "==> Done: $OUTPUT_DIR/$NAME.pdf"
