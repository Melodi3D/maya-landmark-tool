"""
Landmark Tool by Melodi
"""

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance
from PySide6 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys
import os

# landmark functions

# color presets
red = (1.0, 0.0, 0.0)
orange = (1.0, 0.5, 0.0)
yellow =  (1.0, 1.0, 0.0)
green = (0.0, 1.0, 0.0)
blue = (0.0, 0.0, 1.0)
magenta = (1.0, 0.0, 1.0)
cyan = (0.0, 1.0, 1.0)
pink = (1.0, 0.4, 0.7)

#function for confirming faces are selected
def faces_confirm():
    cmds.confirmDialog(
        title="Landmark Tool",
        message="Please select at least one polygon face.",
        button=["OK"]
    )
    
# function for creating landmarks
def create_landmark(colors):
    #user selects faces

    selection = cmds.ls(sl=True, flatten=True)

    # filters the selection to polygon faces
    faces = cmds.filterExpand(sm=34)

    # error handling due to no selection
    if not selection:
        raise RuntimeError("Error: Nothing is selected")

    # error handling due to no faces in selection
    if not faces:
        faces_confirm()
        raise RuntimeError("Error: No faces selected")

    # error handling due to wrong colors
    for color in colors:
        if color < 0.0 or color > 1.0:
            raise RuntimeError("Error: Colors should be between 0.0 and 1.0 ")

    #creates landmark shader as a shader node, with lambert material

    landmark_shader = cmds.shadingNode("lambert", asShader=True)
    
    # selects faces
    cmds.select(faces)

    #assigns shader to the selected faces
    cmds.hyperShade(assign=landmark_shader)

    #sets the colors for the landmark shader to RGB values

    cmds.setAttr(

    f"{landmark_shader}.color",

    colors[0], colors[1], colors[2],

    type="double3")


class landmarkTool(QtWidgets.QWidget):
    """
    Creates tool window
    """
    window = None

    def __init__(self, parent=None):
        """
        Initialize class
        """
        super(landmarkTool, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)

        self.widgetPath = os.path.dirname(os.path.abspath(__file__))
        self.widget = QtUiTools.QUiLoader().load(
            os.path.join(self.widgetPath, "landmarkTool.ui")
        )
        self.widget.setParent(self)
        # set initial window size
        self.resize(600, 850)
        # locate UI widgets
        self.btn_close = self.widget.findChild(QtWidgets.QPushButton, 'btn_close')
        # assign functionality to buttons
        self.btn_close.clicked.connect(self.close)

    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())

def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName():  # update this name to match name below
                win.destroy()

    # QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    landmarkTool.window = landmarkTool(parent=mayaMainWindow)
    landmarkTool.window.setObjectName('myToolWindowName')  # code above uses this to ID any existing windows
    landmarkTool.window.setWindowTitle('landmarkTool Ui')
    landmarkTool.window.show()
