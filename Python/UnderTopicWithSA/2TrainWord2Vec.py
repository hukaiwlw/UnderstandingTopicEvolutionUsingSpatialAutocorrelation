import WOSparser
from gensim.models import word2vec

###
#2.training the word2vec model
# input the keyword lists and abstract(en1AB)
# output the word2vec model
###
dirABST = "D:/publications/GitWksp/WoSdata/naturalhazard/en1ABST.txt"
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
# the two-dimensional keyword points after dimension reduction.
# sentences=word2vec.Text8Corpus(dirABST)
# model=word2vec.Word2Vec(sentences,sg=0,min_count=1)
model=word2vec.Word2Vec.load(dir+"w2v.m")
