#write the WOS parser
# firstly, the abstract extraction
# secondly, the keywords collection extraction
# build the construct to storage the data sets for the further NLP processing
#str="D:/NatureEnvironments/Nautra harzard"
import os
import codecs
from nltk.corpus import stopwords
import nltk
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
# from MulticoreTSNE import MulticoreTSNE as TSNE

from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
from gensim.models import word2vec

def rename_download(dir):
    names=os.listdir(dir)
    for name in names:
        if name.endswith(".txt"):
            os.rename(dir+"/"+name,dir+"/"+"download_"+name)

#  through regular expression
def build_ABCorpus(dir):
    CorpusContent=""
    ABcontents=""
    count=1
    names=os.listdir(dir)
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir+name)
            fobj=codecs.open(dir+name,'r','utf-8')
            for eachline in fobj:
                ABcontents+=eachline
    ABCollections=ABcontents.split("\nAB ")
    for abblock in ABCollections:
        blockends=abblock.split("\n")
        if blockends and count>1:
            print(count)
            CorpusContent+=blockends[0]
        count += 1
    CorpusContent = CorpusContent.replace("(", "")
    CorpusContent = CorpusContent.replace(")", "")
    CorpusContent = str.lower(CorpusContent)
    return CorpusContent

# build the keyword collection
def build_DECorpus(dir):
    CorpusContent=""
    contents=""
    count=1
    names=os.listdir(dir)
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir+name)
            fobj=codecs.open(dir+name,'r','utf-8')
            for eachline in fobj:
                contents+=eachline
    CollectionsF=contents.split("\nER")
    for collf in CollectionsF:#collf为其中一个文献单元
        # print(collf)
        if "\nDE " in collf:
            Collections=collf.split("\nDE ")
        else:
            continue
        # for deblock in Collections:
        deblock=Collections[1]
        if "\nID " in deblock:
            blockends=deblock.split("\nID ")
        else:
            blockends = deblock.split("\nAB ")
        if blockends and count>1:
            print(count)
            temp = blockends[0].replace("    ", "_")
            temp = temp.replace("\n   ", "_")
            temp = temp.replace("   ", "_")
            temp = temp.replace("  ", "_")
            temp = temp.replace(" ", "_")
            temp = temp.replace(",", "_")
            temp = temp.replace(". ", "_")
            temp=temp.replace("-","_")
            temp=temp.replace("(","")
            temp=temp.replace(")","")
            temp=temp.replace("\"","")
            temp=temp.replace("'","")
            print(temp)
            strlist = temp.split(";")
            wordstring = ""
            for word in strlist:
                if word.startswith("_"):
                    word = word[1:len(word)]
                if word.endswith("_"):
                    word = word[0:len(word) - 1]
                wordstring += word
                wordstring += " "
                wordstring = wordstring.lower()
            CorpusContent +=wordstring
            CorpusContent+=" "
        count += 1
    return CorpusContent


# put all keyword from the keyword list into one file as the keyword collection
def build_DESTCorpus(dir):
    CorpusContent=""
    contents=""
    count=1
    stemmer = SnowballStemmer('english')
    names=os.listdir(dir)
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir+name)
            fobj=codecs.open(dir+name,'r','utf-8')
            for eachline in fobj:
                contents+=eachline
    CollectionsF=contents.split("\nER")
    for collf in CollectionsF:
        # print(collf)
        if "\nDE " in collf:
            Collections=collf.split("\nDE ")
        else:
            continue
        # for deblock in Collections:
        deblock=Collections[1]
        if "\nID " in deblock:
            blockends=deblock.split("\nID ")
        else:
            blockends = deblock.split("\nAB ")
        if blockends and count>1:
            print(count)
            temp = blockends[0]
            temp = temp.replace("-", "_")
            temp = temp.replace("(", "")
            temp = temp.replace(")", "")
            temp = temp.replace("\"", "")
            temp = temp.replace("'", "")
            strlist = temp.split(";")
            wordstring = ""
            for word in strlist:
                strtemp = nltk.word_tokenize(word)
                out = [stemmer.stem(wd) for wd in strtemp]
                for wds in out:
                    wordstring += wds + "_"
                wordstring=wordstring[0:len(wordstring)-1]
                wordstring+=" "
            CorpusContent +=wordstring
        count += 1
    return CorpusContent

#generating keyword -author -school -journal pairs
def GenerateTRef(dir):
    contents = ""
    count = 1
    ftuple=[]
    stemmer = SnowballStemmer('english')
    names = os.listdir(dir)
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                contents += eachline
    CollectionsF = contents.split("\nER")
    for collf in CollectionsF:  # collf as one unit
        wordAU=""
        wordPY=""
        wordCR=""
        wordCT=""
        wordDE=""
        ftupleunit = []
        if "\nAU " in collf:
            Collections = collf.split("\nAU ")
        deblock = Collections[1]
        if "\n" in deblock:
            blockends = deblock.split("\n")
        if blockends:
            print(count)
            wordAU = blockends[0].replace(",","")

        if "\nPY " in collf:
            Collections = collf.split("\nPY ")
        else:
            continue
        deblock = Collections[1]
        if "\n" in deblock:
            blockends = deblock.split("\n")
        if blockends:
            wordPY = blockends[0]
            print(wordPY)
        wordAP=wordAU+", "+wordPY
        ftupleunit.append(wordAP)
        ftupleunit.append(wordPY)
        if "\nCR " in collf:
            Collections = collf.split("\nCR ")
        else:
            continue
        deblock = Collections[1]
        if "\nNR " in deblock:
            blockends = deblock.split("\nNR ")
        if blockends:
            wordCR = blockends[0]
        ftupleunit.append(wordCR)

        if "\nTC " in collf:
            Collections = collf.split("\nTC ")
        deblock = Collections[1]
        if "\n" in deblock:
            blockends = deblock.split("\n")
        if blockends:
            wordCT = blockends[0]
        ftupleunit.append(wordCT)

        if "\nDE " in collf:
            Collections = collf.split("\nDE ")
        else:
            continue
        # for deblock in Collections:
        deblock = Collections[1]
        if "\nID " in deblock:
            blockends = deblock.split("\nID ")
        else:
            blockends = deblock.split("\nAB ")
        if blockends :
            temp = blockends[0]
            temp = temp.replace("-", "_")
            temp = temp.replace("(", "")
            temp = temp.replace(")", "")
            temp = temp.replace("\"", "")
            temp = temp.replace("'", "")
            strlist = temp.split(";")
            wordstring = ""
            for word in strlist:
                strtemp = nltk.word_tokenize(word)
                out = [stemmer.stem(wd) for wd in strtemp]
                for wds in out:
                    wordstring += wds + "_"
                wordstring = wordstring[0:len(wordstring) - 1]
                wordstring += " "
                wordDE=wordstring
        ftupleunit.append(wordDE)
        count += 1
        ftuple.append(ftupleunit)
    df=pd.DataFrame(ftuple,columns=["AUPY","PY","CR","TC","STDE"])
    return df



# built the abstract corpus by extract abstract from WoS files into one file
# as the abstract collection
def build_ABcorpus_filedir(dir):
    CorpusContent = ""
    ABcontents = ""
    count = 0
    names = os.listdir(dir)
    dirAB=dir+"AB/"
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                ABcontents += eachline
    ABCollections = ABcontents.split("\nAB ")
    for abblock in ABCollections:
        blockends = abblock.split("\n")
        if blockends and count > 0:
            print(count)
            CorpusContent += blockends[0]
            Writetofile(blockends[0],dirAB+str(count)+".txt")
        count += 1
    return CorpusContent

# building the corpus directory
def build_DEcorpus_filedir(dir):
    CorpusContent = ""
    contents = ""
    count = 0
    names = os.listdir(dir)
    dirDE=dir+"DE/"
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                contents += eachline
    CollectionsF = contents.split("\nER")
    for collf in CollectionsF:  # collf为其中一个文献单元
        # print(collf)
        if "\nDE " in collf:
            Collections = collf.split("\nDE ")
        else:
            continue
        # for deblock in Collections:
        deblock = Collections[1]
        if "\nID " in deblock:
            blockends=deblock.split("\nID ")
        else:
            blockends = deblock.split("\nAB ")
        # blockends = abblock.split("\n")
        if blockends and count > 0:
            print(count)
            CorpusContent += blockends[0]
            Writetofile(blockends[0].lower(),dirDE+str(count)+".txt")
        count += 1
    return CorpusContent

#Using the Stemming method to extract keyword into one file as the keyword collection
def build_DEcorpus_dir_MST(dir):
    contents = ""
    count = 0
    names = os.listdir(dir)
    dirDE=dir+"DE/ST/"
    stemmer=SnowballStemmer('english')
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                contents += eachline
    CollectionsF = contents.split("\nER")
    for collf in CollectionsF:  # collf为其中一个文献单元
        if "\nDE " in collf:
            Collections = collf.split("\nDE ")
        else:
            continue
        deblock = Collections[1]
        if "\nID " in deblock:
            blockends = deblock.split("\nID ")
        else:
            blockends = deblock.split("\nAB ")
        if blockends and count > 0:
            print(count)
            temp = blockends[0]
            temp = temp.replace("-", "_")
            temp = temp.replace("(", "")
            temp = temp.replace(")", "")
            temp = temp.replace("\"", "")
            temp = temp.replace("'", "")
            strlist=temp.split(";")
            wordstring=""
            for word in strlist:
                strtemp=nltk.word_tokenize(word)
                out=[stemmer.stem(wd) for wd in strtemp]
                for wds in out:
                    wordstring+=wds+"_"
                wordstring=wordstring[0:len(wordstring)-1]
                wordstring+=" "
            wordstring=str.lower(wordstring)
            Writetofile(wordstring,dirDE+str(count)+".txt")
        count += 1

# Process every keyword list
# flood vulnerability; spatial homogeneity; spatial heterogeneity
# will transfer to be like
#
def build_DEcorpus_dir_M(dir):
    contents = ""
    count = 0
    names = os.listdir(dir)
    dirDE=dir+"DE/CO/"
    for name in names:
        if name.endswith(".txt") and name.startswith("download"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                contents += eachline
    CollectionsF = contents.split("\nER")
    for collf in CollectionsF:
        # print(collf)
        if "\nDE " in collf:
            Collections = collf.split("\nDE ")
        else:
            continue
        deblock = Collections[1]
        if "\nID " in deblock:
            blockends = deblock.split("\nID ")
        else:
            blockends = deblock.split("\nAB ")
        if blockends and count > 0:
            print(count)
            temp = blockends[0].replace("    ", "_")
            temp = temp.replace("\n   ", "_")
            temp = temp.replace("   ", "_")
            temp = temp.replace("  ", "_")
            temp = temp.replace(" ","_")
            temp = temp.replace(".", "_")
            temp = temp.replace(",", "_")
            temp = temp.replace("-", "_")
            temp = temp.replace("(", "")
            temp = temp.replace(")", "")
            strlist=temp.split(";")
            wordstring=""
            for word in strlist:
                if word.startswith("_"):
                    word = word[1:len(word)]
                if word.endswith("_"):
                    word = word[0:len(word) - 1]
                wordstring += word
                wordstring += " "
                wordstring = wordstring.lower()
            Writetofile(wordstring,dirDE+str(count)+".txt")
        count += 1


def Fix_DEcorpus_dirM(dir):
    dirDE=dir+"DE/CO/"
    names = os.listdir(dirDE)
    for name in names:
        if name.endswith(".txt"):
            # print(dirDE + name)
            fobj = codecs.open(dirDE + name, 'r', 'utf-8')
            contents = ""
            for eachline in fobj:
                contents += eachline
                print(eachline)
            contents=contents.replace(" _", " ")
            contents = contents.replace("\"", "")
            contents = contents.replace("'", "")
            contents = contents.replace(".", "")
            contents = contents.replace("__", "_")
            Writetofile(contents,dirDE+name)

def Fix_DEcorpus_dirMST(dir):
    dirDE=dir+"DE/ST/"
    names = os.listdir(dirDE)
    for name in names:
        if name.endswith(".txt"):
            # print(dirDE + name)
            fobj = codecs.open(dirDE + name, 'r', 'utf-8')
            contents = ""
            for eachline in fobj:
                contents += eachline
                print(eachline)
            contents=contents.replace(" _", " ")
            contents = contents.replace("\"", "")
            contents = contents.replace("'", "")
            contents = contents.replace(".", "")
            contents = contents.replace("__", "_")
            contents = contents.replace("?_?_?_?_?_", "")
            Writetofile(contents,dirDE+name)

def Fix_file(dirfile):
    # names = os.listdir(dirDE)
    fobj = codecs.open(dirfile, 'r', 'utf-8')
    contents = ""
    for eachline in fobj:
        contents += eachline
    contents=contents.replace(" _", " ")
    contents = contents.replace("\"", "")
    contents = contents.replace("'", "")
    contents = contents.replace(".", "")
    contents = contents.replace("/", "")
    contents = contents.replace(":", "")
    contents = contents.replace("__", "_")
    Writetofile(contents,dirfile)

def Stem_file(dirfile,dirfiledist):
    # names = os.listdir(dirDE)
    fobj = codecs.open(dirfile, 'r', 'utf-8')
    stemmer=SnowballStemmer("english")
    contents = ""
    for eachline in fobj:
        contents += eachline
    st=nltk.word_tokenize(contents)
    out=[stemmer.stem(wd) for wd in st]
    res=""
    for wd in out:
        res+=wd
        res+=" "
    Writetofile(res,dirfiledist)

def LE_file(dirfile,dirfiledist):
    # names = os.listdir(dirDE)
    fobj = codecs.open(dirfile, 'r', 'utf-8')
    lemma=WordNetLemmatizer()
    contents = ""
    for eachline in fobj:
        contents += eachline
    st=nltk.word_tokenize(contents)
    out=[lemma.lemmatize(wd) for wd in st]
    res=""
    for wd in out:
        res+=wd
        res+=" "
    Writetofile(res,dirfiledist)

def Fix_file_clusterST(dirfile):
    # names = os.listdir(dirDE)
    fobj = codecs.open(dirfile, 'r', 'utf-8')
    contents = ""
    for eachline in fobj:
        contents += eachline
    contents = contents.replace(" _", " ")
    contents = contents.replace("\"", "")
    contents = contents.replace("'", "")
    contents = contents.replace("/", "")
    contents = contents.replace("_.", "")
    contents = contents.replace("?_?_?_?_?_", "")
    contents = contents.replace("__", "_")
    Writetofile(contents, dirfile)

def load_from_file(filepath):
    text=""
    fobj=codecs.open(filepath,'r','utf-8')
    for eachline in fobj:
        text+=eachline
    return text

def Writetofile(str,filepath):
    fp=codecs.open(filepath,'w','utf-8')
    fp.write(str)

def filter_stopwords_dir(dir,dir_filter):
    names = os.listdir(dir)
    for name in names:
        ABcontents=""
        if name.endswith(".txt"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                ABcontents += eachline
        ABcontents=filter_stopwords(ABcontents)
        Writetofile(ABcontents,dir_filter + name)

def filter_DE_dir(dir,dir_filter):
    names = os.listdir(dir)
    for name in names:
        contents=""
        if name.endswith(".txt"):
            print(dir + name)
            fobj = codecs.open(dir + name, 'r', 'utf-8')
            for eachline in fobj:
                contents += eachline
        contents=filter_stopwords(contents)
        Writetofile(contents,dir_filter + name)

def filter_stopwords(str):
    str=str.lower()
    stemmer=SnowballStemmer('english')
    in_str=nltk.word_tokenize(str)
    out= [word for word in in_str if word not in stopwords.words('english')]
    out=[stemmer.stem(word) for word in out]
    outst=""
    for w in out:
        outst+=w
        outst+=" "
    return outst

def filter_DE(str):
    str=str.lower()
    in_str=str.split(";")
    outst=""
    for w in in_str:
        outst+=w
        outst+=" "
    return outst


###
#1. abstract extration
#input WoS dataset directory
#out text file cu1AB.txt
###
# extract abstract into one file en1AB.txt
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirAB="D:/publications/GitWksp/WoSdata/naturalhazard//en1AB.txt"
dirABST="D:/publications/GitWksp/WoSdata/naturalhazard//en1ABST.txt"
content=build_ABCorpus(dir)
Writetofile(content,dirAB)
Stem_file(dirAB,dirABST)



###
#3. extract the keyword collection in the geographic natural hazard data collection
# input WoS dataset of geographical natural hazards
# output dirDEST=dir+"cu1DECOST.txt"
###
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirDEST=dir+"cu1DECOST.txt"
content=build_DESTCorpus(dir)
Writetofile(content,dirDEST)


###
#4. transfer the keyword collections into the word vectors
###
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirDEST=dir+"cu1DECOST.txt"
dirKeywordList=dir+"keywordlist.csv"
corpus1=load_from_file(dirDEST)
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


###
# 5. dimension reduction
# listres has the vectors
# listtext has the keywords
# we need the keywords with the X,Y dimensions and along with the citations
# after different time points
#
###

dirTuple=dir+"cu1DECOTuple.csv"
dirTupleG=dir+"cu1DECOTuple_2010_2013_2016.csv"
dirTupleG2=dir+"cu1DECOTuple_2016151413121009080706.csv"
# dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
df=GenerateTRef(dir)
df.to_csv(dirTuple)
# df=pd.read_csv(dirTuple)
#STDE stands for keywords, TC stands for total citation counts
#aupy stands for author and publication for identifying the paper
# CR stands for the cited references
stde=df["STDE"]
tc=df["TC"]
aupy=df["AUPY"]
py=df["PY"]
cr=df["CR"]
wlTCSTC=[]
count=0
for stdei in stde:
    stdeis=stdei.split(" ")
    for w in stdeis:
        if "" == w  or "\n" == w or w is None:
            continue
        wl = []
        count_SC = 0
        count_AF_2008 = 0
        count_AF_2007 = 0
        count_AF_2006 = 0
        count_AF_2010=0
        count_AF_2011=0
        count_AF_2012=0
        count_AF_2013=0
        count_AF_2014=0
        count_AF_2015=0
        count_SC_2010_7=0
        count_SC_2010 =0
        count_SC_2013_7 = 0
        count_SC_2013 = 0
        count_SC_2016_7=0
        count_SC_2016=0

        tci = tc[count]
        aupyi = aupy[count]
        pyi = py[count]
        # 计算时间阶段内的该topic被引用次数 >2009年后
        # compute the keyword citations after 2009
        for cri in cr:
            if aupyi in cri and int(pyi) > 2006:
                count_AF_2006+=1
            if aupyi in cri and int(pyi) > 2007:
                count_AF_2007+=1
            if aupyi in cri and int(pyi) > 2008:
                count_AF_2008+=1
            if aupyi in cri and int(pyi) > 2009:
                count_SC+=1
            if aupyi in cri and int(pyi) > 2010:
                count_AF_2010+=1
            if aupyi in cri and int(pyi) > 2011:
                count_AF_2011+=1
            if aupyi in cri and int(pyi) > 2012:
                count_AF_2012 += 1
            if aupyi in cri and int(pyi) > 2013:
                count_AF_2013 += 1
            if aupyi in cri and int(pyi) > 2014:
                count_AF_2014 += 1
            if aupyi in cri and int(pyi) > 2015:
                count_AF_2015 += 1
        for cri in cr:
            if aupyi in cri and int(pyi) > 2003 and int(pyi) <= 2010:
                count_SC_2010_7+=1
        for cri in cr:
            if aupyi in cri and int(pyi) < 2010:
                count_SC_2010 += 1
        for cri in cr:
            if aupyi in cri and int(pyi) > 2006 and int(pyi) <=2013:
                count_SC_2013_7 += 1
        for cri in cr:
            if aupyi in cri and int(pyi) < 2013:
                count_SC_2013 += 1
        for cri in cr:
            if aupyi in cri and int(pyi) > 2009 and int(pyi) <=2016:
                count_SC_2016_7 += 1
        for cri in cr:
            if aupyi in cri and int(pyi) < 2016:
                count_SC_2016 += 1

        # insert the current keyword and the corresponding citations
        flag=True
        for wp in wlTCSTC:
            if wp and w == wp[0]:
                wp[1] =int(wp[1])+ int(tci)
                wp[2] =int(wp[2])+ int(count_SC)
                wp[3]=int(wp[3])+ int(count_SC_2010_7)
                wp[4] = int(wp[4]) + int(count_SC_2010)
                wp[5] = int(wp[5]) + int(count_SC_2013_7)
                wp[6] = int(wp[6]) + int(count_SC_2013)
                wp[7] = int(wp[7]) + int(count_SC_2016_7)
                wp[8] = int(wp[8]) + int(count_SC_2016)
                wp[9] = int(wp[9])+ int(count_AF_2010)
                wp[10] = int(wp[10])+ int(count_AF_2011)
                wp[11] = int(wp[11])+ int(count_AF_2012)
                wp[12] = int(wp[12])+ int(count_AF_2013)
                wp[13] = int(wp[13])+ int(count_AF_2014)
                wp[14] = int(wp[14])+ int(count_AF_2015)
                wp[15] = int(wp[15]) + int(count_AF_2006)
                wp[16] = int(wp[16]) + int(count_AF_2007)
                wp[17] = int(wp[17]) + int(count_AF_2008)
                flag=False
                continue
        if flag:
            wl.append(w)
            wl.append(tci)
            wl.append(count_SC)
            wl.append(count_SC_2010_7)
            wl.append(count_SC_2010)
            wl.append(count_SC_2013_7)
            wl.append(count_SC_2013)
            wl.append(count_SC_2016_7)
            wl.append(count_SC_2016)
            wl.append(count_AF_2010)
            wl.append(count_AF_2011)
            wl.append(count_AF_2012)
            wl.append(count_AF_2013)
            wl.append(count_AF_2014)
            wl.append(count_AF_2015)
            wl.append(count_AF_2006)
            wl.append(count_AF_2007)
            wl.append(count_AF_2008)
            wlTCSTC.append(wl)
    count+=1
dwp=pd.DataFrame(wlTCSTC,columns=["w","tc","stc","2010_7","2010","2013_7","2013","2016_7","2016","2010","2011","2012","2013","2014","2015","2006","2007","2008"])
# dirTuple=dir+"cu1DECOTuple.csv"
# dirTupleG=dir+"cu1DECOTuple_2010_2013_2016.csv"
# dirTupleG2=dir+"cu1DECOTuple_2016151413121009080706.csv"
dwp.to_csv(dirTupleG2)









