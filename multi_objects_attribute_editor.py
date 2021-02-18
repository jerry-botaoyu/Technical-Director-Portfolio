import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

BUTTON_HEIGHT = 50
OUTPUT_HEIGHT = 50
ROW_SPACING = 10
# IMPORTANT: this script only works on the following object: transform, and mesh.
# TODO: specifying what attributes are normally modified will optimize this script. 
#       this is because each object will have about 200 attributes and not all of these attributes
#       should be copied onto the child objects.

g_transform_attributes = {}
g_mesh_attributes = {}
g_new_transform_attributes = {}
g_new_mesh_attributes = {}
diff_transform_attributes = {}
diff_mesh_attributes = {}

#there are attributes that should be locked no matter what
IGNORED_ATTRIBUTE = ["translateX", "translateY", "translateZ"] 

def initializeEditor():
    cmds.window( width=350, title="Multiple Object Attribute Editor" )
    cmds.columnLayout( rs=ROW_SPACING, cw=20, columnAttach=('both', 20), adjustableColumn=True )
    cmds.text("padding", label=" ")
    cmds.text("output", label="Select the parent object and click the 'record INITIAL attributes' button", height=OUTPUT_HEIGHT, wordWrap=True)
    cmds.button( label="record INITIAL attributes", command=getInitialAttributes, height=BUTTON_HEIGHT)
    cmds.button( label="save MODIFIED attributes", command=getModifiedAttributes,  height=BUTTON_HEIGHT)
    cmds.button( label="apply to children", command=followParent, height=BUTTON_HEIGHT)
    cmds.showWindow()

initializeEditor()

# Reinitializes parent objects, and their attributes. 
def getInitialAttributes(self):
    cmds.text("output", edit=True, label="INITIAL Attributes has been recorded! You may now modify the parent's attributes. \n" +
              "After the modification, Cllick on the 'save MODIFIED attributes'")
    print "---------------------------------------------- getParent"
    global g_transform_attributes, g_mesh_attributes
    g_transform_attributes = {}
    g_mesh_attributes = {}
    g_new_transform_attributes = {}
    g_new_mesh_attributes = {}
    parentObjs = cmds.ls(selection=True, dag=True)
    # get the initial attributes
    callBacksForRightType(populateObj, parentObjs, g_transform_attributes, g_mesh_attributes)

def getModifiedAttributes(self):
    cmds.text("output", edit=True, label="MODIFIED Attributes has been recorded! You may now select the children objects. \n" +
              "After selecting them, Cllick on the 'apply to children'")
    global g_transform_attributes, g_mesh_attributes, g_new_transform_attributes, g_new_mesh_attributes
    global diff_transform_attributes, diff_mesh_attributes
    parentObjs = cmds.ls(selection=True, dag=True)
    # get the new attributes, after parent's attributes have changed
    callBacksForRightType(populateObj, parentObjs, g_new_transform_attributes, g_new_mesh_attributes)
    diff_transform_attributes = get_differences_between(g_new_transform_attributes, g_transform_attributes)
    diff_mesh_attributes = get_differences_between(g_new_mesh_attributes, g_mesh_attributes)

# Copies parent objects' attributes into child objects' attributes                
def followParent(self):
    cmds.text("output", edit=True, label="Select the parent object and click the 'record INITIAL attributes' button")
    global diff_transform_attributes, diff_mesh_attributes
    childObjs = cmds.ls(selection=True, dag=True)
    callBacksForRightType(setChildAttributes, childObjs, diff_transform_attributes, diff_mesh_attributes)

# find the difference of x and y dictionaries. if there is a difference, keep value of x.
def get_differences_between(x, y):
    return {k: x[k] for k in x if k in y and x[k] != y[k]}

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

# modifies the correct attributes' type depending on the objects' type
def callBacksForRightType(callBackFunction, objs, transformAttributes, meshAttributes):
    for obj in objs: 
        if cmds.objectType(obj) == "transform":
            callBackFunction(obj, transformAttributes)
        elif cmds.objectType(obj) == "mesh":
            callBackFunction(obj, meshAttributes)
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
                print 'attempting to set ', fullAttributeName, ' to ', objAttributesReference[attribute] 
                cmds.setAttr(fullAttributeName, objAttributesReference[attribute])
            except:
                errorAttributes.append(fullAttributeName)
    print "For ", objName, ", values cannot get from these attributes: ", errorAttributes


