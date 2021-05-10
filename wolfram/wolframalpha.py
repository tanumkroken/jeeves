

import requests
from wolfram import WOLFRAM_ALPHA_JEEVES
from wolframalpha import Client, Result


class WolframAlpha:
    def __init__(self, logger):
        self.logger = logger
        self.wolfram = Client(WOLFRAM_ALPHA_JEEVES)
        self.voice_api = 'http://api.wolframalpha.com/v1/spoken?'
        self.conversation_api = 'http://api.wolframalpha.com/v1/conversation.jsp?'

    def query(self, question: str):
        podres = []
        res = self.wolfram.query(question)
        parse = Result(res)
        print(parse.details)
        print(parse.results)
        payload = {
            "question": question,
            "success": res.success,
            "numpods": res.numpods}
        if res.success:
            for pod in res.pods:
                for sub in pod.subpods:
                    podres.append({'title': pod.title,'result':sub.plaintext})
        payload['pods'] = podres
        # The voice result
        # params={'i': question,'appid':WOLFRAM_ALPHA_API}
        #res = requests.get(self.voice_api,params=params)
        #payload['voice'] = res.text
        return payload

    def check_query(self, question: str):
        # Check if Wolfram has an answer to the question
        http = self.query_api.format(question, WOLFRAM_ALPHA_REST)
        check = requests.get(self.query_api.format(question, WOLFRAM_ALPHA_REST))
        result = check.json()
        print(http, result)
        if result['query']['accepted'] is True:
            payload = {
                "question": question,
                "success": True,
                "domain" : result['query']['domain']}
        else:
            payload = {
                "question": question,
                "success": False
            }
        return payload

    def voice(self, question: str):
        params={'i': question,'appid':WOLFRAM_ALPHA_JEEVES}
        res = requests.get(self.voice_api,params=params)
        payload = {"question": question,"success": True}
        payload['voice'] = res.text
        return payload

    def conversation(self, question: str, conversation_id: str = '') -> dict:
        # First question in the conversation
        if conversation_id == '':
            params={'i': question,'appid':WOLFRAM_ALPHA_JEEVES}
            res = requests.get(self.conversation_api,params=params)
        # Follow up question in the conversation
        else:
            params={'i': question,'appid':WOLFRAM_ALPHA_JENKINS, 'conversationid': conversation_id}
            res = requests.get(self.conversation_api,params=params)
        json = res.json()
        if 'error' in json:
            payload = {"question": question,"success": False, 'error':json['error']}
            return payload
        else:
            payload = {"question": question,"success": True}
            payload['result'] = json['result']
            payload['conversationid'] = json['conversationID']
            if 's' in json:
                payload['s'] = json['s']
            return payload
