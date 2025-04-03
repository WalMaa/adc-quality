import os

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH")

model_name = "llama3.1"

template = """
You are an assistant in code quality analysis.
You need to look for source code quality improvements.
Suggest a remediation for the identified issue.

DO NOT HALLUCINATE.

Source code:

{code}

"""


prompt = PromptTemplate(
    template=template,
    input_variables=["code"],
)



def initialize_qa_chain():
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        faiss_path = os.path.join(project_root, "faiss_index_")

        # Load embedding model
        print("Loading embedding model...")
        embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {"device": "cuda"}
        embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs=model_kwargs
        )
        
        if os.path.exists(faiss_path):
            print(f"Loading FAISS vector store from {faiss_path}...")
            persisted_vectorstore = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
        else:
            # Load the dataset using LangChain's DirectoryLoader
            print(f"Loading documents from {DATASET_PATH}...")
            loader = DirectoryLoader(DATASET_PATH, glob=["**/*.java", "**/*.py", "**/*.js", "**/*.ts"])
            documents = loader.load()
            
            # Split the document into chunks
            print("Splitting documents...")
            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100, separator="\n")
            docs = text_splitter.split_documents(documents=documents)


            # Create FAISS vector store
            print("Creating FAISS vector store, this might take a while...")
            vectorstore = FAISS.from_documents(docs, embeddings)

            vectorstore.save_local(faiss_path)
            persisted_vectorstore = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)

        # Create a retriever
        retriever = persisted_vectorstore.as_retriever(search_kwargs={"k": 5})

        llm = ChatOllama(model=model_name,
            num_predict=512,
            num_gpu=1
            )

        # Create Retrieval-Augmented Generation (RAG) system
        return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff" , retriever=retriever)
    except Exception as e:
        print(f"Initialization failed: {e}")
        raise
    


def prompt_llm(code):
    """
    Formats and sends a query to the LLM via RetrievalQA.
    """
    print("Querying LLM...")
    formatted_prompt = prompt.format(code=code)
    return qa_chain(formatted_prompt, return_only_outputs=True)

    
qa_chain = initialize_qa_chain()
   

