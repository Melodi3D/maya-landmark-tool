"""
Landmark Tool by Melodi
"""
# Explanation:
# imports maya commands
from maya import cmds

# color presets
red = (1.0, 0.0, 0.0)
orange = (1.0, 0.5, 0.0)
yellow =  (1.0, 1.0, 0.0)
green = (0.0, 1.0, 0.0)
blue = (0.0, 0.0, 1.0)
magenta = (1.0, 0.0, 1.0)
cyan = (0.0, 1.0, 1.0)
pink = (1.0, 0.4, 0.7)

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

create_landmark(red)
