from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, sip, maya
import pymel.core as pm

class SetAovsUi(QWidget):
    def __init__(self, parent=None):
        super(SetAovsUi, self).__init__(parent)
        self.initUi(parent)
        sys.stdout.write('Set Aovs Ui opened\n')

    def initUi(self, parent):
        win = QWidget(self.getMayaMainWindow())
        win.setWindowFlags(Qt.Tool)
        if pm.window('setAovs', ex=1):
            pm.deleteUI('setAovs')
        if pm.windowPref('setAovs', exists = True):
            pm.windowPref('setAovs', remove = True)
        self.setAovsUi = pm.window('setAovs', t='Set Aovs')
        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        font = QFont("SansSerif", 10)
        self.treeWidget.setFont(font)
        self.treeWidget.setFocusPolicy(Qt.ClickFocus)
        self.addAovsButton = QPushButton('Additional Aovs')    #    Add Button to refer new Aovs
        self.addItems(self.treeWidget.invisibleRootItem())    #    Add items in treeWidget
        self.treeWidget.itemChanged.connect (self.handleChanged)    #    connect checkBox
        self.treeWidget.itemSelectionChanged.connect(self.changeRenderLayer)    #    connect selection changed SIGNAL.. Used for selecting current render layer
        self.addAovsButton.clicked.connect(self.addAovs)    #    connect button with SIGNAL
        self.layout = QVBoxLayout()    #    Layout QWidgets
        self.layout.addWidget(self.treeWidget)
        self.layout.addWidget(self.addAovsButton)
        self.resize(300, 400)
        self.setLayout(self.layout)    #    Set layout and Window title
        self.setWindowTitle('Set Aovs')

#    Get render layers funtion
    def getRenderLayers(self):
        renderLayers = [layer for layer in pm.ls(type='renderLayer') if not layer.endswith("defaultRenderLayer")]
        return renderLayers

#    Add items to tree widget function
    def addItems(self, parent):
        column = 0
        self.renderLayers = self.getRenderLayers()    #    Get render layers
        self.renderLayerDict = {}    #    Dictionary to store layer name and the assosiated AOVS
        for layer in self.renderLayers:
            if str(layer.name()) not in self.renderLayerDict:
                self.renderLayerDict[str(layer.name())] = []    #    Add elements to Dictionary as Key with empty list as value
#            vrayRenderElements = pm.listConnections(layer, s=1, type='VRayRenderElement')    #    Find all the AOVS connected to each render layers and Append to the Dictionary self.renderLayerDict[Key] = Value
            vrayRenderElements = pm.ls(type='VRayRenderElement')
            for element in vrayRenderElements:
                if element.name() not in self.renderLayerDict[str(layer.name())]:
                    self.renderLayerDict[str(layer.name())].append(str(element.name()))
#            vrayRenderElementSets = pm.listConnections(layer, s=1, type='VRayRenderElementSet')
            vrayRenderElementSets = pm.ls(type='VRayRenderElementSet')
            for set in vrayRenderElementSets:
                if set.name() not in self.renderLayerDict[str(layer.name())]:
                    self.renderLayerDict[str(layer.name())].append(str(set.name()))
        panels = pm.getPanel( type='modelPanel' )    #    Get all the Model panels and Set show to None
        for panel in panels:
            if '|' in panel:
                panel = panel.split('|')[-1]
                pm.modelEditor(panel, e=1, allObjects=0)

        for key, values in self.renderLayerDict.iteritems():     #    Update tree widget with top parent node as render layer name and childs as Aovs
            pm.editRenderLayerGlobals(currentRenderLayer=key)    #    select current render layer and find the Aovs state (Enabled or Disabled)
            layer_item = self.addParent(parent, column, key, 'data Layers')
            for value in sorted(values):
                self.addChild(layer_item, column, value, 'data Aovs')

#    Function to Add Parent Items to tree widget
    def addParent(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setBackgroundColor(column, QColor(60,60,60))
        item.setData(column, Qt.UserRole, data)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded (False)
        return item

#    Function to Add Child Items to tree widget with Check box
    def addChild(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setBackgroundColor(column, QColor(70,70,70))
        item.setData(column, Qt.UserRole, data)
        queryAov = pm.getAttr('%s.enabled' % item.text(column))    #    Get current state of Aovs to turn the the checkbox On/Off
        pm.editRenderLayerAdjustment('%s.enabled' % item.text(column))
        if queryAov:
            item.setCheckState (column, Qt.Checked)
        else:
            item.setCheckState (column, Qt.Unchecked)
        return item

#    Function to enable and disable Aovs, if the checkBox is turned On/Off
    def handleChanged(self, item, column):
        if item.checkState(column) == Qt.Checked:
            pm.setAttr('%s.enabled' % item.text(column), 1)
            sys.stdout.write('%s is Enabled\n' % item.text(column))
        if item.checkState(column) == Qt.Unchecked:
            pm.setAttr('%s.enabled' % item.text(column), 0)
            sys.stdout.write('%s is Disabled\n' % item.text(column))

#    Function to toggle render layer when selected in the tree widget
    def changeRenderLayer(self):
        layerName = self.treeWidget.currentItem()
        if layerName.text(0) in self.renderLayers:
            pm.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
            pm.editRenderLayerGlobals(currentRenderLayer=str(layerName.text(0)))
        else:
            layer = layerName.parent()
            pm.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
            pm.editRenderLayerGlobals(currentRenderLayer=str(layer.text(0)))

    def addAovs(self):
        fileToRef = pm.fileDialog2(dir='/jobs/loca/common/aovs', okc = 'Reference', fileFilter = '*.mb', fileMode = 4, ds=2)
        references = pm.listReferences()
        if fileToRef:
            for each in fileToRef:
                if each not in references:
                    namespace = each.split('/')[-1].split('.mb')[0]
                    pm.createReference(each, namespace = namespace)
                    pm.setAttr('%s:%s.enabled' % (namespace, namespace), 0)
                    self.renderLayers[0]
                    adjustmentPlugs = str(pm.listAttr('%s.adjustments' % self.renderLayers[0], m=1)[-3])
                    lastAdjsNum = int(adjustmentPlugs.split('[')[-1].split(']')[0])
                    newAdjsNum = lastAdjsNum + 1
                    pm.connectAttr('%s:%s.enabled' % (namespace, namespace), '%s.adjustments[%d].plug' % (self.renderLayers[0],newAdjsNum), f=1)
                    self.close()
                    self.__init__()
                    self.show()
                else:
                    fileName = each.split('/')[-1].split('.m')[0]
                    pm.warning('%s is already referenced so skipped' % fileName)
        else:
            pass
        return 0

#    Function to run PyQt UI in Maya
    def getMayaMainWindow(self):
        ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
        main_win = sip.wrapinstance(long(ptr), QObject)
        return main_win

if __name__ == '__main__':
    setAovsUi = SetAovsUi()
    setAovsUi.show()
