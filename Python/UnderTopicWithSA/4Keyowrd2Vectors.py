import WoSdataparser
from gensim.models import word2vec
from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
###
#4. transfer the keyword collections into the word vectors
###
dir="D:/publications/GitWksp/WoSdata/ngeo/"
dirbk="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirDEST=dir+"cu1DECOST.txt"
dirKeywordList=dir+"keywordlist.csv"
model=word2vec.Word2Vec.load(dirbk+"w2v.m")
corpus1=WoSdataparser.load_from_file(dirDEST)
strlist=corpus1.split(" ")
## remove the repeative keywords
strlist=list(set(strlist))
listres=[]
listtext=[]
# np.zeros((num_features,), dtype="float32")
tm_a=[0.0]*100
count_err=0
for stritem in strlist:
    count=0.0
    sts1 = []
    try:
        if "_" in stritem:  # compute the average of the word vectors
            sts1 = np.array(stritem.split("_"))
            for st in sts1:
                tm_a +=np.add(tm_a,model[st])
                count+=1
            tm_a =np.divide(tm_a,count)
            print(model[st])
            print(tm_a)
            listres.append(tm_a)
            listtext.append(stritem)
        else:
            tm_a = model[stritem]
            # print("size:" + str(len(np.array(model[stritem]))))
            listres.append(tm_a)
            listtext.append(stritem)
    except:
        count_err+=1
        print("error"+str(count_err)+":"+stritem)

X_tsne = TSNE(learning_rate=100).fit_transform(listres)
keywordList=[]
count=0
for eachkeyword in listtext:
    keywordXY = []
    keywordXY.append(eachkeyword)
    keywordXY.append(10000*X_tsne[count,0]+100000)
    keywordXY.append(10000*X_tsne[count,1]+100000)
    count=count+1
    keywordList.append(keywordXY)
df=pd.DataFrame(keywordList,columns=["keyword", "X", "Y"])
#dirKeywordList=dir+"keywordlist.csv"
df.to_csv(dirKeywordList)