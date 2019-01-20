import WOSparser
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
df=WOSparser.GenerateTRef(dir)
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