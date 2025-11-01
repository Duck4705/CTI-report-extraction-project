from langchain_core.messages import SystemMessage, HumanMessage
from prompt.prompt import Prompt_extract_CE
from state.state import CE
from tool.Call_LLM import call_LLM



base_llm_with_structed = call_LLM(CE)

def Node4(state: dict):
    filtered_sentences = state['filtered_sentences']
    all_CE = {
        "AttackGroup": [],
        "SoftwareTool": []
    }

    for sentence in filtered_sentences:
        messages_system = SystemMessage(content=Prompt_extract_CE)
        messages_user = HumanMessage(content=sentence)

        messages = [
            messages_system,
            messages_user
        ]
        try:
            response = base_llm_with_structed.invoke(messages)
            for key in all_CE.keys():
                if key in response:
                    all_CE[key].extend(response[key])
        except Exception as e:
            print(f"Error processing sentence: {e}")

    # Convert to the format expected by state.py
    state_ce = {
        "AttackGroup": all_CE["AttackGroup"],
        "SoftwareTool": all_CE["SoftwareTool"]
    }
   
    return {"CE": state_ce}