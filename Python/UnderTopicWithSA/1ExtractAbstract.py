import WOSparser

dir="D:/publications/GitWksp/WoSdata/naturalhazard"
dirAB="D:/publications/GitWksp/WoSdata/naturalhazarden1AB.txt"
dirABST="D:/publications/GitWksp/WoSdata/naturalhazarden1ABST.txt"
content=WOSparser.build_ABCorpus(dir)
WOSparser.Writetofile(content,dirAB)
Stem_file(dirAB,dirABST)