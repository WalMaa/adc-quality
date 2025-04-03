import importlib.util
from pathlib import Path
import sys
import os
import argparse
import inquirer
import signal

rag_path = (Path(__file__).parent / "rag.py").resolve()
spec = importlib.util.spec_from_file_location("rag_module", rag_path)
rag_module = importlib.util.module_from_spec(spec)
sys.modules["rag_module"] = rag_module
spec.loader.exec_module(rag_module)

prompt_llm = rag_module.prompt_llm

BACKEND_PATH = "../backend"

def signal_handler(sig, frame):
    print("\n\n👋 Interrupted by user. Exiting program. Goodbye!")
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

def list_code_files(directory):
    valid_ext = {".py"}
    files = []
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            if Path(f).suffix in valid_ext:
                files.append(os.path.join(root, f))
    return sorted(files)

def select_file_or_action(files):
    choices = files + ["Quit Program"]
    
    try:
        questions = [
            inquirer.List(
                "selection",
                message="Select a file to analyze or quit",
                choices=choices,
            )
        ]
        answers = inquirer.prompt(questions)
        return answers["selection"] if answers else None
    except KeyboardInterrupt:
        raise KeyboardInterrupt("User interrupted the selection process.")
    except Exception as e:
        print(f"⚠️ Error during selection: {e}")
        return "Quit Program"
        

def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            print(f"\n🧪 Analyzing {file_path}...\n")
            result = prompt_llm(code)
            print("\n🔍 Result:")
            print(result)
            print("\n" + "-" * 60)
    except Exception as e:
        print(f"\n❌ Error analyzing file: {e}")
        print("-" * 60)

def main():
    parser = argparse.ArgumentParser(description="RAG Code Quality CLI")
    parser.add_argument("--interactive", action="store_true", help="Use interactive file selector")
    parser.add_argument("--file", help="Specify a single file path directly")

    args = parser.parse_args()
    available_files = list_code_files(BACKEND_PATH)

    # If a single file is specified, analyze it and then enter interactive mode
    if args.file:
        if os.path.isfile(args.file):
            analyze_file(args.file)
        else:
            print(f"⚠️ File not found: {args.file}")
    
    # Enter interactive mode (both with --interactive flag or after analyzing a single file)
    if args.interactive or args.file or not (args.interactive or args.file):
        while True:
            selection = select_file_or_action(available_files)
            
            if selection == "Quit Program":
                print("👋 Exiting program. Goodbye!")
                break
            
            if selection in available_files:
                analyze_file(selection)
            else:
                print("⚠️ Invalid selection.")

if __name__ == "__main__": # pragma: no cover
    main()