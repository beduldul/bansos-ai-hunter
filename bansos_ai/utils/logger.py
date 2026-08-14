"""
Modul Logger Terintegrasi Menggunakan Rich Console.
"""

import sys
from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_logger(verbose: bool = False) -> logging.Logger:
    """Mengonfigurasi logger aplikasi dengan format Rich."""
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)]
    )
    
    logger = logging.getLogger("bansos_ai")
    logger.setLevel(log_level)
    return logger

logger = setup_logger()
