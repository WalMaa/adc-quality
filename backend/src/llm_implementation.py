from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from src.routes.llms import get_current_selected_llm

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