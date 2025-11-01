from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Annotated, Optional
from langgraph.graph import add_messages



class IOC(TypedDict):
    URL: list[str]
    Host: list[str]
    Email: list[str]
    Ipnet: list[str]
    File: list[str]
    Filehash: list[str]
    Filepath: list[str]
    CVE: list[str]

class CE(TypedDict):
    AttackGroup: list[str]
    SoftwareTool: list[str]

class CTIState(TypedDict):
    input: str
    sentences: list[str]
    filtered_sentences: list[str] # sentences after filtering for Mitre ATT&CK techniques
    IOC: IOC
    CE: CE
    mapped_sentences: list[str] # mapping of sentences to IOCs and CEs
    AT: list[str]