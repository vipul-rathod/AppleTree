import os, sys
import nuke, nukescripts

import sgtk

def convertWriteNode():
    eng = sgtk.platform.current_engine()
    app = eng.apps["tk-nuke-writenode"]
    nodes = app.get_write_nodes()[0]
    renderPath = app.get_node_render_path(nodes)
    basePath = os.path.dirname(renderPath)
    versionFolder = basePath.split('/')[-1]
    if not os.path.exists(basePath):
        os.mkdir(basePath)
    if app:
        app.convert_to_write_nodes()