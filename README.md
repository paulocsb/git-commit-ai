# 🤖 git-commit-ai

AI-powered commit message helper that analyzes your Git diff and generates commit messages using OpenAI or a local LLM (like Ollama).

---

## 🚀 Features

- Analyze staged diffs and suggest commit messages using Ai
- Use OpenAI (`gpt-4`) or a local model (via Ollama)
- Edit messages inline before committing
- Doctor command to validate environment setup

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/paulocsb/git-commit-ai.git
cd git-commit-ai
```

2. Install with pip (in editable mode):

```bash
pip install -e .
```

3. (Optional) Add the CLI to your `$PATH` to run it like `git commit-ai`:

```bash
chmod +x bin/git-commit-ai
ln -s "$(pwd)/bin/git-commit-ai" /usr/local/bin/git-commit-ai
```

> ✅ You can now run it like a native Git command:
>
> ```bash
> git commit-ai
> ```

---

## Configuration

Create a `.env` file in the project root (or set env vars):

```env
OPENAI_API_KEY=sk-...
OLLAMA_LANGUAGE_MODEL=llama3.2-vision
```

---

## Usage

### Basic usage

```bash
git add .
git commit-ai
```

Generates a commit message based on staged changes and prompts:

```text
Suggested commit message:

✨ Add user authentication with token-based login

Commit message?/Edit/Cancel (Y/e/n):
```

### Use OpenAI instead of local agent

```bash
git commit-ai -a openai --openai-api-key sk-...
```

Or rely on your `.env`:

```bash
export OPENAI_API_KEY=sk-...
git commit-ai -a openai
```

### Use a custom local model

```bash
git commit-ai --ollama-language-model llama2
```

---

## Doctor command

Check if your environment is ready:

```bash
git commit-ai --doctor
```

---

## CLI Options

| Flag                     | Description                                 |
|--------------------------|---------------------------------------------|
| `-a, --agent`            | Choose between `local` or `openai`          |
| `--openai-api-key`       | Set your OpenAI API key                     |
| `--ollama-language-model`| Specify Ollama model name (default: `llama3.2-vision`) |
| `-d, --doctor`           | Run diagnostic checks                       |

---

## Example Workflow

```bash
git add .
git commit-ai -a openai
# Generates and suggests a commit message
# Prompts you to confirm, edit, or cancel
```

---

## Development

This project uses:

- Python 3.8+
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [OpenAI API](https://platform.openai.com/)
- [Ollama](https://ollama.com/) for local LLMs

To run from source:

```bash
python bin/git-commit-ai
```
