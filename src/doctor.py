import importlib
import platform
import subprocess
import shutil

def run_doctor():
    print("\n🩺 Running environment diagnostics...\n")

    # Python
    print(f"🐍 Python version: {platform.python_version()}\n")

    # Git
    git = shutil.which("git")
    if not git:
        print("❌ Git not found.")
    else:
        print(f"✔️ Git found at: {git}")
        try:
            version = subprocess.check_output(["git", "--version"], text=True)
            print(f"   {version.strip()}")
        except Exception:
            print("   ⚠️ Failed to get Git version")

    # Python packages
    print("\n📦 Checking Python packages:")
    required = ["openai", "python-dotenv"]
    for pkg in required:
        try:
            importlib.import_module(pkg)
            print(f"✔️  {pkg}")
        except ImportError:
            print(f"❌ Missing: {pkg} — run `pip install {pkg}`")

    print("\n✅ Done.\n")

if __name__ == "__main__":
    run_doctor()