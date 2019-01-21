import WoSdataparser


dir="D:/publications/GitWksp/WoSdata/naturalhazard"
dirAB="D:/publications/GitWksp/WoSdata/naturalhazarden1AB.txt"
dirABST="D:/publications/GitWksp/WoSdata/naturalhazarden1ABST.txt"
dirABReST= "D:/publications/GitWksp/WoSdata/naturalhazard/en1ABReST.txt"
content=WoSdataparser.build_ABCorpus(dir)
WoSdataparser.Writetofile(content,dirAB)
WoSdataparser.Stem_file(dirAB,dirABST)
#remove the stop word
content=WoSdataparser.load_from_file(dirABST)
content_ReStop=WoSdataparser.remove_stopwords(content)
WoSdataparser.Writetofile(content_ReStop,dirABReST)