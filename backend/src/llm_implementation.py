from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

model_name = "llama3.1"

template = """
System message: {system_message}

Query: {query}

"""


# Defining a structured prompt template so that we can analyze the outputs structurally
prompt = PromptTemplate(
    template=template,
    input_variables=["query", "system_message"],
)

llm = ChatOllama(model=model_name, temperature=0.2,)


def prompt_llm(query, system_message):
    formatted_prompt = prompt.format(query=query, system_message=system_message)
    print("Formatted prompt: ", formatted_prompt)
    return llm.invoke(formatted_prompt)
