from langchain_core.messages import SystemMessage, HumanMessage
from prompt.prompt import Prompt_extract_IOC
from state.state import IOC
from tool.Call_LLM import call_LLM



base_llm_with_structed = call_LLM(IOC)

def Node3(state: dict):
    filtered_sentences = state['filtered_sentences']
    all_IOC = {
        "URL": [],
        "Filepath": [],
        "File": [],
        "Filehash": [],
        "Email": [],
        "Ipnet": [],
        "Host": [],
        "CVE": []
    }

    for sentence in filtered_sentences:
        messages_system = SystemMessage(content=Prompt_extract_IOC)
        messages_user = HumanMessage(content=sentence)

        messages = [
            messages_system,
            messages_user
        ]
        try:
            response = base_llm_with_structed.invoke(messages)
            for key in all_IOC.keys():
                if key in response:
                    all_IOC[key].extend(response[key])
        except Exception as e:
            print(f"Error processing sentence: {e}")

    # Convert to the format expected by state.py
    state_ioc = {
        "URL": all_IOC["URL"],
        "Host": all_IOC["Host"],
        "Email": all_IOC["Email"],
        "Ipnet": all_IOC["Ipnet"],
        "File": all_IOC["File"],
        "Filehash": all_IOC["Filehash"],
        "Filepath": all_IOC["Filepath"],
        "CVE": all_IOC["CVE"]
    }
    
    return {"IOC": state_ioc}