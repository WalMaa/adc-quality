import os
import inquirer
import argparse
from pathlib import Path
from rag import prompt_llm

BACKEND_PATH = "../backend"

def list_code_files(directory):
    valid_ext = {".py"}
    files = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            if Path(f).suffix in valid_ext:
                files.append(os.path.join(root, f))
    return files

def select_file(files):
    questions = [
        inquirer.List(
            "selected_file",
            message="Select a file to analyze",
            choices=files,
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["selected_file"] if answers else None

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        print(f"\n🧪 Analyzing {file_path}...\n")
        result = prompt_llm(code)
        print("🔍 Result:")
        print(result)
        print("-" * 60)

def main():
    parser = argparse.ArgumentParser(description="RAG Code Quality CLI")
    parser.add_argument("--interactive", action="store_true", help="Use interactive file selector")
    parser.add_argument("--file", help="Specify a single file path directly")

    args = parser.parse_args()
    available_files = list_code_files(BACKEND_PATH)

    if args.interactive:
        selected = select_file(available_files)
    elif args.file:
        selected = args.file
    else:
        print("No file specified. Use --interactive or --file.")
        return

    if selected not in available_files and not os.path.isfile(selected):
        print("⚠️ Invalid file selection.")
        return

    analyze_file(selected)

if __name__ == "__main__":
    main()
