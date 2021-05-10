#  Copyright (c) 2021 by Ole Christian Astrup. All rights reserved.  Licensed under MIT
#   license.  See LICENSE in the project root for license information.
#

class Match:

    def __init__(self,match_id: str, string_id:str, word: str):
        self.match_id = match_id
        self.string_id = string_id
        self.word = word

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "string_id": self.string_id,
            "word": self.word
        }

class SpacyMeta:
    def __init__(self):
        pass

    def to_dict(self, meta: dict):
        payload = {
               "success": True,
               "lang": meta['lang'],
               "name": meta['name'],
               "version": meta['version'],
               "spacy_version": meta['spacy_version'],
               "description": meta['description'],
               "author": meta['author'],
               "email": meta['email'],
               "url": meta['url'],
               "license": meta['license'],
               "labels":  meta['labels'],
               "tok2vec": meta['labels']['tok2vec'],
               "parser": meta['labels']['parser'],
               "senter": meta['labels']['senter'],
               "ner": meta['labels']['ner'],
               "lemmatizer": meta['labels']['lemmatizer'],
               "attribute_ruler": meta['labels']['attribute_ruler'],
               "pipeline": meta['pipeline'],
               "components": meta['components'],
               "disabled": meta['disabled'],
            }
        return payload

class Matcher:
    def __init__(self):
        pass

    def to_dict(self, input: dict):

        return

