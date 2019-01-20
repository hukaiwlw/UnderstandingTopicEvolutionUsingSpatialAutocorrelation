import WOSparser
###
#4. transfer the keyword collections into the word vectors
###
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirDEST=dir+"cu1DECOST.txt"
dirKeywordList=dir+"keywordlist.csv"
corpus1=WOSparser.load_from_file(dirDEST)
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
        if "_" in stritem:  # 对某些phrase去平均
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
        print("in the error"+str(count_err)+":"+stritem)

X_tsne = TSNE(learning_rate=100).fit_transform(listres)
keywordXY=[]
keywordList=[]
count=0
for eachkeyword in listtext:
    keywordXY.append(eachkeyword)
    keywordXY.append(X_tsne[count,0])
    keywordXY.append(X_tsne[count,1])
    count=count+1
    keywordList.append(keywordXY)
df=pd.DataFrame(keywordList,columns=["keyword", "X", "Y"])
df.to_csv(dirKeywordList)