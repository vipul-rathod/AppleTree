import sys, os, shutil
from PyQt4 import QtCore
from PyQt4 import QtGui

if 'T:/software/python-api/' not in sys.path:
    sys.path.append('T:/software/python-api/')
from shotgun_api3 import Shotgun

class PublishPlayblast(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PublishPlayblast, self).__init__(parent)
        
        #    Default path to get list of mov's to publish to shotgun
        self.movPath = 'I:/bubblebathbay/layout_movs/'
        
        #    Tool Version
        toolVersion = str('0.0.1')
        
        #    Combox for listing all episodes
        self.epLabel = QtGui.QLabel("Episode:")
        self.epComboBox = QtGui.QComboBox()
        self.epLayout = QtGui.QHBoxLayout()
        self.epLayout.addWidget(self.epLabel)
        self.epLayout.addWidget(self.epComboBox)

        #    Combox for listing all shots in selected Episodes
        self.shLabel = QtGui.QLabel("Shot:")
        self.shComboBox = QtGui.QComboBox()
        self.shLayout = QtGui.QHBoxLayout()
        self.shLayout.addWidget(self.shLabel)
        self.shLayout.addWidget(self.shComboBox)
        
        #    List for selecting shots to publish
        self.movTreeWidget = QtGui.QTreeWidget()
        self.movTreeWidget.setHeaderLabel('Shots')
        
        #    Button for publishing selected shots in List
        self.publishButton = QtGui.QPushButton("Publish")
        self.publishButton.clicked.connect(self._moveFilesToPublish)
        #    Main UI Layout
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.epLayout)
        self.mainLayout.addLayout(self.shLayout)
        self.mainLayout.addWidget(self.movTreeWidget)
        self.mainLayout.addWidget(self.publishButton)
        
        #    Set main layout for UI
        self.setLayout(self.mainLayout)
        
        #    Populate episode comboBox
        self.populateComboList()
        
        #    Populate shot folder comboBox
        self.epComboBox.currentIndexChanged[str].connect(self.populateShotComboList)
        self.epComboBox.setCurrentIndex(1)
        self.epComboBox.setCurrentIndex(0)
        
        self._getMovFiles()
        self.shComboBox.currentIndexChanged[str].connect(self._getMovFiles)
        
        
        #    Set window title
        self.setWindowTitle("Publish Playblast Tool v%s" % toolVersion)

    def publishingPath(self, episode, shotName):
        self.publishPathTemplate = 'I:/bubblebathbay/episodes/%s/%s/Blck/publish/review/' % (episode, shotName)
        return self.publishPathTemplate

    def _getEpisodeAndShotFolderList(self):
        self.epDict = {}
        for dir in os.listdir(self.movPath):
            if dir:
                if dir.startswith('ep'):
                    if os.listdir(os.path.join(self.movPath,dir)):
                        self.epDict[dir] = os.listdir(os.path.join(self.movPath,dir))
        return self.epDict
    
    def populateComboList(self):
        self.episodes = self._getEpisodeAndShotFolderList()
        self.epComboBox.addItems(sorted(self.episodes.keys()))

    @QtCore.pyqtSlot(str)
    def populateShotComboList(self, index):
        episodes = self.episodes[str(index)]
        self.shComboBox.clear()
        self.shComboBox.addItems(sorted(episodes))

    def _getMovFiles(self):
        self.movTreeWidget.clear()
        self.treeWidgetItems = []
        self.episodeFld = self.epComboBox.currentText()
        self.shotFld = self.shComboBox.currentText()
        self.epFldPath = os.path.join(self.movPath, str(self.episodeFld))
        self.shFldPath = '%s/%s' % (self.epFldPath, self.shotFld)
        for root, dirs, files in os.walk(self.shFldPath):
            for fl in sorted(files):
                if fl.endswith('.mov'):
                    treeWidgetItem = QtGui.QTreeWidgetItem([fl.split('.mov')[0]])
                    treeWidgetItem.setCheckState(0, QtCore.Qt.Checked)
                    self.treeWidgetItems.append(treeWidgetItem)
        self.movTreeWidget.addTopLevelItems(self.treeWidgetItems)

    def _moveFilesToPublish(self):
        base_url    = "http://bubblebathbay.shotgunstudio.com"
        script_name = 'playBlastPublisher'
        api_key     = '718daf67bfd2c7e974f24e7cbd55b86bb101c4e5618e6d5468bc4145840e4558'

        sgsrv = Shotgun(base_url = base_url , script_name = script_name, api_key = api_key, ensure_ascii=True, connect=True)
        selectedShots = [item.text(0) for item in self.treeWidgetItems if item.checkState(0)]
        if selectedShots:
            for each in selectedShots:
                episode = each.split('sh')[0]
                shotName = '%s_sh%s' % (each.split('sh')[0], each.split('sh')[1].split('Lay')[0])
                self.publishPath = self.publishingPath(episode, shotName)
                for root, dirs, files in os.walk(self.shFldPath):
                    for fl in sorted(files):
                        if fl.endswith('.mov') and fl == '%s.mov' % each:
                            srcPath = os.path.join(root,fl)
                            self.playblastName = fl
                            while os.path.exists(os.path.join(self.publishPath, fl)):
                                allFiles= os.listdir(self.publishPath)
                                publishFiles = []
                                if allFiles:
                                    for allFile in allFiles:
                                        if allFile.endswith('.mov'):
                                            publishFiles.append(allFile)
                                versionNumber = int(sorted(publishFiles)[-1].split('.v')[1].split('.mov')[0])
                                versionNumber += 1
                                if versionNumber < 10:
                                    publishFileName = '%sLayout.v%03d.mov' % (shotName.replace('_', ''), versionNumber)
                                    self.publishPath = os.path.join(self.publishPath, publishFileName)
                                    self.playblastName = os.path.basename(self.publishPath)
                                else:
                                    publishFileName = '%sLayout.v%02d.mov' % (shotName.replace('_', ''), versionNumber)
                                    self.publishPath = os.path.join(self.publishPath, publishFileName)
                                    self.playblastName = os.path.basename(self.publishPath)

                            shutil.copy2(srcPath, self.publishPath)
                            
                            publishMovPath = os.path.join(self.publishingPath(episode, shotName), self.playblastName)
                            
                            getShotTasks =  sgsrv.find_one('Shot',  filters = [["code", "is", shotName]], fields=['id', 'tasks'])

                            for key, values in getShotTasks.iteritems():
                                if key == 'tasks':
                                    for value in values:
                                        if value['name'] == 'Layout':
                                            self.taskId = value['id']
                            if self.publishPath.endswith('review'):
                                self.publishPath = os.path.join(self.publishPath,fl)
                                self.playblastName = fl
                            data = { 'project': {'type':'Project','id': 66},
                                     'code':  self.playblastName,
                                     'description': 'Layout playblast published',
                                     'sg_path_to_movie': publishMovPath,
                                     'sg_status_list': 'rev',
                                     'entity': {'type':'Shot', 'id':getShotTasks['id']},
                                     'sg_task': {'type':'Task', 'id':self.taskId},
                                     'user': {'type':'HumanUser', 'id':92} }
                            result = sgsrv.create('Version', data)
                            result2 = sgsrv.upload("Version", result['id'], publishMovPath, "sg_uploaded_movie")
                print "Done"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    pp = PublishPlayblast()
    pp.show()
    app.exec_()