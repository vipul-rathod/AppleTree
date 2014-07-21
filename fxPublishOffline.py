import maya.cmds as cmds
import sgtk, sys

#    Save file to publish folder with version up

class PublishAFX(object):
    def __init__(self):
        self.tk = sgtk.sgtk_from_path("T:/software/bubblebathbay_sandbox")

    def saveFileToPublish(self):
        self.currentFilePath = cmds.file(q=1, sn=1)
        if self.currentFilePath:
            if '/work/' in self.currentFilePath:
                self.baseName = os.path.basename(self.currentFilePath)
                self.publishPath = self.currentFilePath.split(self.baseName)[0].replace('/work/', '/publish/')
                self.publishFilePath = os.path.join(self.publishPath, self.baseName)
                if os.listdir(self.publishPath):
                    fileName = sorted(os.listdir(self.publishPath))[-1].replace('.ma', '.mb')
                    newPublishFilePath = os.path.join(self.publishPath, fileName)
                    curVersion = os.path.splitext(fileName)[0].split('.v')[-1]
                    newVersion = int(curVersion) + 1
                    newVersionStr = '.v%03d' % newVersion
                    self.publishFilePath = newPublishFilePath.replace('.v%03d' % int(curVersion), newVersionStr)
                    cmds.file(f=1, save=1)
                    cmds.file(rename=self.publishFilePath)
                    cmds.file(f=1, save=1, type = 'mayaBinary')
                    cmds.file(self.currentFilePath, f=1, open=1)
                    return self.publishFilePath
                else:
                    fileName = self.baseName.replace('.ma', '.mb')
                    newPublishFilePath = os.path.join(self.publishPath, fileName)
                    self.publishFilePath = newPublishFilePath
                    cmds.file(f=1, save=1)
                    cmds.file(rename=self.publishFilePath)
                    cmds.file(f=1, save=1, type = 'mayaBinary')
                    cmds.file(self.currentFilePath, f=1, open=1)
                    return self.publishFilePath
            else:
                cmds.confirmDialog(m="File is not in work directory.. Kindly save your file in work directory and run this script", b="Ok")
        else:
            cmds.warning('Cannot find proper file. Please save our file and proceed....')

    def registerOnShotgun(self):
        self.fileToPublish = self.saveFileToPublish().replace('/', '\\')
        fileName = os.path.basename(self.fileToPublish)
        version = os.path.splitext(fileName)[0].split('.v')[-1]
        ctx = self.tk.context_from_path(self.fileToPublish)
        sgtk.util.register_publish(self.tk, ctx, self.fileToPublish, fileName, int(version))
        sys.stderr.write("Publish Done!!!!!")

if __name__ == "__main__":
    publishAFX = PublishAFX()
    publishAFX.registerOnShotgun()
