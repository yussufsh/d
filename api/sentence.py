'''
Created on Feb 25, 2017

@author: manish_kelkar
'''
import nltk
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from nltk.parse.generate import generate, demo_grammar

from nltk import CFG
import sys

class SentenceGenerator(object):
    '''
    classdocs
    '''


    def generate_sentence(self,words_list):
        start = time.time()
        #words_list
        #for i in sys.argv[1:]:
        #   sentence=words_list+" "+str(i)
        words=""
        evaluator={}
#        words_list=[{u'yard': 96.20924377441406}, {u'golf course': 96.03392791748047}, {u'grassland': 96.03392791748047}, {u'birds': 90.010524}]
#        words_list=[{u'yard': 96.20924377441406}, {u'golf course': 06.03392791748047}, {u'grassland': 16.03392791748047}]
        for word in words_list:
            new_word=word.keys()[0].replace(' ','_')
            evaluator[new_word]=word[word.keys()[0]]
            words=words+" "+word.keys()[0].replace(' ','_')
        #print words
        words_list=words
        
        #print evaluator
        if 'people' in words_list:
            words_list=words_list.replace('person','')
            #words_list=words_list.replace('man','')
            words_list=words_list.replace('human','')
        if 'computer' or 'phone' or 'mobile' or 'laptop' in words_list:
            words_list=words_list.replace('electronics','')
        
        #print "Tokenize the words"
        tokens = nltk.word_tokenize(words_list)
        #print tokens
        
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)
        
        print tagged
        #print "entities"
        #print entities
        
        #print "Default grammar"
	grammar="""
            S -> NP
            NP -> Det 'a' N
            NP -> Det 'some' NNS
            NP -> Det 'a' N ',' 'a' N
            NP -> Det 'a' N ',' 'a' N 'and' 'a' N
            NP -> Det 'a' N ',' N 'and' N
            NP -> Det 'a' N ',' N ',' N 'and' N
            NP -> Det 'a' N ',' N ',' N ',' N 'and' N
            NP -> Det 'a' N ',' N ',' N ',' N ',' N 'and' N
            NP -> Det 'a' N ',' N ',' N ',' N ',' N ',' N 'and' N
            NP -> Det 'a' VBG
            NP -> Det 'a' VBG 'and' 'a' N
            NP -> Det 'some' NNS ',' N 'and' N
            NP -> Det 'some' NNS ',' N ',' N 'and' N
            NP -> Det 'some' NNS 'or' NNS
            Det -> 'I see'
        """
        
        found_NNS= False
        found_NN= False
        found_VBG= False
        
        #Filter out plurals        
        for plural_nouns in tagged:
           if plural_nouns[1] == 'NNS':
               if not found_NNS:
                   grammar=grammar+"NNS -> '" + plural_nouns[0] +"'"
                   found_NNS= True
               else :
                   grammar=grammar+" | '"+ plural_nouns[0]+"'"
        # Filter out singular
        for singular_nouns in tagged:
           if singular_nouns[1] == 'NN' or (singular_nouns[1] != 'NNS' and singular_nouns[1] !='VBG' and singular_nouns[1] !='VBP') :
               if not found_NN:
                   grammar=grammar+"\n N -> '" + singular_nouns[0]+"'"
                   found_NN= True
               else :
                   grammar=grammar+" | '"+ singular_nouns[0]+"'"
        # filter out others
        for vbg in tagged:
            if vbg[1] == 'VBG':
                 if not found_VBG:
                     grammar=grammar+" \n VBG -> '"+vbg[0]+"'"
                 else:
                    grammar=grammar+" | '"+ vbg[0]+"'"
        #print "new gram:"
        #print grammar
        #print tagged
        #print grammar
        gram=CFG.fromstring(grammar)
        #print gram.productions()
        
        # check for vowels and adjust a/an
        vowel = 'a', 'e', 'i', 'o', 'u'
        weight=[]
        output=[]
        for sentence in generate(gram, n=1000):
            word=0
            value = 0
            valid = False
            while word < len(sentence):
                if sentence[word] == 'a' and sentence[word+1].startswith(vowel):
                    sentence[word] = 'an'
                value = value + evaluator.get(sentence[word], 0)
                #print evaluator.get(word, 0)
                word+=1
            check_duplicate=words_list.split()
            duplicate= False  
            for i in check_duplicate:
                if sentence.count(i) > 1:
                    duplicate= True
                    break
             
            if not duplicate: 
                output.append(sentence)
                weight.append(value)
          
        # print the most valid sentence
        #print output
        m = max(weight)
        maximum= [i for i, j in enumerate(weight) if j == m]
        end = time.time()
        logger.info("Time taken by Grammar: " + str(end - start))
        text= ' '.join(output[maximum[0]])
        text= text.replace('_',' ')
        return text 

 
#            if len(set_value) == len(sentence):
#                print sentence
            #print "value" + str(value)
