from api import nlp


def resolve_register_skill(obj, info, domain: str, call_back:str, lang: str, matcher):
    payload = nlp.register_skill(domain, call_back, lang, matcher)
    return payload

def resolve_register_domain(obj, info, domain:str, lang: str, phrases):
    payload = nlp.register_domain(domain, lang, phrases)
    return payload
