import os

# episode = None
# shotName = None
# srcTask = 'Comp'
# dstTask = 'Light'
# version = None
# fileName = None
# srcPath = 'I:/bubblebathbay/episodes/%s/%s/%s/publish/nuke/%s' % (episode, shotName, srcTask,fileName)

# fileName = 'eptst2_shot001_shotCam.v016.abc'
class BubbleBathBayUtils_Cl(object):

    def versionNumber(self, fileName):
        name, version, ext = fileName.split('.')[0], fileName.split('.')[1],fileName.split('.')[-1]
        yield (name, version, ext)
    
    def getEpisodesPath(self, path='I:/bubblebathbay/episodes'):
        episodes = [ep for ep in sorted(os.listdir(path)) if ep.startswith('ep')]
#         print episodes
        episodesPath = {}
#         shotsPath = []
        for ep in episodes:
            epPath = os.path.join(path, ep)
            episodesPath[ep] = epPath.replace('\\', '/')
#             shotPath = self.getShotPath(epPath.replace('\\', '/'))
#             shotsPath.append(shotPath)
        return episodesPath
    
    def getShotPath(self, epPath):
        shots = [shot for shot in os.listdir(epPath) if shot.startswith('ep')]
        shotsPath = {}
        for shot in shots:
            shotPath = os.path.join(epPath, shot)
            shotsPath[shot] = shotPath.replace('\\', '/')
        return shotsPath
    
    def getTaskPath(self, shotPath,task):
        tasks = ["AFX", "animatic", "Anm", "Blck", "Comp", "editorial", "FX", "Light", "SBoard"]
        for tassk in tasks:
            if task == tassk:
                return tassk

if __name__ == '__main__':
    abc = BubbleBathBayUtils_Cl()
    print abc.getEpisodesPath()
