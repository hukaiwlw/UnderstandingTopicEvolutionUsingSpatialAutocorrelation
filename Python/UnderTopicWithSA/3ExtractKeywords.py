import WOSparser

###
#3. extract the keyword collection in the geographic natural hazard data collection
# input WoS dataset of geographical natural hazards
# output dirDEST=dir+"cu1DECOST.txt"
###
dir="D:/publications/GitWksp/WoSdata/naturalhazard/"
dirDEST=dir+"cu1DECOST.txt"
content=WOSparser.build_DESTCorpus(dir)
WOSparser.Writetofile(content,dirDEST)