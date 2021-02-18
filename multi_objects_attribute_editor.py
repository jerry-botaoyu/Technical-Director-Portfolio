import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

BUTTON_HEIGHT = 50
OUTPUT_HEIGHT = 30
# IMPORTANT: this script only works on the following object: transform, and mesh.
# TODO: specifying what attributes are normally modified will optimize this script. 
#       this is because each object will have about 200 attributes and not all of these attributes
#       should be copied onto the child objects.

transformObjAttributes = {}
meshObjAttributes = {}

#there are attributes that should be locked no matter what
IGNORED_ATTRIBUTE = ["translateX", "translateY", "translateZ"] 

def initializeEditor():
    cmds.window( width=350, title="Multiple Object Attribute Editor" )
    cmds.columnLayout( adjustableColumn=True )
    output = cmds.text(label="Step 1: Adjust the parent attributes", height=OUTPUT_HEIGHT)
    cmds.button( label="Step 2: Make the slected object as the parent object", command=getParent, bgc=[1, 1, 0.04], height=BUTTON_HEIGHT)
    cmds.button( label="Step 3: Make the childs' attributes same as parent", command=followParent, bgc=[0.47, 1, 0.04], height=BUTTON_HEIGHT)
    cmds.showWindow()

# Reinitializes parent objects, and their attributes. 
def getParent(self):
    transformObjAttributes = {}
    meshObjAttributes = {}
    parentObjs = cmds.ls(selection=True, dag=True)
    callBacksForRightType(populateObj, parentObjs)
    

# Populates the attributes of parent objects
def populateObj(objName, objAttributesReference):
    print "---------------------------------------------- populateObj"
    errorAttributes = []
    allAttributes = cmds.listAttr(objName)
    for attribute in allAttributes:
        fullAttributeName = objName + '.' + attribute
        value = None
        try:
            value = cmds.getAttr(fullAttributeName, sl=True)
        except:
            errorAttributes.append(fullAttributeName)
        objAttributesReference[attribute] = value
    print "For ", objName, ", values cannot get from these attributes: ", errorAttributes

# Copies parent objects' attributes into child objects' attributes                
def followParent(self):
    childObjs = cmds.ls(selection=True, dag=True)
    callBacksForRightType(setChildAttributes, childObjs)

# modifies the correct attributes' type depending on the objects' type
def callBacksForRightType(callBackFunction, objs):
    global transformObjAttributes, meshObjAttributes
    for obj in objs: 
        if cmds.objectType(obj) == "transform":
            callBackFunction(obj, transformObjAttributes)
        elif cmds.objectType(obj) == "mesh":
            callBackFunction(obj, meshObjAttributes)
        else:
            print "Error: ", cmds.objectType(obj), " is unsupported."

# copies the parents' attributes into the childs' attributes
def setChildAttributes(objName, objAttributesReference):
    print "---------------------------------------------- setChildAttributes"
    errorAttributes = []
    for attribute in objAttributesReference:
        fullAttributeName = objName + '.' + attribute
        if attribute not in IGNORED_ATTRIBUTE:
            try:
                cmds.setAttr(fullAttributeName, objAttributesReference[attribute])
            except:
                errorAttributes.append(fullAttributeName)
    print "For ", objName, ", values cannot get from these attributes: ", errorAttributes


