import WoSdataparser


###
#3. extract the keyword collection in the geographic natural hazard data collection
# input WoS dataset of geographical natural hazards
# output dirDEST=dir+"cu1DECOST.txt"
###
dir="D:/publications/GitWksp/WoSdata/ngeo/"
dirDEST=dir+"cu1DECOST.txt"
content=WoSdataparser.build_DESTCorpus(dir)
WoSdataparser.Writetofile(content,dirDEST)