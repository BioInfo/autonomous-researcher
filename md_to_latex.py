#!/usr/bin/env python3
"""Convert markdown paper to LaTeX format."""

import re
import sys
from pathlib import Path


def md_to_latex(md_content: str) -> str:
    """Convert markdown to LaTeX."""
    lines = md_content.split('\n')
    latex_lines = []
    in_code_block = False
    title = ""
    authors = ""
    abstract = ""

    # First pass: extract title, authors, abstract
    i = 0
    while i < len(lines):
        line = lines[i]

        # Title
        if line.startswith('# ') and 'title' in line.lower():
            i += 1
            if i < len(lines):
                title = lines[i].strip()
            i += 1
            continue

        # Authors
        if line.startswith('## ') and 'author' in line.lower():
            i += 1
            if i < len(lines):
                authors = lines[i].strip()
            i += 1
            continue

        # Abstract
        if line.startswith('## ') and 'abstract' in line.lower():
            i += 1
            abstract_lines = []
            while i < len(lines) and not lines[i].startswith('#'):
                if lines[i].strip():
                    abstract_lines.append(lines[i].strip())
                i += 1
            abstract = ' '.join(abstract_lines)
            continue

        i += 1

    # Build LaTeX document
    latex_lines.append(r'\documentclass[11pt]{article}')
    latex_lines.append(r'\usepackage[utf8]{inputenc}')
    latex_lines.append(r'\usepackage[T1]{fontenc}')
    latex_lines.append(r'\usepackage{amsmath,amssymb}')
    latex_lines.append(r'\usepackage{graphicx}')
    latex_lines.append(r'\usepackage{hyperref}')
    latex_lines.append(r'\usepackage[margin=1in]{geometry}')
    latex_lines.append('')
    latex_lines.append(r'\title{' + escape_latex(title) + '}')
    latex_lines.append(r'\author{' + escape_latex(authors) + '}')
    latex_lines.append(r'\date{}')
    latex_lines.append('')
    latex_lines.append(r'\begin{document}')
    latex_lines.append(r'\maketitle')
    latex_lines.append('')

    if abstract:
        latex_lines.append(r'\begin{abstract}')
        latex_lines.append(escape_latex(abstract))
        latex_lines.append(r'\end{abstract}')
        latex_lines.append('')

    # Second pass: convert body
    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip title, authors, abstract sections (already processed)
        if line.startswith('# ') and 'title' in line.lower():
            i += 2
            continue
        if line.startswith('## ') and 'author' in line.lower():
            i += 2
            continue
        if line.startswith('## ') and 'abstract' in line.lower():
            i += 1
            while i < len(lines) and not lines[i].startswith('#'):
                i += 1
            continue

        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                latex_lines.append(r'\begin{verbatim}')
                in_code_block = True
            else:
                latex_lines.append(r'\end{verbatim}')
                in_code_block = False
            i += 1
            continue

        if in_code_block:
            latex_lines.append(line)
            i += 1
            continue

        # Section headers
        if line.startswith('### '):
            # Numbered subsection like "### 1. Introduction"
            header = line[4:].strip()
            header = re.sub(r'^\d+\.\s*', '', header)  # Remove numbering
            latex_lines.append(r'\section{' + escape_latex(header) + '}')
            i += 1
            continue

        if line.startswith('## '):
            header = line[3:].strip()
            header = re.sub(r'^\d+\.\s*', '', header)
            latex_lines.append(r'\section{' + escape_latex(header) + '}')
            i += 1
            continue

        # Horizontal rule
        if line.startswith('---'):
            i += 1
            continue

        # Bold
        line = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', line)

        # Italic
        line = re.sub(r'\*(.+?)\*', r'\\textit{\1}', line)

        # Inline code
        line = re.sub(r'`(.+?)`', r'\\texttt{\1}', line)

        # Lists
        if line.strip().startswith('- '):
            if i == 0 or not lines[i-1].strip().startswith('- '):
                latex_lines.append(r'\begin{itemize}')
            latex_lines.append(r'  \item ' + escape_latex(line.strip()[2:]))
            if i + 1 >= len(lines) or not lines[i+1].strip().startswith('- '):
                latex_lines.append(r'\end{itemize}')
            i += 1
            continue

        # Regular paragraph
        if line.strip():
            latex_lines.append(escape_latex(line))
        else:
            latex_lines.append('')

        i += 1

    latex_lines.append('')
    latex_lines.append(r'\end{document}')

    return '\n'.join(latex_lines)


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    # Don't escape if already contains LaTeX commands
    if '\\' in text and '{' in text:
        return text

    replacements = [
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_latex.py <input.md> [output.tex]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_suffix('.tex')

    md_content = input_path.read_text(encoding='utf-8')
    latex_content = md_to_latex(md_content)
    output_path.write_text(latex_content, encoding='utf-8')

    print(f"LaTeX saved to: {output_path}")


if __name__ == "__main__":
    main()
