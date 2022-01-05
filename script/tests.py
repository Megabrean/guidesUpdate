import maya.cmds as cmds

""" attrList = cmds.listAttr('Spine__dpAR_1:Guide_Base', userDefined=True)
print(attrList)
objAttrAndValues = {}
objAttrAndValues['Spine__dpAR_1:Guide_Base'] = {}
print(objAttrAndValues)
for attr in attrList:
    try:
        objAttrAndValues['Spine__dpAR_1:Guide_Base'][attr] = cmds.getAttr('Spine__dpAR_1:Guide_Base.'+attr, silent=True)
    except:
        objAttrAndValues['Spine__dpAR_1:Guide_Base'][attr] = ''

print(objAttrAndValues) """


print(cmds.listAttr(cmds.ls(selection=True), keyable=True))

[u'FkLine__dpAR_1:Guide_Base_RadiusCtrl', u'FkLine__dpAR_1:Guide_Base_Ant', u'FkLine__dpAR_1:Guide_JointEnd', u'FkLine__dpAR_1:Guide_JointLoc3', u'FkLine__dpAR_1:Guide_JointLoc2', u'FkLine__dpAR_1:Guide_JointLoc1']
