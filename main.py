import pandas as pd
from nltk.tokenize import word_tokenize
from rapidfuzz.distance import Levenshtein
import warnings


warnings.filterwarnings(action='ignore',)
##############################
# INITIALIZE/LOADING OF DATA
ngrams = {}
maximum_n = 3
for ngram in range(1, maximum_n+1):  # from unigram to pentagram
    ngrams[ngram] = pd.read_pickle(
        f'data/{ngram}gram.pkl').squeeze().fillna(0)  # read all grams
all_words = ngrams[1].index.values  # get unigram words
all_words = pd.Series(word[0]
                      for word in all_words)  # from tuple to word/string
################################


class PredictNextWords:
    def __init__(self, string):
        self.string = string
        self.token_string = [self.autocorrect(word)
                             for word in word_tokenize(self.string)]
        ################################

    def autocorrect(self, string):
        if (all_words == string).sum() > 0:  # words in database contain selected word
            return string  # word is alright; returns
        else:
            index = (all_words.apply(lambda word_: Levenshtein.distance(
                word_, string, weights=(2, 2, 1))).sort_values(ascending=True))  # attempts to find right word via levenshtein dist by its index
            # (insertion, deletion, substituiton)
        return all_words[index]

    def change_string(self, string):
        self.string = string
        self.token_string = [self.autocorrect(word)
                             for word in word_tokenize(self.string)]

    def autogram(self):
        length = len(self.token_string)  # for gram range
        ngram_n = maximum_n
        # range from 4-2
        gram_range = [num for num in range(2, maximum_n+1)][::-1]
        for n in gram_range:  # n-2 iterate
            # if token length less than n
            # if 3 grams, length must be >= 2
            if length < n-1:
                continue
            else:
                ngram_n = n
                break
        return ngram_n

    def next_words(self, num_words):
        # chain will require self.string to change.
        # reserve original into variable and restore in the end
        reserve_string = self.string
        probability = 1  # starting probability 100%
        string_add = ''  # for return; predicted words
        for times in range(num_words):
            # chain
            res = self.next()  # returns series
            res_p = res[0]  # proabbilty
            res_string = res.index[0]  # get string to be added
            probability = probability * res_p  # probability chain rule
            # concatenate result, >expect space at start
            string_add = string_add+' '+res_string
            # sets string to use in processing
            self.change_string(self.string+' '+res_string)
        self.change_string(reserve_string)  # restore original string
        return [string_add[1:], round(res_p, 2)]  # string,remove first space

    def next(self, ngram_n=None):  # returns of series of words and probabbility
        if ngram_n not in list(range(2, maximum_n)):  # accepted ngrams only (1-4)
            ngram_n = self.autogram()
        # kwargs[self_call] = indicator that function is called from within
        tup = tuple(self.token_string[-1*(ngram_n-1):])
        # try if tuple exists in the current data
        tuple_exists = True  # default
        try:
            ngrams[ngram_n][tup]  # test
        except KeyError:
            tuple_exists = False
        ####
        if tuple_exists == True:
            # p(C|A,B) = c(A,B,C)/c(A,B)
            # C -> next_counts, c(A,B) -> scalar
            next_counts = (ngrams[ngram_n][tup])
            scalar = ngrams[ngram_n-1][tup]
            result = next_counts/scalar
            # sort highest -lowest
            result = result.sort_values(ascending=False)
            return result
        else:
            # means tuple does not exist in database, reduces ngram by 1, recall method again
            return self.next(ngram_n-1)
    ####################


string = 'university of'
ob = PredictNextWords(string)
# predict next word, # returns a series containing likelihood based on data
print(string)
# shows series of possible next words, max 10
nexts = ob.next(ngram_n=3).head(10)
for id in range(len(nexts)):  # index by int
    print('..', nexts.index[id], f'({round(nexts[id],2)*100}%)')

print('\n')
following_words, words_prob = ob.next_words(
    num_words=4)  # shows top possible next words
print(string)
print('..', following_words, f'({round(words_prob,2)*100}%)')
