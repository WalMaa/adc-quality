import sys
import importlib.util
from pathlib import Path
import pytest
import os

# Dynamically import rag.py from rag/ directory
rag_path = Path(__file__).resolve().parents[1] / "rag.py"
spec = importlib.util.spec_from_file_location("rag_module", rag_path)
rag_module = importlib.util.module_from_spec(spec)
sys.modules["rag_module"] = rag_module
spec.loader.exec_module(rag_module)


@pytest.fixture
def mock_llm_pipeline(mocker, tmp_path):
    """
    Patches all common dependencies in initialize_qa_chain for reuse in multiple tests.
    """
    mocker.patch("os.path.exists", return_value=False)

    mock_loader = mocker.patch.object(rag_module, "DirectoryLoader")
    mock_loader.return_value.load.return_value = [{"page_content": "code"}]

    mock_splitter = mocker.patch.object(rag_module, "CharacterTextSplitter")
    mock_splitter.return_value.split_documents.return_value = ["chunk1", "chunk2"]

    mock_embeddings = mocker.Mock()
    mocker.patch.object(rag_module, "HuggingFaceEmbeddings", return_value=mock_embeddings)

    mock_vectorstore = mocker.Mock()
    mock_vectorstore.as_retriever.return_value = "mock_retriever"

    mock_faiss = mocker.patch.object(rag_module, "FAISS")
    mock_faiss.from_documents.return_value = mock_vectorstore
    mock_faiss.load_local.return_value = mock_vectorstore
    mock_vectorstore.save_local.return_value = None

    mock_llm = mocker.Mock()
    mocker.patch.object(rag_module, "ChatOllama", return_value=mock_llm)

    mock_qa = mocker.patch.object(rag_module, "RetrievalQA")
    mock_qa.from_chain_type.return_value = "mock_qa_chain"

    real_path_join = os.path.join

    def safe_path_join(*args):
        joined = real_path_join(*args)
        if "faiss_index_" in joined:
            return str(tmp_path / "fake_faiss_index")
        return joined

    mocker.patch("os.path.join", side_effect=safe_path_join)

    return {
        "mock_faiss": mock_faiss,
        "mock_qa": mock_qa,
        "mock_vectorstore": mock_vectorstore,
        "mock_llm": mock_llm,
    }


def test_prompt_llm_formats_and_calls_chain(mocker):
    """
    Tests that prompt_llm formats the code and calls qa_chain with it.
    """
    mock_chain = mocker.patch.object(rag_module, "qa_chain")
    mock_chain.return_value = {"result": "Analysis complete"}

    code = "def foo(): pass"
    result = rag_module.prompt_llm(code)

    expected_prompt = rag_module.prompt.format(code=code)
    mock_chain.assert_called_once_with(expected_prompt, return_only_outputs=True)
    assert result == {"result": "Analysis complete"}


def test_initialize_qa_chain_creates_index_and_returns_chain(mock_llm_pipeline):
    """
    Tests that initialize_qa_chain creates a FAISS index and returns a QA chain.
    """
    result = rag_module.initialize_qa_chain()

    assert result == "mock_qa_chain"
    mock_llm_pipeline["mock_faiss"].from_documents.assert_called_once()
    mock_llm_pipeline["mock_qa"].from_chain_type.assert_called_once_with(
        llm=mock_llm_pipeline["mock_llm"], chain_type="stuff", retriever="mock_retriever"
    )


def test_initialize_qa_chain_loads_existing_index(mock_llm_pipeline, mocker):
    """
    Tests that initialize_qa_chain loads an existing FAISS index if available.
    """
    mocker.patch("os.path.exists", return_value=True)

    result = rag_module.initialize_qa_chain()

    assert result == "mock_qa_chain"
    mock_llm_pipeline["mock_qa"].from_chain_type.assert_called_once_with(
        llm=mock_llm_pipeline["mock_llm"], chain_type="stuff", retriever="mock_retriever"
    )


def test_initialize_qa_chain_error_handling(mocker, capsys):
    """
    Tests that initialize_qa_chain prints and raises exception on failure.
    """
    mocker.patch("os.path.exists", side_effect=RuntimeError("Mocked init failure"))

    with pytest.raises(RuntimeError):
        rag_module.initialize_qa_chain()

    captured = capsys.readouterr()
    assert "Initialization failed: Mocked init failure" in captured.out
