import sys
import importlib.util
from pathlib import Path
import pytest
import tempfile
import os

main_path = Path(__file__).resolve().parents[1] / "main.py"
spec = importlib.util.spec_from_file_location("main_module", main_path)
main_module = importlib.util.module_from_spec(spec)
sys.modules["main_module"] = main_module
spec.loader.exec_module(main_module)


@pytest.fixture
def temp_py_file():
    """Fixture to create a temporary Python file."""
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
        tmp.write("def foo(): pass")
        tmp_path = tmp.name
    yield tmp_path
    os.unlink(tmp_path)


def test_list_code_files_returns_only_py_files(tempfile_path=tempfile.gettempdir()):
    """
    Tests that only .py files are returned by list_code_files().
    """
    py_file = os.path.join(tempfile_path, "example.py")
    txt_file = os.path.join(tempfile_path, "note.txt")
    with open(py_file, "w") as f:
        f.write("print('Hello')")
    with open(txt_file, "w") as f:
        f.write("note")

    result = main_module.list_code_files(tempfile_path)
    assert py_file in result
    assert txt_file not in result


def test_select_file_or_action_returns_selection(monkeypatch):
    """
    Tests that select_file_or_action returns the selected file when prompt works normally.
    """
    monkeypatch.setattr("inquirer.prompt", lambda _: {"selection": "file1.py"})
    result = main_module.select_file_or_action(["file1.py", "file2.py"])
    assert result == "file1.py"


def test_select_file_or_action_keyboard_interrupt(monkeypatch):
    """
    Tests that select_file_or_action raises KeyboardInterrupt when interrupted by user.
    """
    monkeypatch.setattr("inquirer.prompt", lambda _: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        main_module.select_file_or_action(["a.py"])


def test_select_file_or_action_error_handling(monkeypatch, capsys):
    """
    Tests that select_file_or_action returns 'Quit Program' and logs error on exception.
    """
    monkeypatch.setattr("inquirer.prompt", lambda _: (_ for _ in ()).throw(Exception("inquirer crashed")))
    result = main_module.select_file_or_action(["a.py"])
    captured = capsys.readouterr()
    assert "⚠️ Error during selection: inquirer crashed" in captured.out
    assert result == "Quit Program"


def test_analyze_file_success(monkeypatch, capsys, temp_py_file):
    """
    Tests that analyze_file prints the analysis result for valid input.
    """
    monkeypatch.setattr(main_module, "prompt_llm", lambda code: f"Analysis of: {code}")
    main_module.analyze_file(temp_py_file)
    captured = capsys.readouterr()
    assert "🧪 Analyzing" in captured.out
    assert "Analysis of" in captured.out


def test_analyze_file_failure(capsys):
    """
    Tests that analyze_file handles errors gracefully when file does not exist.
    """
    main_module.analyze_file("/nonexistent/file.py")
    captured = capsys.readouterr()
    assert "❌ Error analyzing file:" in captured.out


def test_main_runs_single_file_mode(monkeypatch, capsys):
    """
    Tests that main() analyzes a single file when --file is provided.
    """
    fake_code = "print('x')"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(fake_code)
        tmp_path = tmp.name

    monkeypatch.setattr(sys, "argv", ["main.py", "--file", tmp_path])
    monkeypatch.setattr(main_module, "prompt_llm", lambda code: "Mocked Result")
    monkeypatch.setattr(main_module, "select_file_or_action", lambda x: "Quit Program")
    monkeypatch.setattr(main_module, "list_code_files", lambda x: [tmp_path])

    main_module.main()
    captured = capsys.readouterr()
    assert "Mocked Result" in captured.out
    os.unlink(tmp_path)


def test_main_file_not_found(monkeypatch, capsys):
    """
    Tests that main() prints an error if the specified file path does not exist.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "--file", "/nonexistent.py"])
    monkeypatch.setattr(main_module, "select_file_or_action", lambda x: "Quit Program")
    monkeypatch.setattr(main_module, "list_code_files", lambda x: [])
    main_module.main()
    captured = capsys.readouterr()
    assert "⚠️ File not found" in captured.out


def test_main_interactive_exit(monkeypatch, capsys):
    """
    Tests that main() exits correctly when 'Quit Program' is selected in interactive mode.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "--interactive"])
    monkeypatch.setattr(main_module, "select_file_or_action", lambda x: "Quit Program")
    monkeypatch.setattr(main_module, "list_code_files", lambda x: [])
    main_module.main()
    captured = capsys.readouterr()
    assert "👋 Exiting program" in captured.out


def test_main_valid_selection_calls_analyze(monkeypatch):
    """
    Tests that main() calls analyze_file when a valid file is selected.
    """
    test_file = "valid_script.py"
    monkeypatch.setattr(sys, "argv", ["main.py", "--interactive"])
    monkeypatch.setattr(main_module, "list_code_files", lambda _: [test_file])

    call_count = {"analyzed": False}
    monkeypatch.setattr(main_module, "analyze_file", lambda x: call_count.update(analyzed=True))

    # return the valid file once, then exit
    def fake_selector(_):
        return test_file if not call_count["analyzed"] else "Quit Program"

    monkeypatch.setattr(main_module, "select_file_or_action", fake_selector)

    main_module.main()
    assert call_count["analyzed"]


def test_main_invalid_selection(monkeypatch, capsys):
    """
    Tests that main() prints a warning when selection is invalid.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "--interactive"])

    monkeypatch.setattr(main_module, "list_code_files", lambda x: ["valid1.py", "valid2.py"])

    # First call returns an invalid selection, second call exits loop
    monkeypatch.setattr(main_module, "select_file_or_action",
        lambda x: "not_in_available_files" if "valid1.py" in x else "Quit Program")

    monkeypatch.setattr(main_module, "analyze_file", lambda x: None)

    # To break the loop: on second call to select_file_or_action, return "Quit Program"
    call_count = {"count": 0}
    def fake_selector(files):
        call_count["count"] += 1
        return "not_in_available_files" if call_count["count"] == 1 else "Quit Program"

    monkeypatch.setattr(main_module, "select_file_or_action", fake_selector)

    main_module.main()
    captured = capsys.readouterr()
    assert "⚠️ Invalid selection." in captured.out


def test_signal_handler_exits_gracefully(capsys):
    """
    Tests that signal_handler prints a goodbye message and exits the program.
    """
    with pytest.raises(SystemExit):
        main_module.signal_handler(None, None)
    captured = capsys.readouterr()
    assert "👋 Interrupted by user. Exiting program. Goodbye!" in captured.out
