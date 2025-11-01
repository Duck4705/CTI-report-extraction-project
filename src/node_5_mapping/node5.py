from tool.Mapping_Tool import map_sentence_with_IOC_CE

def Node5(state: dict):
    filtered_sentences = state['filtered_sentences']
    ioc_dict = state.get('IOC', {})
    ce_dict = state.get('CE', {})

    mapped_sentences = []
    for sentence in filtered_sentences:
        mapped_sentence = map_sentence_with_IOC_CE(sentence, ioc_dict, ce_dict)
        mapped_sentences.append(mapped_sentence)

    return {"mapped_sentences": mapped_sentences}