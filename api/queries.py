from api import wolfram, nlp

def resolve_match_skill(obj, info, sentence:str):
    payload = nlp.match_skill(sentence)
    return payload

def resolve_match_tokens(obj, info, sentence:str):
    payload = nlp.match_tokens(sentence)
    return payload

def resolve_match_phrases(obj, info, sentence:str):
    payload = nlp.match_phrases(sentence)
    return payload

def resolve_spacy_meta(obj, info, lang: str):
    payload = nlp.meta(lang)
    return payload

def resolve_analysis(obj, info, sentence: str):
    payload = nlp.analysis(sentence)
    return payload

def resolve_is_english(obj,info, msg:str):
    return  nlp.is_english(msg)

def resolve_language(obj,info, sentence:str):
    payload = nlp.language(sentence)
    return payload
def resolve_wolfram_query(obj,info, question:str):
    payload = wolfram.query(question)
    return payload
def resolve_wolfram_voice(obj,info, question:str):
    payload = wolfram.voice(question)
    return payload
def resolve_wolfram_check(obj,info, question:str):
    payload = wolfram.check_query(question)
    return payload
def resolve_wolfram_conversation(obj,info, question:str, conversationid: str, s: str):
    payload = wolfram.conversation(question, conversationid)
    return payload
