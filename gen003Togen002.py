import os
import sys
import glob
path = 'I:/bubblebathbay/episodes/ep114/'
shotsList = os.listdir(path)
episode = 'ep114'

# task = 'Anm'
# workDir = 'work'
# appFolder = 'maya'
# fileToWorkOn = []
# for shot in sorted(shotsList):
#     if '_mp' not in shot:
#         filePath = os.path.join(path, shot, task, workDir, appFolder)
#         if os.path.exists(filePath):
#             files = [os.path.join(filePath, f) for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]
#             if files:
#                 latestFile = max(files, key=os.path.getctime)
#                 readFile = open(latestFile, 'r')
#                 fileContentOld = readFile.readlines()
#                 for eachLine in fileContentOld:
#                     if 'PROPGEN001InflatableBuoy' in eachLine :
#                         if latestFile not in fileToWorkOn:
#                             fileToWorkOn.append(latestFile)
# #                             print latestFile

fileToWorkOn = ['I:/bubblebathbay/episodes/ep114/ep114_sh018\\Anm\\work\\maya\\ep114sh018Anim.v009.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh019\\Anm\\work\\maya\\ep114sh019Anim.v007.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh020\\Anm\\work\\maya\\ep114sh020Anim.v007.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh022\\Anm\\work\\maya\\ep114sh022Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh023\\Anm\\work\\maya\\ep114sh023Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh024\\Anm\\work\\maya\\ep114sh024Anm.v011.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh025\\Anm\\work\\maya\\ep114sh025Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh026\\Anm\\work\\maya\\ep114sh026Anim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh029\\Anm\\work\\maya\\ep114sh029Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh030\\Anm\\work\\maya\\ep114sh030Anim.v017.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh031\\Anm\\work\\maya\\ep114sh031Anim.v013.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh043\\Anm\\work\\maya\\ep114sh043Anim.v007.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh052\\Anm\\work\\maya\\ep114sh052Anim.v050.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh055\\Anm\\work\\maya\\ep114sh055Anm.v005.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh056\\Anm\\work\\maya\\ep114sh056Anm.v009.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh058\\Anm\\work\\maya\\ep114sh058Anim.v012.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh067\\Anm\\work\\maya\\ep114sh067Anim.v011.ma']


# fileToWorkOn = ['I:/bubblebathbay/episodes/ep114/ep114_sh017\\Anm\\work\\maya\\ep114sh017Anim.v010.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh030\\Anm\\work\\maya\\ep114sh030Anim.v016.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh041\\Anm\\work\\maya\\ep114sh041Anim.v023.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh042\\Anm\\work\\maya\\ep114sh042Anim.v017.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh051\\Anm\\work\\maya\\ep114sh051Anim.v007.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh059\\Anm\\work\\maya\\ep114sh059Anim.v010.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh060\\Anm\\work\\maya\\ep114sh060Anim.v006.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh061\\Anm\\work\\maya\\ep114sh061.v006.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh062\\Anm\\work\\maya\\ep114sh062Anim.v005.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh065\\Anm\\work\\maya\\ep114sh065Anim.v006.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh066\\Anm\\work\\maya\\ep114sh066Anim.v005.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh066A\\Anm\\work\\maya\\ep114sh066AAnim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh067\\Anm\\work\\maya\\ep114sh067Anim.v010.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh068\\Anm\\work\\maya\\ep114sh068Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh077\\Anm\\work\\maya\\ep114sh077.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh081\\Anm\\work\\maya\\ep114sh081.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh083\\Anm\\work\\maya\\ep114sh083.v006.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh084\\Anm\\work\\maya\\ep114sh084.v003.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh085\\Anm\\work\\maya\\ep114sh085.v003.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh086\\Anm\\work\\maya\\ep114sh086.v003.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh087\\Anm\\work\\maya\\ep114sh087Anim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh088\\Anm\\work\\maya\\ep114sh088.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh089\\Anm\\work\\maya\\ep114sh089Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh091\\Anm\\work\\maya\\ep114sh091Anim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh092\\Anm\\work\\maya\\ep114sh092Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh093\\Anm\\work\\maya\\ep114sh093Anim.v004.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh095\\Anm\\work\\maya\\ep114sh095Anim.v001.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh096\\Anm\\work\\maya\\ep114sh096.v006.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh097\\Anm\\work\\maya\\ep114sh097Anim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh098\\Anm\\work\\maya\\ep114sh098.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh099\\Anm\\work\\maya\\ep114sh099Anim.v001.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh100\\Anm\\work\\maya\\ep114sh100Anim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh101\\Anm\\work\\maya\\ep114sh101.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh102\\Anm\\work\\maya\\ep114sh102.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh103\\Anm\\work\\maya\\ep114sh103Anim.v002.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh104\\Anm\\work\\maya\\ep114sh104.v003.ma', 'I:/bubblebathbay/episodes/ep114/ep114_sh105\\Anm\\work\\maya\\ep114sh105.v005.ma']
# 
for each in fileToWorkOn:
    fileName = os.path.basename(each)
    verNum = os.path.splitext(fileName)[0].split('.v')[1]
    newVerNum = int(verNum) + 1
    newFileName = each.replace('.v%s' % verNum, '.v%03d' % newVerNum)
     
    f = open(each, 'r+b')
#     newFile = open(newFileName, 'w')
    f_content = f.readlines()
#     for cont in f_content:
#         newFile.write(cont)
#     newFile.close()
#     'PROPGEN003InflatableBuoy' in new_cont
    newF = open(newFileName, 'w')
#     new_contents = newF.readlines()
    for i, new_cont in enumerate(f_content):
        if 'PROP_GEN001_InflatableBuoy' in new_cont:
            new_conts = new_cont.replace('PROP_GEN001_InflatableBuoy', 'PROP_GEN002_InflatableBuoy')
            f_content[i] = new_conts
 
    for i, new_cont in enumerate(f_content):
        if 'PROPGEN001InflatableBuoy' in new_cont:
            new_conts = new_cont.replace('PROPGEN001InflatableBuoy', 'PROPGEN002InflatableBuoy')
            f_content[i] = new_conts
 
    newF.truncate()
    for cont in f_content:
        newF.write(cont)
    newF.close()
    print '%s done' % each
#     