import logging
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler
from rich.theme import Theme

# Custom theme for the console
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "bold green",
    "thought": "italic cyan",
    "code": "bold yellow",
    "result": "white"
})

console = Console(theme=custom_theme)

# Global logger instance and log file path
logger = None
_log_file_path = None

def setup_logging(log_file_path: str = "agent.log"):
    """Sets up logging to both file and console."""
    global logger, _log_file_path

    _log_file_path = log_file_path

    # Ensure directory exists
    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            # We don't add RichHandler here because we want manual control over console output
            # to keep it "elegant" and not just a stream of logs.
        ]
    )
    # Create a separate logger for the file that doesn't propagate to root
    file_logger = logging.getLogger("agent_file")
    file_logger.setLevel(logging.DEBUG)
    logger = file_logger
    return file_logger

def set_log_file(log_file_path: str):
    """Update the log file path dynamically."""
    global logger
    logger = setup_logging(log_file_path)

# Initialize with default log file (will be updated when experiment starts)
logger = setup_logging()

def log_step(step_name, status="INFO"):
    """Logs a step to the file."""
    logger.info(f"[{step_name}] {status}")

def print_panel(content, title, style="info"):
    """Prints a rich panel to the console."""
    console.print(Panel(content, title=title, border_style=style, expand=False))

def print_status(message, style="info"):
    """Prints a status message."""
    console.print(f"[{style}]{message}[/{style}]")
