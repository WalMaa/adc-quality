import pytest
from rag import rag as rag_module


def test_prompt_llm_formats_and_calls_chain(mocker):
    """
    Tests that prompt_llm formats the code and calls qa_chain with it.
    """
    mock_chain = mocker.patch("rag.rag.qa_chain")
    mock_chain.return_value = {"result": "Analysis complete"}

    code = "def foo(): pass"
    result = rag_module.prompt_llm(code)

    expected_prompt = rag_module.prompt.format(code=code)
    mock_chain.assert_called_once_with(expected_prompt, return_only_outputs=True)
    assert result == {"result": "Analysis complete"}


def test_initialize_qa_chain_creates_index_and_returns_chain(mocker):
    """
    Tests that initialize_qa_chain creates a new FAISS index and returns a QA chain if index doesn't exist.
    """
    mocker.patch("os.path.exists", return_value=False)

    mock_loader = mocker.patch("rag.rag.DirectoryLoader")
    mock_loader.return_value.load.return_value = [{"page_content": "print('Hello')"}]

    mock_splitter = mocker.patch("rag.rag.CharacterTextSplitter")
    mock_splitter.return_value.split_documents.return_value = ["chunk1", "chunk2"]

    mock_embeddings = mocker.Mock()
    mocker.patch("rag.rag.HuggingFaceEmbeddings", return_value=mock_embeddings)

    mock_vectorstore = mocker.Mock()
    mock_faiss = mocker.patch("rag.rag.FAISS")
    mock_faiss.from_documents.return_value = mock_vectorstore
    mock_vectorstore.as_retriever.return_value = "mock_retriever"
    mock_vectorstore.save_local.return_value = None
    mock_faiss.load_local.return_value = mock_vectorstore

    mock_llm = mocker.Mock()
    mocker.patch("rag.rag.ChatOllama", return_value=mock_llm)

    mock_qa = mocker.patch("rag.rag.RetrievalQA")
    mock_qa.from_chain_type.return_value = "mock_qa_chain"

    result = rag_module.initialize_qa_chain()

    assert result == "mock_qa_chain"
    mock_faiss.from_documents.assert_called_once()
    mock_qa.from_chain_type.assert_called_once_with(
        llm=mock_llm, chain_type="stuff", retriever="mock_retriever"
    )


def test_initialize_qa_chain_loads_existing_index(mocker):
    """
    Tests that initialize_qa_chain loads an existing FAISS index if available.
    """
    mocker.patch("os.path.exists", return_value=True)

    mock_embeddings = mocker.Mock()
    mocker.patch("rag.rag.HuggingFaceEmbeddings", return_value=mock_embeddings)

    mock_vectorstore = mocker.Mock()
    mock_vectorstore.as_retriever.return_value = "mock_retriever"
    mocker.patch("rag.rag.FAISS.load_local", return_value=mock_vectorstore)

    mock_llm = mocker.Mock()
    mocker.patch("rag.rag.ChatOllama", return_value=mock_llm)

    mock_qa = mocker.patch("rag.rag.RetrievalQA")
    mock_qa.from_chain_type.return_value = "mock_qa_chain"

    result = rag_module.initialize_qa_chain()

    assert result == "mock_qa_chain"
    mock_qa.from_chain_type.assert_called_once_with(
        llm=mock_llm, chain_type="stuff", retriever="mock_retriever"
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
