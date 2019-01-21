#write the WOS parser
# firstly, the abstract extraction
# secondly, the keywords collection extraction
# build the construct to storage the data sets for the further NLP processing
import os
import codecs
from nltk.corpus import stopwords
import nltk
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd

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
            # print(count)
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
            # print(wordPY)
        wordPY=wordPY.replace("\r","")
        wordAU=wordAU.replace("\r","")
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
        wordCT=wordCT.replace("\r","")
        ftupleunit.append(wordCT)

        #collect stem keywords in keyword list for each paper
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
        print(ftupleunit)
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

def remove_stopwords(content):
    content_List = nltk.word_tokenize(content)
    filtered=[w for w in content_List if (w not in stopwords.words('english'))]
    return ' '.join(filtered)











