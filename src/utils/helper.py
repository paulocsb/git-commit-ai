from utils.icons import Icons
from utils.colors import Colors
import readline
import subprocess

__all__ = [
  "print_header",
  "print_subheader",
  "print_success",
  "print_error",
  "print_info",
  "print_warning",
  "print_step",
  "print_highlight",
  "prefill_input"
]

def print_header(text: str):
  """Print a bold header"""
  print(f"{Colors.BOLD}{Colors.WHITE}{text}{Colors.NC}")

def print_subheader(text: str):
  """Print a subheader"""
  print(f"{Colors.BOLD}{text}{Colors.NC}")

def print_success(text: str):
  """Print success message with checkmark"""
  print(f"{Colors.GREEN}{Icons.CHECK}{Colors.NC} {text}")

def print_error(text: str):
  """Print error message with cross"""
  print(f"{Colors.RED}{Icons.CROSS}{Colors.NC} {text}")

def print_info(text: str):
  """Print info message with info icon"""
  print(f"{Colors.CYAN}{Icons.INFO} Info:{Colors.NC} {text}")

def print_warning(text: str):
  """Print warning message with bullet"""
  print(f"{Colors.YELLOW}{Icons.BULLET} Warning:{Colors.NC} {text}")

def print_step(text: str):
  """Print step message with arrow"""
  print(f"{Colors.BLUE}{Icons.ARROW}{Colors.NC} {text}")

def print_highlight(text: str):
  """Print highlight message with sparkles"""
  print(f"{Colors.YELLOW}{Icons.SPARKLES}{Colors.NC} {text}")

def prefill_input(prompt, prefill):
  def hook():
    readline.insert_text(prefill)
    readline.redisplay()

  readline.set_pre_input_hook(hook)

  try:
    return input(prompt)
  finally:
    readline.set_pre_input_hook()
