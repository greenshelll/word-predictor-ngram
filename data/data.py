
import pandas as pd
import nltk
from collections import Counter
import re
from nltk.util import ngrams
# corpus

#from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import conll2000, \
    conll2002, nps_chat


def set_data(data_tokenized):
    data_tokenized = pd.Series(data_tokenized)

    def pureWord(word):  # must contain atleast 1 letter
        if len(re.findall(string=word, pattern='[a-zA-Z]+')) <= 0:
            return False
        else:
            return True
    # include only elements that has atleast 1 letter
    data_tokenized = data_tokenized[data_tokenized.apply(pureWord)]
    print('data cleaned')

    for x in range(1, 4):
        title = f'{x}gram'
        print(title, 'on queue')
        data = pd.Series(Counter(ngrams(data_tokenized, x))).to_frame()
        print(data)
        data.to_pickle('data/{}.pkl'.format(title))
        print(title, 'created')

    # bigram.to_csv('bigram.csv')
    # trigram.to_csv('trigram.csv')
    # unigram.to_csv('unigram.csv')
    print('success')


nltk.download('conll2000')
nltk.download('conll2002')
# ltk.download('inaugural')
# nltk.download('genesis')
'''nltk.download('product_reviews_1')
nltk.download('product_reviews_2')'''
nltk.download('nps_chat')
# nltk.download('gutenberg')
nltk.download('brown')
# nltk.download('gutenberg')

'''
lis_gutenberg = ['austen-emma.txt', 'austen-persuasion.txt', 'austen-sense.txt', 'bible-kjv.txt',
                 'blake-poems.txt', 'bryant-stories.txt', 'burgess-busterbrown.txt',
                 'carroll-alice.txt', 'chesterton-ball.txt', 'chesterton-brown.txt',
                 'chesterton-thursday.txt', 'edgeworth-parents.txt', 'melville-moby_dick.txt',
                 'milton-paradise.txt', 'shakespeare-caesar.txt', 'shakespeare-hamlet.txt',
                 'shakespeare-macbeth.txt', 'whitman-leaves.txt']
'''
print('starting')
print('gathering corpus')
# add data as list containing each word
elements_words = [] + list(brown.words())+list(nps_chat.words())

'''for x in lis_gutenberg:
    elements_words = elements_words + list(gutenberg.words(x))
print('corpus arranged')
# process'''
set_data(elements_words)
