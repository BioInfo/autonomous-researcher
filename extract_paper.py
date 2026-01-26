#!/usr/bin/env python3
"""Extract paper from orchestrator log and save to reports/."""

import re
import sys
from pathlib import Path
from datetime import datetime


def extract_paper(log_path: Path) -> str:
    """Extract paper content from orchestrator log."""
    content = log_path.read_text(encoding='utf-8')

    # Look for paper markers
    # Pattern 1: After "I will draft the Arxiv-style paper" followed by markdown
    # Pattern 2: After [ORCH_FINAL] marker
    # Pattern 3: Content between "# Title" and "[DONE]"

    # Try to find markdown paper (starts with # Title or # <something>)
    paper_match = re.search(
        r'(#\s+Title.*?)(?:\[DONE\]|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if paper_match:
        paper = paper_match.group(1).strip()
        # Clean up the paper
        paper = re.sub(r'\[DONE\]', '', paper).strip()
        return paper

    # Fallback: look for content after "Final paper" or "Arxiv-style paper"
    fallback_match = re.search(
        r'(?:final paper|arxiv-style paper)[^\n]*\n+(#.*?)(?:\[DONE\]|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if fallback_match:
        return fallback_match.group(1).strip()

    return ""


def main():
    if len(sys.argv) < 2:
        # Find most recent experiment
        active_dir = Path.home() / "workspace" / "experiments" / "active"
        if not active_dir.exists():
            print("No experiments found")
            sys.exit(1)

        exp_dirs = sorted(active_dir.iterdir(), reverse=True)
        if not exp_dirs:
            print("No experiment directories found")
            sys.exit(1)

        exp_dir = exp_dirs[0]
    else:
        exp_dir = Path(sys.argv[1])

    log_path = exp_dir / "logs" / "orchestrator.log"
    if not log_path.exists():
        print(f"Log not found: {log_path}")
        sys.exit(1)

    print(f"Reading: {log_path}")
    paper = extract_paper(log_path)

    if not paper:
        print("No paper found in log")
        sys.exit(1)

    # Save to reports
    reports_dir = exp_dir / "reports"
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_path = reports_dir / f"{timestamp}_extracted_paper.md"
    report_path.write_text(paper, encoding='utf-8')

    print(f"Paper saved to: {report_path}")
    print(f"Paper length: {len(paper)} chars")


if __name__ == "__main__":
    main()
