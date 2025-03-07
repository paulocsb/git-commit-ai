from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from agents.openai_agent import generate_with_openai
from agents.local_agent import generate_with_local
from utils.diff_parser import get_git_diff
from utils.helper import * # type: ignore
from utils.helper import Colors, Icons
from doctor import run_doctor
from os import getenv
from dotenv import load_dotenv
import subprocess
import sys

load_dotenv()

def main():
  try:
    parser = ArgumentParser(
      prog="git-commit-ai",
      description="AI-powered Git commit message helper.",
      usage='%(prog)s [options]',
      add_help=True,
      formatter_class=lambda prog: ArgumentDefaultsHelpFormatter(
          prog, max_help_position=40, width=100
      )
    )

    parser.add_argument("-a", "--agent", choices=["openai", "local"], default="local", help="Set LLM agent", metavar="AGENT")

    agent_group = parser.add_argument_group("OPENAI Configuration")
    agent_group.add_argument(
        "--openai-api-key",
        metavar="API_KEY",
        help="Set openai api key"
    )

    agent_group = parser.add_argument_group("OLLAMA Configuration")
    agent_group.add_argument(
        "--ollama-language-model",
        metavar="MODEL",
        default="llama3.2-vision",
        help="Set ollama language model"
    )

    parser.add_argument("-d", "--doctor", action="store_true", help="Run environment diagnosys")
    args = parser.parse_args()

    if args.doctor:
      run_doctor()
      sys.exit(0)

    diff = get_git_diff()
    if not diff:
      print()
      print_error("There's no changes to be committed.")
      sys.exit(0)

    if args.agent == "openai":
      openai_api_key = args.openai_api_key or getenv("OPENAI_API_KEYs")

      if not openai_api_key:
        print()
        print_error("OpenAI API key is required for 'openai' agent. Use --openai-api-key or set OPENAI_API_KEY.")
        sys.exit(0)

      print()
      print_step("Generating commit message")
      msg = generate_with_openai(diff, str(openai_api_key))
    else:
      ollama_language_model = args.ollama_language_model or getenv("OLLAMA_LANGUAGE_MODEL")

      print()
      print_step("Generating commit message")
      msg = generate_with_local(diff, ollama_language_model)

    if not msg:
      print_error("Generated commit message is empty. Nothing to commit.")
      sys.exit(1)

    print_info("Commit message generated successfully\n")

    print_header("Suggested commit message:\n")
    print_highlight(f"{msg}\n")

    while True:
      choice = input(f"{Colors.BLUE}{Icons.ARROW}{Colors.NC} Commit message?/Edit/Cancel (Y/e/n): ").strip().lower()
      if choice in {'y', 'e', 'n'}:
        break
      print_error("Invalid choice. Please enter Y, e, or n.")

    if choice == 'y':
      if msg:
        commit_and_show_log(msg)
        sys.exit(0)
      else:
        print_error("Empty commit message. Aborted.")
        sys.exit(0)
    elif choice == 'e':
      print_subheader(f"\nEdit your commit message below:")
      print_info(f"Press `Enter` to commit or Type `Ctrl+C` to abort.\n")

      try:
        new_msg = prefill_input("> ", msg).strip()
        print()
      except KeyboardInterrupt:
        print()
        print_error("Edit aborted by user (Ctrl+C). No commit made.")
        sys.exit(0)

      final_msg = new_msg if new_msg else msg

      if final_msg:
        commit_and_show_log(final_msg)
        sys.exit(0)
      else:
        print_error("Commit aborted: message is empty.")
        sys.exit(0)
    elif choice == 'n':
      print_error("Cancelled. No commit made.")
      sys.exit(0)
    else:
      print_error("Invalid choice. Please enter Y, e, or n.")
      sys.exit(0)
  except KeyboardInterrupt:
    print()
    print_error("Aborted by user (Ctrl+C). No commit made.")
    sys.exit(0)

def commit_and_show_log(msg: str):
  subprocess.run(["git", "commit", "-m", msg])
  print()
  print_success("Commit created successfully:\n")
  result = subprocess.run(["git", "log", "-1"], capture_output=True, text=True)
  print(result.stdout)

if __name__ == "__main__":
  main()