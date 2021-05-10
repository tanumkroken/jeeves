#  Copyright (c) 2021 by Ole Christian Astrup. All rights reserved.  Licensed under MIT
#   license.  See LICENSE in the project root for license information.
#
import spacy
from spacy.errors import MatchPatternError
from spacy.matcher import Matcher
import fasttext
from iso_language_codes import language_name
from api.models import Match, SpacyMeta
from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span
from translate import Translator



class MyTranslator:
    ''' Using MyMemory to translate between languages'''
    def __init__(self, **kwargs):
        if 'from_lang' in kwargs:
            self.from_lang = kwargs['from_lang']
        else:
            self.from_lang = 'no'
        if 'to_lang' in kwargs:
            self.to_lang = kwargs['to_lang']
        else:
            self.to_lang = 'en'
        self.email = 'ole.christian@astrup.info'
        self.translator = Translator(from_lang=self.from_lang, to_lang=self.to_lang)


    def translate(self, sentence: str)->str:
        translation = self.translator.translate(sentence)
        return translation

class SkillMatcher:
    def __init__(self, nlp, logger):
        self.logger = logger
        self.nlp = nlp # The list of nlp vocab instances, one for each language
        self.phrase_matcher = {}  # The phrase based PhraseMatcher
        self.token_matcher = {}  # The token based Matcher
        # Create the PhraseMatcher
        self.create_phrase_matchers()
        # Crete the Matchers
        self.create_matchers()

    def create_matchers(self):
        # Create the token matchers
        for lang in self.nlp:
            #if DEBUG:
            self.logger.info('Creating Matcher object for language {}'.format(lang))
            nlp = self.nlp[lang]
            self.token_matcher[lang] = Matcher(nlp.vocab, validate=True)
        return

    def create_phrase_matchers(self):
        # Create the phrase matcher
        for lang in self.nlp:
            self.logger.info('Creating PhraseMatcher object for language {}'.format(lang))
            nlp = self.nlp[lang]
            self.phrase_matcher[lang] = PhraseMatcher(nlp.vocab, validate=True, attr="LOWER") # Only match lowercase
        return

    def register_skill_domain(self, domain: str, lang: str, phrases):
        ''' Register a PhraseMatcher pattern '''
        payload = {"success": True,  'domain': domain, 'lang':lang, 'pattern': phrases}
        try:
            if lang == 'en':
                phrase_matcher = self.phrase_matcher['en']
                nlp = self.nlp[lang]
                # Add each individual term
                # Only run nlp.make_doc to speed things up
                patterns = [nlp.make_doc(text) for text in phrases]
                phrase_matcher.add(domain, patterns)
                payload['rules'] = len(phrase_matcher)
                self.logger.debug(f"Added skill domain rule: ({domain}, {phrases} for language {lang}")
            elif lang == 'no':
                phrase_matcher = self.phrase_matcher['no']
                nlp = self.nlp[lang]
                # Add each individual term
                # Only run nlp.make_doc to speed things up
                patterns = [nlp.make_doc(text) for text in phrases]
                phrase_matcher.add(domain, patterns)
                payload['rules'] = len(phrase_matcher)
                self.logger.debug(f"Added skill domain rule: ({domain}, {phrases} for language {lang}")
            else:
                payload['success'] = False
                msg = f'No vocab has been loaded for language {lang}'
                payload['errors'] = [msg]
                self.logger.error(msg)
        except MatchPatternError as err:
            payload["success"] = False
            msg = f"Error registering pattern for PhraseMatcher {domain}: {err}"
            payload["errors"] = [msg]
            self.logger.error(msg)
        return payload

    def register_skill(self, domain: str, call_back: str, lang: str, patterns):
        ''' Register a Matcher pattern '''
        payload = {"success": True, "domain": domain, 'call_back': call_back, 'lang':lang, 'pattern': patterns}
        try:
            if lang == 'en':
                matcher = self.token_matcher['en']
                matcher.add(call_back, [patterns])
                on_match, patterns = matcher.get(call_back)
                payload['rules'] = len(matcher)
                self.logger.debug(f"Added skill method: ({call_back}, {patterns} for language {lang}")
            elif lang == 'no':
                matcher = self.token_matcher['no']
                matcher.add(call_back, [patterns])
                payload['rules'] = len(matcher)
                self.logger.debug(f"Added skill method: ({call_back}, {patterns} for language {lang}")
            else:
                payload['success'] = False
                msg = f'No vocab has been loaded for language {lang}'
                payload['errors'] = [msg]
                self.logger.error(msg)

        except MatchPatternError as err:
            payload["success"] = False
            msg = f"Error registering pattern for PhraseMatcher {call_back}: {err}"
            payload["errors"] = [msg]
            self.logger.error(msg)
        return payload

    def match_tokens(self, sentence: str, lang_code:str):
        domain = None
        tokens = []
        if lang_code == 'en':
            nlp = self.nlp['en']
            doc = nlp(sentence)
            matcher = self.token_matcher['en']
            matches = matcher(doc)
        else:
            nlp = self.nlp['no'] # Norwegian is default vocab
            doc = nlp(sentence)
            matcher = self.token_matcher['no']
            matches = matcher(doc)
        # Match tokens
        if len(matches) > 0:
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]  # Get string representation
                span = doc[start:end]  # The matched span
                tokens.append(Match(match_id, string_id,span).to_dict())
                call_back = string_id
                n = call_back.find('/')
                if n < 0 :
                    self.logger.error(f'The callback {call_back} has no domain qualifier')
                    domain = call_back
                else:
                    domain = call_back[0:n]
            payload = {'success': True, 'sentence': sentence, 'lang': lang_code, 'call_back': call_back,
                       'domain': domain, 'matches': tokens}
        else:
            payload = {'success':False, 'sentence':sentence, 'lang':lang_code}
            self.logger.debug('Matcher: No match on {} for language code {}'.format(sentence, lang_code))
        return payload

    def match_phrases(self, sentence: str, lang_code:str):
        domain = None
        tokens = []
        if lang_code == 'en':
            nlp = self.nlp['en']
            doc = nlp(sentence)
            matcher = self.phrase_matcher['en']
            matches = matcher(doc)
        else:
            nlp = self.nlp['no'] # Norwegian is default vocab
            doc = nlp(sentence)
            matcher = self.phrase_matcher['no']
            matches = matcher(doc)
        # Match tokens
        if len(matches) > 0:
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]  # Get the string representation
                span = doc[start:end]  # The matched span
                tokens.append(Match(match_id, string_id,span).to_dict())
                domain = string_id
            payload = {'success': True, 'sentence': sentence, 'lang': lang_code, 'domain': domain,
                       'matches': tokens}
        else:
            payload = {'success':False, 'sentence':sentence, 'lang':lang_code}
            self.logger.debug('PhrseMatcher: No match on {} for language code {}'.format(sentence, lang_code))
        return payload


    def match_skill(self, sentence: str, lang_code: str) -> dict:
        ''' The skill matcher will match the phrases in the sentence to determine the domain.
            Then the tokens will be matched to determine the domain method'''
        result = self.match_phrases(sentence, lang_code)
        domain = "Unknown"
        if result['success'] is True:
            domain = result['domain']
            method = self.match_tokens(sentence, lang_code)
            if method['success'] is True:
                payload = method
            else:
                err = f'No matching call back in {sentence} for the domain {domain}'
                payload = {'success': False, 'sentence': sentence, 'errors': [err]}
                self.logger.debug(err)
        else:
            err = f'Match skill: No matching skill for  {domain} in {sentence}'
            self.logger.debug(err)
            payload = {'success': False, 'sentence': sentence, 'errors': [err]}
        return payload


class LanguageProcessor:

    def __init__(self, logger):
        self.logger = logger
        self.trained_modules = {}
        # SKip the Norwegian vocab as we translate to English before processing
        # self.trained_modules['no'] = "trained_modules/nb_core_news_lg"
        self.trained_modules['en'] = "trained_modules/en_core_web_lg"  # Use the medium size vocab for improved accuracy
        self.nlp = {} # The nlp vocabs, one for each trained language
        # Load the nlp vocab modules
        self.load_modules()
        self.fasttext_model = 'trained_modules/lid.176.bin'
        self.logger.info('Loading fasttext module {}'.format(self.fasttext_model))
        # The skills matcher
        self.skill = SkillMatcher(self.nlp, self.logger)
        # The language translator
        self.trl = MyTranslator(from_lang='no', to_lang='en')
        # Load custom pipe-lines
        #self.load_custom_pipelines() #ToDo need to understand pipelines better
        # Output Spacy meta
        for lang in self.trained_modules:
            meta = self.meta(lang)
            self.logger.debug(f'Spacy Metadata for lang {lang}')
            for key in meta:
                self.logger.debug(f'Key {key}, Value: {meta[key]}')

    def load_custom_pipelines(self):
        # Load the custom pipe lines
        for lang in self.nlp:
            nlp = self.nlp[lang]
            nlp.add_pipe("skills_pipeline", config={"label": "SKILL"})
        self.logger.debug('Loaded custom pipelines')
        return

    def load_modules(self):
        for lang in self.trained_modules:
            self.logger.info('Loading module {}'.format(self.trained_modules[lang]))
            self.nlp[lang] = spacy.load(self.trained_modules[lang])
        return

    def register_skill(self, domain: str, call_back: str, lang: str, patterns):
        ''' Register a Matcher pattern '''
        return self.skill.register_skill(domain, call_back, lang, patterns)

    def register_domain(self, domain: str, lang: str, phrases):
        ''' Register a PhraseMatcher pattern '''
        return self.skill.register_skill_domain(domain, lang, phrases)

    def meta(self, lang: str):
        ''' Returns all the Spacy metadata '''
        if lang in self.nlp:
            meta = self.nlp[lang].meta
            spacy = SpacyMeta()
            payload = spacy.to_dict(meta)
        else:
            self.logger.error('No language module for {} loaded'.format(lang))
            payload = {'success': False}
        return payload

    def translate(self, sentence: str)-> str:
        return self.trl.translate(sentence)

    def language(self, msg: str):
        # load the fasttext pre-rained model for language detection
        fmodel = fasttext.load_model(self.fasttext_model)
        pred = fmodel.predict(msg)
        label = pred[0][0]
        pred =  pred[1][0]
        isocode = label.replace('__label__','')
        lang = language_name(isocode)
        payload = {
            "language": lang,
            "isocode": isocode,
            "prediction": pred
        }
        return payload

    def is_english(self, msg):
        r = self.language(msg)
        if r['isocode'] == 'en' and r['prediction'] > 0.5:
            return True
        else:
            return False

    def match_skill(self, sentence: str):
        translated = sentence
        if self.is_english(sentence) is not True:
            # Do the translation
            translated = self.translate(sentence)
        lang_code = 'en'
        payload = self.skill.match_skill(translated, lang_code)
        if payload['success'] is False:
            analysis = self.analysis(sentence)
            self.logger.debug('Language {}'.format(analysis))
        payload['translation'] = translated
        return payload

    def match_tokens(self, sentence: str):
        ''' Matcher
            Translate to English before matching'''
        translated = sentence
        if self.is_english(sentence) is not True:
            # Do the translation
            translated = self.translate(sentence)
        lang_code = 'en'
        payload = self.skill.match_tokens(translated, lang_code)
        if payload['success'] is False:
            analysis = self.analysis(sentence)
            self.logger.debug('Language {}'.format(analysis))
        payload['translation'] = translated
        return payload

    def match_phrases(self, sentence: str):
        ''' PhraseMatcher
            Translate to English before matching'''
        translated = sentence
        if self.is_english(sentence) is not True:
            # Do the translation
            translated = self.translate(sentence)
        lang_code = 'en'
        payload = self.skill.match_phrases(translated, lang_code)
        if payload['success'] is False:
            analysis = self.analysis(sentence)
            self.logger.debug('Language {}'.format(analysis))
        payload['translation'] = translated
        return payload

    def analysis(self, sentence: str):
        # Determine the language
        ''' NLP anlaysis'''
        analysis = {}
        analysis['sentence'] = sentence
        translated = sentence
        if self.is_english(sentence) is not True:
            # Do the translation
            translated = self.translate(sentence)
        nlp = self.nlp['en']
        lang = 'en'
        doc = nlp(translated)
        # Base noun phrases
        noun_phrase = [chunk.text for chunk in doc.noun_chunks]
        # Named entities
        named_entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        # Tokens
        tokens = []
        lemma =[]
        pos =[]
        tag = []
        dep =[]
        shape = []
        alpha = []
        stop = []
        tokens = [{'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_, 'tag': token.tag_, 'dep': token.dep_,
                   'shape': token.shape_, 'alpha': token.is_alpha, 'stop': token.is_stop,
                   'explanation': spacy.explain(token.tag_)} for token in doc]
        analysis['language']= lang
        analysis['noun_phrase']= noun_phrase
        analysis['translation']= translated
        analysis['named_entities']= named_entities
        analysis['tokens']= tokens
        return analysis

@Language.factory("skills_pipeline")
class JeevesSkills:
    def __init__(self, nlp, name, label="SKILL"):
        r = requests.get("https://restcountries.eu/rest/v2/all")
        r.raise_for_status()  # make sure requests raises an error if it fails
        countries = r.json()
        # Convert API response to dict keyed by country name for easy lookup
        self.countries = {c["name"]: c for c in countries}
        self.label = label
        # Set up the PhraseMatcher with Doc patterns for each country name
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add("SKILLS", [nlp.make_doc(c) for c in self.countries.keys()])
        # Register attributes on the Span. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Span.set_extension("jenkins_skill", default=None, force = True)
        #Span.set_extension("country_capital", default=None)
        #Span.set_extension("country_latlng", default=None)
        #Span.set_extension("country_flag", default=None)
        # Register attribute on Doc via a getter that checks if the Doc
        # contains a country entity
        Doc.set_extension("jenkins_has_skill", getter=self.jenkins_has_skill, force= True)

    def __call__(self, doc):
        spans = []  # keep the spans for later so we can merge them afterwards
        for _, start, end in self.matcher(doc):
            # Generate Span representing the entity & set label
            entity = Span(doc, start, end, label=self.label)
            # Set custom attributes on entity. Can be extended with other data
            # returned by the API, like currencies, country code, calling code etc.
            entity._.set("jenkins_skill", True)
            #entity._.set("country_capital", self.countries[entity.text]["capital"])
            #entity._.set("country_latlng", self.countries[entity.text]["latlng"])
            #entity._.set("country_flag", self.countries[entity.text]["flag"])
            spans.append(entity)
        # Overwrite doc.ents and add entity – be careful not to replace!
        doc.ents = list(doc.ents) + spans
        return doc  # don't forget to return the Doc!

    def jenkins_has_skill(self, doc):
        """Getter for Doc attributes. Since the getter is only called
        when we access the attribute, we can refer to the Span's 'is_skill'
        attribute here, which is already set in the processing step."""
        return any([entity._.get("jenkins_skill") for entity in doc.ents])

