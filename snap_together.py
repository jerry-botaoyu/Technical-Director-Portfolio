import maya.cmds as cmds

# yMin is the minimum of the Y axis of the selectedObj
# yMax is the the maximum of the Y axis of selectedPlane 
yMin = yMax = selectedObj = selectedPlane = None
BUTTON_HEIGHT = 50
OUTPUT_HEIGHT = 20

# initialize the UI elements
# main function
def initCollisionDetector():
    cmds.window( width=350, title="A clone of snap together tool" )
    cmds.columnLayout( adjustableColumn=True )
    cmds.button( label="Object", command=getSelectedObj, bgc=[1, 1, 0.04], height=BUTTON_HEIGHT)
    cmds.button( label="Plane", command=getSelectedPlane, bgc=[0.47, 1, 0.04], height=BUTTON_HEIGHT)
    cmds.button( label="Make it touch perfectly", command=touchPerfectly,bgc=[0.04, 0.81, 1], height=BUTTON_HEIGHT)
    output = cmds.text("output", label="Select Object", height=OUTPUT_HEIGHT)
    cmds.showWindow()

# get the selected object and initialize yMin    
def getSelectedObj(self):
    global yMin, selectedObj
    selectedObj = cmds.ls(selection=True)[0]
    print cmds.xform(selectedObj, q=True, bb=True)
    yMin = cmds.xform(selectedObj, q=True, bb=True)[1]
    cmds.text("output", edit=True, label="select plane")

# get the selected plane and initialize yMax
# also tell users if it is the object and plane are touching
# use align()
def getSelectedPlane(self):
    global yMin, yMax, selectedPlane
    selectedPlane = cmds.ls(selection=True)[0]
    yMax = cmds.xform(selectedPlane, q=True, bb=True)[4]
    print("yMin: " + str(yMin) + " ,yMax: " + str(yMax))
    if yMin == yMax:
        cmds.text("output", edit=True, label="it is touched perfectly")
    else:
        cmds.text("output", edit=True, label="it is not touching")

# make the the object and plane touch each other
def touchPerfectly(self):
    global selectedObj, selectedPlane
    yMin = cmds.xform(selectedObj, q=True, bb=True)[1]
    yMax = cmds.xform(selectedPlane, q=True, bb=True)[4]
    print("touchPerfectly, yMin: " + str(yMin) + " ,yMax: " + str(yMax))
    if  yMin == yMax:
        cmds.text("output", edit=True, label="no changes needed, since they are touching")
    else:
        pos = cmds.xform(selectedObj, q= 1, t= 1, ws= 1)
        if yMin > yMax:
            pos[1] -= abs(yMax-yMin)
        else:
            pos[1] += abs(yMax-yMin)
        print pos
        cmds.xform(selectedObj, t=pos)

#execute main function
initCollisionDetector()
