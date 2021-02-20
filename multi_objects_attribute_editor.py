import maya.cmds as cmds

"""
Allows the user to change mesh and transform attributes of an object (this will be known as the parent object),
save the changes that the user made,
then apply the changes on multiple other objects (this will be known as the child objects).
"""

BUTTON_HEIGHT = 50
OUTPUT_HEIGHT = 50
ROW_SPACING = 10

"""parent object attributes (initial attributes) before the modification"""
g_transform_attributes = {}
g_mesh_attributes = {}
"""parent object attributes (modified attributes) after the modification"""
g_new_transform_attributes = {}
g_new_mesh_attributes = {}
"""
the difference between the initial and modified attributes,
the child objects will use the value in these attributes.
"""
g_diff_transform_attributes = {}
g_diff_mesh_attributes = {}

"""
there are attributes that should not be modified 
"""
IGNORED_ATTRIBUTE = ["translateX", "translateY", "translateZ"] 

"""
Initializes the UI elements in the editor
"""
def initialize_editor():
    cmds.window( w=350, t="Multiple Object Attribute Editor" )
    cmds.columnLayout( rs=ROW_SPACING, cw=20, cat=('both', 20), adj=True )
    cmds.text("padding", l=" ")
    cmds.text("output", l="Select the parent object and click the 'record INITIAL attributes' button", h=OUTPUT_HEIGHT, ww=True)
    cmds.button( l="record INITIAL attributes", c=get_parent_initial_attributes, h=BUTTON_HEIGHT)
    cmds.button( l="save MODIFIED attributes", c=get_parent_modified_attributes,  h=BUTTON_HEIGHT)
    cmds.button( l="apply changes to children", c=change_child_objects_attributes, h=BUTTON_HEIGHT)
    cmds.showWindow()

"""
get parent initial attributes. 
"""
def get_parent_initial_attributes(self):
    cmds.text("output", e=True, l="INITIAL Attributes has been recorded! You may now modify the parent's attributes. \n" +
              "After the modification, Cllick on the 'save MODIFIED attributes'")
    global g_transform_attributes, g_mesh_attributes
    g_transform_attributes = {}
    g_mesh_attributes = {}
    g_new_transform_attributes = {}
    g_new_mesh_attributes = {}
    parent_objects = cmds.ls(sl=True, dag=True)
    call_back_for_right_type(get_attributes, parent_objects, g_transform_attributes, g_mesh_attributes)

"""
get parent modified attributes and
get the differences between the parent initial attributes and modified attributes.
"""
def get_parent_modified_attributes(self):
    cmds.text("output", e=True, l="MODIFIED Attributes has been recorded! You may now select the children objects. \n" +
              "After selecting them, Cllick on the 'apply changes to children'")
    global g_transform_attributes, g_mesh_attributes, g_new_transform_attributes, g_new_mesh_attributes
    global diff_transform_attributes, g_diff_mesh_attributes
    parent_objects = cmds.ls(sl=True, dag=True)
    call_back_for_right_type(get_attributes, parent_objects, g_new_transform_attributes, g_new_mesh_attributes)
    g_diff_transform_attributes = get_differences_between(g_new_transform_attributes, g_transform_attributes)
    g_diff_mesh_attributes = get_differences_between(g_new_mesh_attributes, g_mesh_attributes)

"""
change the value of child objects' attributes with
the value of diff_transform_attributes and g_diff_mesh_attributes.
"""              
def change_child_objects_attributes(self):
    cmds.text("output", e=True, l="Select the parent object and click the 'record INITIAL attributes' button")
    global g_diff_transform_attributes, g_diff_mesh_attributes
    child_objects = cmds.ls(sl=True, dag=True)
    call_back_for_right_type(set_child_objects_attributes, child_objects, g_diff_transform_attributes, g_diff_mesh_attributes)

"""
find the differences of x and y dictionaries. if there is a difference, keep the value of the item in x.
"""
def get_differences_between(x, y):
    return {k: x[k] for k in x if k in y and x[k] != y[k]}

"""
get the attributes of an object
"""
def get_attributes(object_name, object_attributes_ref):
    error_attributes = []
    all_attributes = cmds.listAttr(object_name)
    for attribute in all_attributes:
        full_attribute_name = object_name + '.' + attribute
        value = None
        try:
            value = cmds.getAttr(full_attribute_name, sl=True)
        except:
            error_attributes.append(full_attribute_name)
        object_attributes_ref[attribute] = value
    print "For ", object_name, ", values cannot get from these attributes: ", error_attributes

"""
Pass the correct pair of object_name and attributes_ref as arguments to the call back function
"""
def call_back_for_right_type(call_back_function, object_names, transform_attributes_ref, mesh_attributes_ref):
    for object_name in object_names: 
        if cmds.objectType(object_name) == "transform":
            call_back_function(object_name, transform_attributes_ref)
        elif cmds.objectType(object_name) == "mesh":
            call_back_function(object_name, mesh_attributes_ref)
        else:
            print "Error: ", cmds.objectType(object_name), " is not supported."

"""
set the value of child objects' attributes using
the value of diff_transform_attributes and g_diff_mesh_attributes.
"""
def set_child_objects_attributes(object_name, object_attributes_ref):
    error_attributes = []
    for attribute in object_attributes_ref:
        full_attribute_name = object_name + '.' + attribute
        if attribute not in IGNORED_ATTRIBUTE:
            try:
                cmds.setAttr(full_attribute_name, object_attributes_ref[attribute])
            except:
                error_attributes.append(full_attribute_name)
    print "For ", object_name, ", values cannot get from these attributes: ", error_attributes
