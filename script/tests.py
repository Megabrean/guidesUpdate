import maya.cmds as cmds

attrList = cmds.listAttr('Limb__dpAR_1:Guide_Base', userDefined=True)
# print(attrList)
objAttrAndValues = {}
objAttrAndValues['Limb__dpAR_1:Guide_Base'] = {}
# print(objAttrAndValues)
for attr in attrList:
    try:
        objAttrAndValues['Limb__dpAR_1:Guide_Base'][attr] = cmds.getAttr('Limb__dpAR_1:Guide_Base.'+attr, silent=True)
    except:
        objAttrAndValues['Limb__dpAR_1:Guide_Base'][attr] = ''

print(objAttrAndValues)
