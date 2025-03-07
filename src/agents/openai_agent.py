from openai import OpenAI
from utils.helper import print_info, print_warning

def generate_with_openai(diff_text, api_key):
  print_info("Running openai LLM agent")

  openai_client = OpenAI()
  openai_client.api_key = api_key

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

  completion = openai_client.chat.completions.create(
      model="gpt-4",
      messages=[{"role": "user", "content": prompt}],
      temperature=0.7,
  )

  return completion.choices[0].message.content