import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import nltk
# nltk.download("book")
from nltk import ngrams
from string import punctuation

# List of gutenberg corpus
# print(gutenberg.fileids())

# List of alphabet
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# String of punctuation
# 0123456789 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
punc = ' ' + punctuation + '\n'
punc = '0123456789' + punc

# Alice's Adventures in Wonderland by Lewis Carroll 1865
alice_raw = nltk.corpus.gutenberg.raw("carroll-alice.txt")
alice_raw = alice_raw.lower()
print("length of the book 'Alice's Adventures': " + str(len(alice_raw)))       # Count all letters in alice data


''' 1. Probability distribution over the 27 outcomes for a randomly selected letter '''
print("### Probability distribution over the 27 outcomes for a randomly selected letter ###")

# For letter X in alphabets and punctuations, compute P(X=x)
# Probability for each alphabet letter
for letter in alphabet:
    letter_prop = round(alice_raw.count(letter) / len(alice_raw), 5)
    # print(letter + ": " + str(letter_prop))
    print(letter + ": " + str(letter_prop) + " / " + str(alice_raw.count(letter)))

# Probability for numbers, whitespace, enter, and punctuation
countFunc = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
punc_prop = round(countFunc(alice_raw, punc) / len(alice_raw), 5)
# print('-' + ": " + str(punc_prop))
print(' ' + ": " + str(punc_prop) + " / " + str(countFunc(alice_raw, punc)))


print()
''' 2. Probability distribution over the 27x27 possible bigrams xy (Marginal probability) '''
print("### Probability distribution over the 27x27 possible bigrams xy (Marginal probability) ###")
alice_bigram = list(ngrams(alice_raw, 2))

# Change all punctuations to ' ' in bigram
alice_bigram_list = []
for ele in alice_bigram:
    ele = list(ele)
    if ele[0] in punc:
        ele[0] = '-'
    if ele[1] in punc:
        ele[1] = '-'
    alice_bigram_list.append(tuple(ele))

# Compute frequencies for bigrams
cfd = nltk.ConditionalFreqDist(alice_bigram_list)
cfd.tabulate()    # frequencies

# Compute probability for bigrams (Marginal probability)
# For ordered pair XY, compute P(X=x, Y=y)
conditions = sorted(cfd.conditions())
conditions = conditions[1:]
conditions.append('-')

bigramPropTable = np.zeros((27, 27))
for x in range(0, 27):
    for y in range(0, 27):
        bigramPropTable[x][y] = cfd[conditions[x]][conditions[y]] / cfd.N()

bigram_df = pd.DataFrame(bigramPropTable, index=conditions, columns=conditions)
print(bigram_df)


print()
''' 3. Conditional probability distributions over P(y|x) and P(x|y) '''
print("### Conditional probability distributions over P(y|x) and P(x|y) ###")
#  3-1. P(y|x)
# For ordered pair XY, compute P(Y=y|X=x) = P(X=x, Y=y) / P(X=x)
cpd = nltk.ConditionalProbDist(cfd, nltk.MLEProbDist)
cpd_yx_table = np.zeros((27, 27))

for x in range(0, 27):
    for y in range(0, 27):
        # print("(" + conditions[x] + ", " + conditions[y] + ") :" + str(cpd[conditions[x]].prob(conditions[y])))
        cpd_yx_table[x][y] = cpd[conditions[x]].prob(conditions[y])

cpd_yx_df = pd.DataFrame(cpd_yx_table, index=conditions, columns=conditions)
print("* P(y|x) table")
print(cpd_yx_df)


# 3-2. P(x|y)
# For ordered pair XY, compute P(X=x|Y=y) = P(X=x, Y=y) / P(Y=y)
cpd_xy_table = np.zeros((27, 27))
for x in range(0, 27):
    for y in range(0, 27):
        if (y == 26):        # punctuation
            cpd_xy_table[x][y] = cfd[conditions[x]][conditions[y]] / countFunc(alice_raw, punc)
        else:               # alphabet
            cpd_xy_table[x][y] = cfd[conditions[x]][conditions[y]] / alice_raw.count(alphabet[y])

cpd_xy_df = pd.DataFrame(cpd_xy_table, index=conditions, columns=conditions)
print("* P(x|y) table")
print(cpd_xy_df)


''' To Do '''
# 1. Probability distribution over the 27 outcomes for a randomly selected letter
# fd = nltk.probability.FreqDist(alice_raw)
# print(fd.N())   # Count all letters in alice data
# print(fd['a'])  # Count 'a' letters in alice data

# 2. Probability distribution over the 27x27 possible bigrams xy

# 3. Conditional probability
#  3-1. P(y|x)
#  3-2. P(x|y)