# word-predictor-ngram
testing practical application of n-gram probability by predicting the words from data obtained on nltk corpus (brown and nps chat)


N-Gram Models
One of the oldest methods used in trying to compute the probability that a given word is the next word in a sentence is employing n-gram models. N-gram models are attempts to guess the next word in a sentence based upon the (n - 1) previous words in the sentence. These models base their guesses on the probability of a given word without any context (i.e., the is a more common word than green and is thus more probable than green if context is ignored) and the probability of a word given the last (n – 1) words. 

- the program contains methods that predicts the possible next word or multiple next words via probability chain rule.
- the dataset is very limited and for experimental use only. An autocorrection method was used via Lavenshtein Min Edit Distance Algorithm to search for the closest word available to the dataset.
