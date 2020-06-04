# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:02:31 2019

@author: LIM YUAN QING

Module contains classes and functions that aims to combine functionalities from 
different libraries (nltk, spacy, textblob etc...) to automate process of 
text mining / sentiment analysis for the purposes of Syntactic Analysis and 
Semantic Analysis
1. tokenization
2. part of speech tagging
3. hyponyms/hypernyms determination
4. 

Corpus (collection of documents) -> Document (collection of sentences)
    -> Sentence (collection of tokens) -> Token (collection of words) -> Word

NLP Workflow
1.  Parsing and tokenizing text data
    -   ngrams
2.  Linguistic annotation
    -   POS annotations: disambiguate tokens based on their function
    -   Dependency parsing: identifies hierarchical relationships among tokens
    -   Stemming: uses simple rules to remove common endings
    -   Lemmatization: derive canonical root (lemma) of a word
3.  Semantic annotation
    -   Named entity recognition (NER): identify tokens that represent objects 
        of interest (can be further developed into a knowledge graph)
4.  Document modelling
    -   Determine how to quantify sentiments implict in a text document
    -   Determine which aspects of a text document to assign to a specific outcome
5.  Document labelling
6.  Data enrichment
7.  Predictive modelling

Key Definitions
1.  Tokenization: Segments text into words, punctuation markets, and so on
2.  POS tagging: Assigns word types to tokens, such as verb or noun
3.  Dependency parsing: Labels syntactic token dependencies, such as subject <-> object
4.  Stemming and lemmatization: Assigns the base forms of words (rats->rat)
5.  Sentence boundary detection: Finds and segments individual sentences
6.  Named entity recognition: Labels real-world objects, such as people, companies
7.  Similarity: Evaluates the similarity of words, text spans, and documents

Challenges of NLP
1.  Ambiguity due to polysemy (a word or phrase having different meanings depending
    on context)
2.  Non-standard and evolving use of language, especially in social media
3.  Use of idioms (throw in the towel)
4.  Tricky entity names (Where is A Bug's Life playing)
5.  Knowledge of the world (Mary and Sue are sisters vs Mary and Sue are mothers)

Classes
-------


"""
#import sys
##sys.path.append(r'E:\Dropbox\Yuan Qing\Work\Projects\Libraries\3. Python\1. Modules\dd8')
#sys.path.append(r'C:\Users\kaiee\Dropbox\Yuan Qing\Work\Projects\Libraries\3. Python\1. Modules\dd8')

import nltk
nltk.download('wordnet')
nltk.download('omw')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import words as wd

import numpy as np
import spacy
import textblob
import re

import dd8.data_science.nlp_data as nlp_data
import dd8.data_science.enums as enums
import dd8
import dd8.utility.utils as utils

logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)


class Dictionary():
    ## load various sources of word dictionaries and their respective scores
    def __init__(self, enum_dictionary_source, 
                 enum_language):
        self.source = enum_dictionary_source
        self.language = enum_language        
        
    def get_words(self):
        if self.source == enums.ENUM_DICTIONARY_SOURCE.NLTK_WORDS:
            if self.language == enums.ENUM_LANGUAGE.ENGLISH:
                return wd.words()

# 1. [done] Spell-check
# 2. Lemmatization replace custom words
# 3. [done] contract_expansions (done)
# 4. SA
# 5. Lemmatization from various package
# 6. Add official detokenizer instead of using ' '.join()
# TreebankWordDetokenizer().detokenize(['the', 'quick', 'brown'])
class Document(object):
    """
    Each instance represents a document within a corpus. This is in line with
    the hierachy as defined in the module documentation (Corpus -> Document ->
    Sentence). Provides convenience functions to process text documents that 
    can be interpreted as a complete text passage. The purpose is to aggregate
    and analyze `Sentence` objects to derive insights/predictions.
    """
    def __init__(self, str_content='', enum_language=None, enum_nlp_package=None):        
        self.__enum_language = enum_language
        self.__enum_nlp_package = enum_nlp_package        
        self.sentences = str_content        
    
    @property
    def language(self):
        return self.__enum_language
    
    @property
    def package_for_tokenization(self):
        return self.__enum_nlp_package
    
    @property
    def sentences(self):
        return self.__gen_sentences
    
    @sentences.setter
    def sentences(self, gen_sentences_new):
        if gen_sentences_new:
            self.__gen_sentences = self.tokenize(gen_sentences_new, 
                                                 self.package_for_tokenization)
        else:
            self.__gen_sentences = None
        
    @property
    def sentiment(self):
        polarity = []
        subjectivity = []
        for sent in self.sentences:
            sentiment = sent.sentiment
            polarity.append(sentiment[0])
            subjectivity.append(sentiment[1])
        return (np.mean(polarity), np.mean(subjectivity))
    
    def tokenize(self, str_content, enum_nlp_package=None):
        if not enum_nlp_package:
            enum_nlp_package = enums.ENUM_NLP_PACKAGE.NLTK
        if enum_nlp_package == enums.ENUM_NLP_PACKAGE.NLTK:
            return [Sentence(sent.replace('\n',''), self.language) 
                        for sent in sent_tokenize(str_content)]            
        else:
            return [Sentence(sent.text.replace('\n',''), self.language) 
                        for sent in spacy.load('en_core_web_sm')(str_content).sents]
    
    def from_txt(self, str_full_file_path):              
        with open(str_full_file_path, 'r', encoding='utf8') as f:
            str_content = str(f.read())        
        self.sentences = str_content
        return self.sentences
    
    def from_csv(self):
        pass
    
    def from_html(self):
        pass
    
    def from_file(self, str_file_path, str_file_format, str_decoder='utf-8'):
        pass
            
class Sentence(object):
    """
    Each instance represents a sentence within a document. This is in line with
    the hierachy as defined in the module documentation (Corpus -> Document ->
    Sentence). Provides convenience functions to process text data that can 
    be interpreted as a sentence within a `Document` object. The purpose is 
    to provide cleaned text data ready for aggregation on a `Document` level
    for further analysis/modelling, such as sentiment analysis.
    
    Default Workflow
    1.  Spellcheck
    2.  Named entity recognition (NER)
    2.  Lemmatization
    3.  ngram with frequency filter for significance
        -   keep if found through NER
        -   for the remaining group of tokens, keep if min_freq reached
    
    Attributes
    ----------
    content
    language
    
    Methods
    -------
    tokenize
        Tokenization of a sentence to tokens using `nltk.tokenize.word_tokenize`.
    """
    def __init__(self, str_content, enum_language=None):
        self.__str_content = str_content
        if not enum_language:
            self.__enum_language = enums.ENUM_LANGUAGE.ENGLISH
        else:
            self.__enum_language = enum_language
    
    def __str__(self):
        return self.content
    
    def __repr__(self):
        pass
    
    def __len__(self):
        return len(self.content)
        
    @property
    def content(self):
        return self.__str_content
    
    @content.setter
    def content(self, str_content_new):
        self.__str_content = str_content_new
    
    @property
    def language(self):
        return self.__enum_language  
    
    @property
    def named_entities(self):
        return self.named_entity_recognition()
    
    @property
    def named_entities_by_type(self):
        output = dict()
        for ent in self.named_entities:
            if ent[1] in output:
                if ent[0] in output[ent[1]]:
                    output[ent[1]][ent[0]].append((ent[2]. ent[3]))
                else:
                    output[ent[1]][ent[0]] = [(ent[2], ent[3])]
            else:
                output[ent[1]] = {ent[0]:[(ent[2], ent[3])]}
        return output
    
    @property
    def sentiment(self):
        return textblob.TextBlob(self.content).sentiment
        
    def spell_check(self, bln_auto_correct=False):
        """
        Performs spell check using `TextBlob.correct()`, which is based on Peter
        Norvig's "How to Write a Spelling Corrector" as implemented in the pattern
        library.
        
        Parameters
        ----------
        bln_auto_correct : bool, optional
            To autocorrect `self.content` (the default is False, which implies
            `self.content` is not automaticlly corrected with the proposed spelling).
            
        Return
        ------
        tup
            tuple containing the original and corrected text for comparison,
            with (original, corrected) structure.
        """
        str_original = self.content
        str_corrected = str(textblob.TextBlob(self.content).correct())
        if bln_auto_correct:
            self.content = str_corrected
        return (str_original, str_corrected)
    
    def named_entity_recognition(self, enum_nlp_package=None):
        """
        Performs named entity recognition on `self.content`.
        
        Parameters
        ----------
        enum_nlp_package : {ENUM_NLP_PACKAGE.NLTK, ENUM_NLP_PACKAGE.SPACY}, optional
            Indicates the NLP package to perform named entity recognition (the
            default value is ENUM_NLP_PACKAGE.SPACY which implies that the 
            `Doc.ents` property is used)
            
        Yields
        ------
        tup
            tuple of the structure (text, label, start_pos, end_pos).
        """
        if not enum_nlp_package:
            enum_nlp_package = enums.ENUM_NLP_PACKAGE.SPACY
        if enum_nlp_package == enums.ENUM_NLP_PACKAGE.SPACY:
            return ((ent.text, ent.label_, ent.start_char, ent.end_char)
                    for ent in spacy.load('en_core_web_sm')(self.content).ents)
    
    def tokenize(self):
        """
        Tokenization of a sentence to tokens using `nltk.tokenize.word_tokenize`.        
        
        Key considerations when performing tokenization (trade-off between accurate
        reflection of text source vs larger vocabulary that may translate into
        more features and higher model complexity)
        1.  Treatment of punctuation and capitalization
        2.  Spelling correction
        3.  Whether to exclude stop words as meaningless noise
        
        The above considerations have a direct impact on the creation of n-grams.        
           
        Return
        ------
        list
            a list of tokens
        """
        return word_tokenize(self.content)   
    
    def ngram(self, n):
        """
        Generate a n-gram. The creation of ngrams is highly dependent on the
        extent of preprocessing done on the original text data prior to its 
        generation, such as spelling correction, and whether stop words are 
        excluded.
        
        While the generation of ngrams with the original text data will likely
        generate the largest number of features for modelling, this will likely
        add unnecessary noise to the modelling process unless ngrams are 
        filtered for significance (using dictionaries or a comparison of relative 
        frequencies of the individual and joint usage)
        
        Parameters
        ----------
        n : int
            number of tokens per n-gram
        
        Return
        ------
        
        """        
        pass
    
    def tag_part_of_speech(self):
        """
        Part-of-speech tagging to disambiguate tokens based on their function, 
        such as when a verb and noun have the same form.
        """
        return nltk.pos_tag(self.tokenize())
    
    def get_synset(self, str_word, str_pos):
        pass
    
    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('N'):
            return wn.NOUN
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            return ''
        


    def contract_expansions(self, dic_expansion_mapping=None):
        if not dic_expansion_mapping:
            dic_expansion_mapping = nlp_data.DIC_EXPANSION_MAP
        
        expansions_pattern = re.compile('({})'.format('|'.join(dic_expansion_mapping.keys())), 
                                          flags=re.IGNORECASE|re.DOTALL)
        def contract_match(expansion):
            match = expansion.group(0)
            first_char = match[0]
            if dic_expansion_mapping.get(match):
                contracted_expansion = dic_expansion_mapping.get(match)
            else:
                contracted_expansion = dic_expansion_mapping.get(match.lower())
            contracted_expansion = first_char+contracted_expansion[1:]
            return contracted_expansion
            
        contracted_text = expansions_pattern.sub(contract_match, self.__str_content)
        #contracted_text = re.sub("'", "", contracted_text)
        self.__str_content = contracted_text
        return self.__str_content

    def expand_contractions(self, dic_contraction_mapping=None):        
        if not dic_contraction_mapping:
            dic_contraction_mapping = nlp_data.DIC_CONTRACTION_MAP
        
        contractions_pattern = re.compile('({})'.format('|'.join(dic_contraction_mapping.keys())), 
                                          flags=re.IGNORECASE|re.DOTALL)
        def expand_match(contraction):
            match = contraction.group(0)
            first_char = match[0]
            if dic_contraction_mapping.get(match):
                expanded_contraction = dic_contraction_mapping.get(match)
            else:
                expanded_contraction = dic_contraction_mapping.get(match.lower())
            expanded_contraction = first_char+expanded_contraction[1:]
            return expanded_contraction
            
        expanded_text = contractions_pattern.sub(expand_match, self.__str_content)
        expanded_text = re.sub("'", "", expanded_text)
        self.__str_content = expanded_text
        return self.__str_content
    
    def remove_special_characters(self, bln_remove_digits=False):
        if bln_remove_digits:
            pattern = r'[^a-zA-z\s]'
        else:
            pattern = r'[^a-zA-z0-9\s]'
        self.__str_content = re.sub(pattern, '', self.__str_content)
        return self.__str_content  
    
    def lemmatize(self, bln_tag_part_of_speech=True, 
                  dic_custom_lemmatization=None,
                  enum_nlp_package=None):
        if not enum_nlp_package:
            enum_nlp_package = enums.ENUM_NLP_PACKAGE.NLTK
            
        if enum_nlp_package == enums.ENUM_NLP_PACKAGE.NLTK:
            if self.__enum_language == enums.ENUM_LANGUAGE.ENGLISH:
                wnl = nltk.WordNetLemmatizer()
                if bln_tag_part_of_speech:
                    pos_taggings = self.tag_part_of_speech()
                    self.__str_content = ' '.join(
                            [wnl.lemmatize(word[0], pos=self.get_wordnet_pos(word[1])) 
                                if self.get_wordnet_pos(word[1]) else
                                wnl.lemmatize(word[0])
                                for word in pos_taggings]
                            )
                else:                
                    self.__str_content = ' '.join([wnl.lemmatize(word) for word in self.__str_content.split()])
                return self.__str_content
            else:
                logger.error('Language not supported.')
                return None
        elif enum_nlp_package == enums.ENUM_NLP_PACKAGE.SPACY:
            try:
                if self.__enum_language == enums.ENUM_LANGUAGE.ENGLISH:
                    nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
                elif self.__enum_language == enums.ENUM_LANGUAGE.GERMAN:
                    nlp = spacy.load('de_core_news_sm', parse=True, tag=True, entity=True)
                else:
                    logger.error('Language not supported.')
                    return None
                text = nlp(self.__str_content)
                self.__str_content = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
                return self.__str_content
            except:
                logger.error('Please try typing "python -m spacy download en_core_web_sm" \
                              in Anaconda Prompt with Administrator Rights.')
                
    def remove_stopwords(self, bln_is_lower_case=False, enum_nlp_package=None):
        if not enum_nlp_package:
            enum_nlp_package = enums.ENUM_NLP_PACKAGE.NLTK
        
        if enum_nlp_package == enums.ENUM_NLP_PACKAGE.NLTK:
            if self.__enum_language == enums.ENUM_LANGUAGE.ENGLISH:
                lst_stopwords = nltk.corpus.stopwords.words('english')                
                                
                tokens = self.tokenize()                
                
                tokens = [token.strip() for token in tokens]
                
                if bln_is_lower_case:
                    filtered_tokens = [token for token in tokens if token not in lst_stopwords]
                else:
                    filtered_tokens = [token for token in tokens if token.lower() not in lst_stopwords]
                
                self.__str_content = ' '.join(filtered_tokens)    
                return self.__str_content

    def remove_custom_words(self, lst_words, bln_is_case_sensitive=False):
        tokens = self.tokenize()
        if bln_is_case_sensitive:
            self.__str_content = [token for token in tokens if token not in lst_words]
        else:
            self.__str_content = [token for token in tokens if token.lower() not in 
                                  [word.lower() for word in lst_words]]
        self.__str_content = ' '.join(self.__str_content) 
        return self.__str_content
    

    
    
    
    