from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from src.routes.llms import selected_llm

selected_llm = "llama3.1:latest"

template = """
System message: {system_message}

Query: {query}

"""


# Defining a structured prompt template so that we can analyze the outputs structurally
prompt = PromptTemplate(
    template=template,
    input_variables=["query", "system_message"],
)

llm = ChatOllama(model=selected_llm, base_url="http://host.docker.internal:11434")

def prompt_llm(query, system_message):
    print(f"Selected LLM: {selected_llm}")
    formatted_prompt = prompt.format(query=query, system_message=system_message)
    print("Formatted prompt: ", formatted_prompt)
    return llm.invoke(formatted_prompt)