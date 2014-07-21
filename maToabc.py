#   Create list of shots where camera exists

#   Check for latest versions

#   convert .ma to .abc

import os, sys
import maya.mel as mm
import maya.standalone
import maya.cmds as cmds
maya.standalone.initialize(name='python')


path = 'I:/bubblebathbay/episodes'
episodeShotsDict = {}
filePaths = {}
episodesList = os.listdir(path)
for episode in episodesList:
    if os.listdir(os.path.join(path,episode)):
        shotList = os.listdir(os.path.join(path,episode))
        episodeShotsDict[episode] = shotList
for key, values in episodeShotsDict.iteritems():
    for value in values:
        if value.startswith('ep'):
            camPath = os.path.join(path,key,value,'Anm', 'publish', 'cam')
#             camPath = path+ '/' + key + '/' + value + '/' + 'Anm' + '/' + 'publish' + '/' + 'cam'
            if os.path.exists(camPath):
                if os.listdir(camPath):
                    versionFolders = os.listdir(camPath)
                    versions = sorted(versionFolders)[-1]
                    versionsPath = os.path.join(camPath, versions)
                    
                    filePath = os.listdir(versionsPath)
                    for maPath in sorted(filePath):
                        if maPath.endswith('.ma'):
                            maFilePath = os.path.join(versionsPath,maPath)
#                             print maFilePath
                            compPath = camPath.replace('Anm', 'Comp').replace('cam', 'nuke')
                            print compPath
                            compFilePath = compPath + '/' + maPath.replace('.ma', '.abc')
                            compFilePath = compFilePath.replace('\\', '/')
#                             print compFilePath
                            filePaths[maFilePath] = compPath
                            cmds.file(maFilePath, open=True, f=1)
                            cmds.loadPlugin("AbcExport.mll")
                            jobString = "AbcExport"
                            jobString += " -j \" -frameRange 1 1000 -root |BAKE_CAM_hrc -file %s\";" %   compFilePath
#                             mm.eval("string $compFilePath = `python \"compFilePath\"`; print $compFilePath;")
#                             mm.eval("string $compFile = `python \"maPath\"`;")
#                             mm.eval("string $finalFile = $compFilePath + "" + $compFile")
                            mm.eval(jobString)
                            print "Done"