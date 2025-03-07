import subprocess
from utils.helper import print_info, print_warning

def generate_with_local(diff_text, model):
    print_info("Running ollama LLM agent")

    # Ensure clean diff without contamination
    if "Provide a clear and concise" in diff_text:
        print_warning("Diff contains previous prompt! Cleaning it.")
        lines = diff_text.splitlines()
        lines = [line for line in lines if "Provide a clear and concise" not in line]
        diff_text = "\n".join(lines)

    prompt = (
        "Provide a clear and concise git commit message for the following diff, "
        "without any quotes, no backticks or explanations before or after to the message:\n\n"
        f"{diff_text}"
    )

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()