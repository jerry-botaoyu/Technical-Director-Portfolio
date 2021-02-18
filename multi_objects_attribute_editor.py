import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

BUTTON_HEIGHT = 50
OUTPUT_HEIGHT = 30
# IMPORTANT: this script only does the transformNode, and does NOT do the shapeNode. This is why castShadows attributes
#            cannot be edited using this script.

# NOTE: the naming covention for shape change. For example, when creating 2 identical cubes, it will be cube1, and cube2.
#       their respective shape node will be cubeShape1 and cubeShape2. However, if you rename the cube as cube3, and cube4.
#       their respective shape node will be cube3Shape and cube4Shape.

# TODO: verify the node names are used correctly
# TODO: do other node such as shape, poly (cube, plane, etc.)

transformNodeAttributes = {}

IGNORED_ATTRIBUTE = ["translateX", "translateY", "translateZ"] 

def initializeEditor():
    cmds.window( width=350, title="Multiple Object Attribute Editor" )
    cmds.columnLayout( adjustableColumn=True )
    output = cmds.text(label="Step 1: Adjust the parent attributes", height=OUTPUT_HEIGHT)
    cmds.button( label="Step 2: Make the slected object as the parent object", command=getParent, bgc=[1, 1, 0.04], height=BUTTON_HEIGHT)
    cmds.button( label="Step 3: Make the childs' attributes same as parent", command=followParent, bgc=[0.47, 1, 0.04], height=BUTTON_HEIGHT)
    cmds.showWindow()

def getParent(self):
    global transformNodeAttributes
    transformNodeAttributes = {}
    parentObj = cmds.ls(selection=True)[0]
    allAttributes = cmds.listAttr(parentObj)
    for attribute in allAttributes:
        fullAttributeName = parentObj + '.' + attribute
        value = None
        try:
            value = cmds.getAttr(fullAttributeName, sl=True)
        except:
            print "Error for " + fullAttributeName
        transformNodeAttributes[attribute] = value
        #print attribute + ": ", value
                
def followParent(self):
    childObjs = cmds.ls(selection=True)
    for childObj in childObjs: 
        for attribute in transformNodeAttributes:
            fullAttributeName = childObj + '.' + attribute
            if attribute not in IGNORED_ATTRIBUTE:
                try:
                    cmds.setAttr(fullAttributeName, transformNodeAttributes[attribute])
                except:
                    print "Error for " + fullAttributeName
