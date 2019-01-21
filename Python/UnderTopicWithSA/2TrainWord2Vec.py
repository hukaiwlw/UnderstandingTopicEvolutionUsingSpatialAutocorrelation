from gensim.models import word2vec

###
#2.training the word2vec model
# input the keyword lists and abstract(en1AB)
# output the word2vec model
# Caution:
# we have already the word2vec model trained.
###
dirABST = "D:/publications/GitWksp/WoSdata/naturalhazard/en1ABST.txt"
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirABReST= "D:/publications/GitWksp/WoSdata/naturalhazard/en1ABReST.txt"
# the two-dimensional keyword points after dimension reduction.
sentences=word2vec.Text8Corpus(dirABReST)
model=word2vec.Word2Vec(sentences,sg=0,min_count=1)
model.save(dir+"w2v.m")
# load the word2vec using the following sentence
# model=word2vec.Word2Vec.load(dir+"w2v.m")
