import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from routes.llms import get_current_selected_llm

template = """
System message: {system_message}

Query: {query}

"""

prompt = PromptTemplate(
    template=template,
    input_variables=["query", "system_message"],
)

llm = None

def prompt_llm(query, system_message):
    global llm
    selected_llm = get_current_selected_llm()
    if not selected_llm:
        raise ValueError("No LLM model selected")
    
    if llm is None or llm.model != selected_llm:
        llm = ChatOllama(model=selected_llm, base_url="http://host.docker.internal:11434")
    
    print(f"Selected LLM: {selected_llm}")
    formatted_prompt = prompt.format(query=query, system_message=system_message)
    print("Formatted prompt: ", formatted_prompt)
    return llm.invoke(formatted_prompt)