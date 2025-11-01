from langchain_core.messages import SystemMessage, HumanMessage
from prompt.prompt import Prompt_filter
from tool.Call_LLM import call_LLM

base_llm = call_LLM()

def Node2(state: dict):
    sentences = state['sentences']
    filtered_sentences = []

    for sentence in sentences:
        messages_system = SystemMessage(content=Prompt_filter)
        messages_user = HumanMessage(content=sentence)

        messages = [
            messages_system,
            messages_user
        ]
        response = base_llm.invoke(messages)
        if "Yes" in response.content:
            filtered_sentences.append(sentence)

    return {"filtered_sentences": filtered_sentences}