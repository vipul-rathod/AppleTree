"""
Copyright (c) 2013 James Dunlop
----------------------------------------------------
Creates maya assets for BBBay into maya based on the assets lists for a shot in the shotgun db

NOTE THIS IMPORTS THE CACHES AND REBULDS THE OCEAN
THE OCEAN IS REATTACHED TO MARKS SHADED OCEAN WHEN THE SHADERS ARE REBUILT!

"""
import os, getpass, sys, sgtk
import tank.templatekey
import shutil
from tank.platform.qt import QtCore, QtGui
from tank.platform import Application
import maya.cmds as cmds
import maya.mel as mel
from functools import partial
from tank import TankError
import pymel.core as pm

if 'T:/software/bubblebathbay_sandbox/custom' not in sys.path:
## Now get the custom tools
    sys.path.append('T:/software/bubblebathbay_sandbox/custom')

## Append custome script path to import the custom modules
if 'T:/software/bubblebathbay_sandbox/install/apps/tk-bbb-splitLayoutShots/splitLayoutShots' not in sys.path:
    sys.path.append('T:/software/bubblebathbay_sandbox/install/apps/tk-bbb-splitLayoutShots/splitLayoutShots')
## Custom modules for layout shot info
import shotFrameRange
import shiftAnimCurves
# from splitLayoutShots import shotFrameRange
## ...................................
import core_archive_readXML as readXML
import utils as utils
import maya_genericSettings as settings
import maya_asset_MASTERCLEANUPCODE as cleanup
from debug import debug
import ProgressBarUI as pbui
import CONST as CONST


reload(settings)
reload(pbui)
reload(CONST)
reload(readXML)
reload(shotFrameRange)
reload(shiftAnimCurves)
print "Reloaded"
#tk-bbb-splitLayoutShots
###########################################################################
### NOTE I HAVE MOVED THE CONNECT CACHE METHODS INTO THE fluidCaches py!!!!!
class SplitLayoutShots(Application):
    def init_app(self):
        # make sure that the context has an entity associated - otherwise it wont work!
        if self.context.entity is None:
            raise tank.TankError("Cannot load the SplitLayoutShots application! "
                                 "Your current context does not have an entity (e.g. "
                                 "a current Shot, current Asset etc). This app requires "
                                 "an entity as part of the context in order to work.")
        getDisplayName = self.get_setting('display_name')
        self.engine.register_command(getDisplayName, self.run_app)
        debug(self, method = 'init_app', message = 'SplitLayoutShots Loaded...', verbose = True)

    def run_app(self):
        debug(self, method = 'run_app', message = 'SplitLayoutShots...', verbose = True)
        getDisplayName = self.get_setting('display_name')
        debug(self, method = 'run_app', message = 'getDisplayName: %s' % getDisplayName, verbose = True)
        self.engine.show_dialog(getDisplayName, self, MainUI, self)
        

class MainUI(QtGui.QWidget):
    def __init__(self, app):
        """
        """
        QtGui.QWidget.__init__(self)
        self.app = app
#         debug(self.app, method = 'MainUI.__init__', message = 'Running app...', verbose = True)

        self.context = self.app.context ## To get the step
#         debug(app = self.app, method = 'MainUI.__init__', message = 'context: %s' % self.context, verbose = True)
#         debug(app = self.app, method = 'MainUI.__init__', message = 'context Step...%s' % self.context.step['name'], verbose = True)


        if self.context.step['name'] == 'Blocking':
            self.tk = sgtk.sgtk_from_path("T:/software/bubblebathbay_sandbox")         
            self.baseTemplatePath = self.tk.templates[self.app.get_setting('shotPathTemplate')]
            self.baseTemplateMoviePath = self.tk.templates[self.app.get_setting('movie_workpath_template')]
#             debug(app = self.app, method = 'MainUI.__init__', message = 'self.baseTemplatePath: %s' % self.baseTemplatePath, verbose = True)

        ################### UI LOAD / BUILD NOW
        ## Now build the UI
        self.mainLayout = QtGui.QVBoxLayout(self)
        
        # List of shots to split
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderLabel('Shots')
        self.treeWidgetItems = []
        self.mySubShots = self._getSubShots()
        for each in self.mySubShots:
            self.treeWidgetItem = QtGui.QTreeWidgetItem([each['name']])
            print each['name']
            self.treeWidgetItem.setCheckState(0, QtCore.Qt.Checked)
            self.treeWidgetItems.append(self.treeWidgetItem)
        
        self.treeWidget.addTopLevelItems(self.treeWidgetItems)
        
        ## Setup the layout and buttons
        self.splitLayoutGroupBox = QtGui.QGroupBox(self)
        self.splitLayoutGroupBox.setTitle('Split Shot Loader:')
#         debug(self.app, method = 'MainUI.__init__', message = 'splitLayoutGroupBox built successfully...', verbose = True)
        
#         self.buttonLayout = QtGui.QHBoxLayout(self.splitLayoutGroupBox)
        self.buttonLayout = QtGui.QHBoxLayout()

#         self.fetchAnimCachesButton = QtGui.QPushButton('Get Cameras')
#         self.fetchAnimCachesButton.clicked.connect(self._fetchAnimationCaches)

#         self.getCamerasButton = QtGui.QPushButton('Get Cameras')
#         self.getCamerasButton.clicked.connect(self._getCameras)

        self.splitLayoutShotsButton = QtGui.QPushButton('Split layout Shots')
        self.splitLayoutShotsButton.clicked.connect(self._splitLayoutShots)

        self.localPlayblastButton = QtGui.QPushButton('Local Playblast')
        self.localPlayblastButton.clicked.connect(self._localPlayblast)

#         self.fetchCoresButton = QtGui.QPushButton('Fetch Core Archives')


#         self.cleanupButton = QtGui.QPushButton('Cleanup')
#         self.cleanupButton.clicked.connect(self._cleanup)
#         debug(self.app, method = 'MainUI.__init__', message = 'All buttons built successfully', verbose = True)
        
        ## Add the buttons to their layout widget
#         self.buttonLayout.addWidget(self.getCamerasButton)
        self.buttonLayout.addWidget(self.splitLayoutShotsButton)
        self.buttonLayout.addWidget(self.localPlayblastButton)
#         self.buttonLayout.addWidget(self.fetchCoresButton)
#         self.buttonLayout.addWidget(self.cleanupButton)
        
        self.mainLayout.addWidget(self.splitLayoutGroupBox)
        self.mainLayout.addWidget(self.treeWidget)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.mainLayout.addStretch(1)
        self.resize(300, 20)

    def _splitLayoutShots(self):
        """
        Main func to handle the shot creationss
        """
        self.shotsToSplit = [item.text(0) for item in self.treeWidgetItems if item.checkState(0)]
        self.mySubShots = self._getSubShots()

        if self.mySubShots :
            for eachSubShotDic in self.mySubShots:##Process all the data for each shot now...
                ## Get the correct frame range from shotgun for the shot
                ##[{'type': 'Shot', 'id': 5737, 'name': 'eptst2_sh001'}, {'type': 'Shot', 'id': 5738, 'name': 'eptst2_sh002'}]
                if eachSubShotDic['name'] in self.shotsToSplit:
                    getShotgunFrameRange = self._fetchShotgunFrameRange(shotId =eachSubShotDic['id'])
                    mpShotFrameRange = shotFrameRange.FetchShotFrameRange()
                    getCameraStartFrame = mpShotFrameRange.fetchShotFrameRange_Fn(eachSubShotDic['name'])
                      
                    ## Shift all the anim curves to start Frame
                    sac = shiftAnimCurves.ShiftAnimCurves()
                    sac.shiftAnimCurves_Fn(getCameraStartFrame['mpStartFrame'])
                    self._setShotFrameRange(getShotgunFrameRange['sg_cut_out'])
    
                    ### Path to workfolder
                    ## self.baseTemplatePath needs fields to create a final working path.
                    fields = {}
                    fields['Sequence'] = eachSubShotDic['name'].split('_')[0]
                    fields['Shot'] = eachSubShotDic['name']
                    fields['Step'] = 'Blck'
                    fields['name'] = str(eachSubShotDic['name'].split('_')[0] + eachSubShotDic['name'].split('_')[1] + 'Layout')
                    fields['version'] = 1
                    publish_path = self.baseTemplatePath.apply_fields(fields)
                    ## Verify existing versions
                    while os.path.exists(publish_path):
                        fields['version'] += 1
                        publish_path = self.baseTemplatePath.apply_fields(fields)
                    else:
                        pass
                    
                    ## Clean up the cameras so there is only one camera with the attr shotCam
                    self._setShotCam(eachSubShotDic['name'])
                    self._audioOffset(eachSubShotDic['name'])
                    ## Save to the working folder.
                    self._publishToWorkFolders(publish_path)
                    self._undoAudioDelete()
                    self._undoSetShotCam(eachSubShotDic['name'])
                else:
                    cmds.warning('No shots selected to split')
        else:
            cmds.warning('This shot has no valid subshots in shotgun to process!!!')

    def _getSubShots(self):
        """
        Function to just return all the subShot data
        """
         ## Build an entity type to get some values from.
        self.entity = self.context.entity    ## returns {'type': 'Shot', 'name': 'ep100_sh010', 'id': 1166}
#         debug(self.app, method = 'MainUI.__init__', message = 'entity... %s' % self.entity, verbose = True)
 
        ## Filter for the matching ID for the shot
        self.sg_filters = [["id", "is", self.entity["id"]]]
#         debug(app = self.app, method = 'MainUI.__init__', message = 'sg_filters... %s' % self.sg_filters, verbose = True)  
         
        ## Build an entity type to get some values from.
        self.sg_entity_type = self.context.entity["type"]                                                                   ## returns Shot
#         debug(app = self.app, method = 'MainUI.__init__', message = 'sg_entity_type...\n%s' % self.sg_entity_type, verbose = True)

        self.data = self.app.shotgun.find_one(self.sg_entity_type, filters=self.sg_filters, fields=['shots'])['shots']
#         debug(app = self.app, method = 'MainUI.__init__', message = 'Child Shots id...\n%s' % self.data, verbose = True)

        if self.data:        
            return self.data
        else:
            return False

    def _fetchShotgunFrameRange(self, shotId):
        self.childShotCutInfo = self.tk.shotgun.find_one('Shot', [['id', 'is', shotId]], fields = ['sg_cut_in', 'sg_cut_out'])
        return self.childShotCutInfo
        ## Fetch child shots startFrame in master file
        #debug(app = self.app, method = 'MainUI.__init__', message = 'Frame Range ...\n%s' % self.mpFrameRange, verbose = True)

    def _setShotFrameRange(self, endFrame):
        cmds.playbackOptions(min=1, ast=1, max=endFrame, aet=endFrame)

    def _setShotCam(self, shotName):
        """
        This function deletes the attr type for the cameras that do no relate to the currently exported shot
        """
        camerasShape = cmds.ls(type='camera')
        cameras = [cmds.listRelatives(camShape, p=1)[0] for camShape in camerasShape]
        for cam in cameras:
            if cam.endswith('shotCam'):
                if cam.split('_shotCam')[0] != shotName:
                    if cmds.attributeQuery('type', node=cam, exists=1):
                        cmds.deleteAttr(cam, attribute = 'type')
    
    def _undoSetShotCam(self, shotName):
        camerasShape = cmds.ls(type='camera')
        cameras = [cmds.listRelatives(camShape, p=1)[0] for camShape in camerasShape]
        for cam in cameras:
            if cam.endswith('shotCam'):
                if cam.split('_shotCam')[0] != shotName:
                    if not cmds.attributeQuery('type', node=cam, exists=1):
                        cmds.addAttr(cam, ln = 'type', dt='string')
                        cmds.setAttr('%s.type' % cam, e=1, keyable=1)
                        cmds.setAttr('%s.type' % cam, 'shotCam', type='string')
                    
    def _publishToWorkFolders(self, fileName):
        cmds.file(rename=fileName)
        cmds.file(save=1, type='mayaAscii')
    
    def _audioOffset(self, shotName):
        audioNodes = cmds.ls(type='audio')
        for audioNode in audioNodes:
            if audioNode == shotName:
                cmds.setAttr('%s.offset' % audioNode, 1)
        for audioNode in audioNodes:
            if audioNode != shotName:
                cmds.delete(audioNode)
 
    def _undoAudioDelete(self):
        cmds.undo()
        
    def _localPlayblast(self):
        self.shotsToPlayblast = [item.text(0) for item in self.treeWidgetItems if item.checkState(0)]
        self.mySubShots = self._getSubShots()
        if self.mySubShots :
            for eachSubShotDic in self.mySubShots:##Process all the data for each shot now...
                ## Get the correct frame range from shotgun for the shot
                ##[{'type': 'Shot', 'id': 5737, 'name': 'eptst2_sh001'}, {'type': 'Shot', 'id': 5738, 'name': 'eptst2_sh002'}]
                if eachSubShotDic['name'] in self.shotsToPlayblast:
                    path = 'I:/bubblebathbay/layout_movs/'
                    episode = eachSubShotDic['name'].split('_')[0]
                    shots = self.entity['name']
                    lat = 'latest'
                    ver = 'version'
                    versionNumber = 001
                    fileName = '%sLayout.v%03d.mov' % (eachSubShotDic['name'].replace('_', ''), versionNumber)
                    movPathToLatest = os.path.join(path, episode, shots, lat, fileName)
                    movPathToVersion = os.path.join(path, episode, shots, ver, fileName)
                    while os.path.exists(movPathToVersion):
                        versionNumber += 1
                        if versionNumber < 10:
                            newFileName = '%sLayout.v%03d.mov' % (eachSubShotDic['name'].replace('_', ''), versionNumber)
                            movPathToVersion = os.path.join(path, episode, shots, ver, newFileName)
                        else:
                            newFileName = '%sLayout.v%02d.mov' % (eachSubShotDic['name'].replace('_', ''), versionNumber)
                            movPathToVersion = os.path.join(path, episode, shots, ver, newFileName)
                    else:
                        pass

                    if not os.path.exists(os.path.join(path, episode, shots, lat)):
                        os.makedirs(os.path.join(path, episode, shots, lat))
                    if not os.path.exists(os.path.join(path, episode, shots, ver)):
                        os.makedirs(os.path.join(path, episode, shots, ver))
                    ### Path to work review folder
                    ## self.baseTemplateMoviePath needs fields to create a final mov path.
#                     fields = {}
#                     fields['Sequence'] = eachSubShotDic['name'].split('_')[0]
#                     fields['Shot'] = eachSubShotDic['name']
#                     fields['Step'] = 'Blck'
#                     fields['name'] = str(eachSubShotDic['name'].split('_')[0] + eachSubShotDic['name'].split('_')[1] + 'Layout')
#                     fields['version'] = 1
#                     publish_movie_path = self.baseTemplateMoviePath.apply_fields(fields)
                    ## Verify existing versions
#                     while os.path.exists(publish_movie_path):
#                         fields['version'] += 1
#                         publish_movie_path = self.baseTemplateMoviePath.apply_fields(fields)
#                     else:
#                         pass

                    activePanel = cmds.getPanel(wf=1)
                    modelPanels = cmds.getPanel(type='modelPanel')
                    camShape = '%s_shotCamShape' % eachSubShotDic['name']
                    if activePanel in modelPanels:
                        modEditor = cmds.modelEditor(activePanel, e=1, cam=camShape, displayAppearance='smoothShaded', displayTextures=True)
                        cmds.modelEditor(activePanel, e=1, allObjects=0)
                        cmds.modelEditor(activePanel, e=1, polymeshes=1, ns=1, hud=1, ps=1, po=('gpuCacheDisplayFilter', 1))
                        mpShotFrameRange = shotFrameRange.FetchShotFrameRange()
                        mel.eval('setFocalLengthVisibility(on);')
                        mel.eval('setCurrentFrameVisibility(on);')
                        mel.eval('setCameraNamesVisibility(on);')
                        mel.eval('setSceneTimecodeVisibility(on);')
                        cmds.displayColor('headsUpDisplayLabels', 16)
                        cmds.displayColor('headsUpDisplayValues', 16)
                        getCameraStartFrame = mpShotFrameRange.fetchShotFrameRange_Fn(eachSubShotDic['name'])
                        cmds.setAttr("defaultResolution.width", 1280)
                        cmds.setAttr("defaultResolution.height", 720)
                        endFrame = getCameraStartFrame['mpEndFrame'] + 1
                        cmds.playblast(sound= eachSubShotDic['name'],
                                       filename=movPathToVersion,
                                       offScreen=1,
                                       widthHeight=[1280,720],
                                       quality=100, 
                                       startTime= getCameraStartFrame['mpStartFrame'],
                                       endTime= endFrame,
                                       format='qt',
                                       forceOverwrite = True,
                                       activeEditor = False,
                                       clearCache = True,
                                       combineSound = True,
                                       compression = 'h.264',
                                       framePadding = 4,
                                       options = False,
                                       sequenceTime = False,
                                       showOrnaments = True,
                                       viewer = True,
                                       percent=75
                                       )
                        shutil.copy2(movPathToVersion, movPathToLatest)
                    else:
                        QtGui.QMessageBox.information(None, "Aborted...", 'You must have active a current 3D viewport! \nRight click the viewport you wish to playblast from.')
                else:
                    pass
        else:
            cmds.warning('This shot has no valid subshots in shotgun to process!!!')

    def destroy_app(self):
        self.log_debug("Destroying SplitLayoutShots")