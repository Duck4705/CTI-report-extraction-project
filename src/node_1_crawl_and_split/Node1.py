from state.state import CTIState
from tool.Crawl_URL import crawl_url
from tool.Split_Sentences import split_sentences
# from prompt.Prompt import Prompt_Planner


def Node1(state: dict):
    user_input = state['input']
    # Call crawl_url to get cleaned text content
    content = crawl_url(user_input)
    # Split the cleaned content into sentences
    sentences = split_sentences(content)
    return {"sentences": sentences}