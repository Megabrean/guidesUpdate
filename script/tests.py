from maya import cmds

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


# print(cmds.listAttr(cmds.ls(selection=True), keyable=True))

# [u'FkLine__dpAR_1:Guide_Base_RadiusCtrl', u'FkLine__dpAR_1:Guide_Base_Ant', u'FkLine__dpAR_1:Guide_JointEnd', u'FkLine__dpAR_1:Guide_JointLoc3', u'FkLine__dpAR_1:Guide_JointLoc2', u'FkLine__dpAR_1:Guide_JointLoc1']

# print(dir(autoRigUI))
# dir(autoRig)
autoRigUI.setupDuplicatedGuide('Head__dpAR_2:Guide_Base')

{u'Head__dpAR_2:Guide_Base': {'fatherMirrorAxis': u'off', 'guideModuleNamespace': u'Head__dpAR_2', 'fatherModule': u'Spine', 'fatherCustomName': u'Spine', 'fatherNode': u'Spine__dpAR_1:Guide_JointLoc3', 'parentNode': u'Spine__dpAR_1:Guide_JointLoc3', 'guideInstance': u'dpAR_2', 'guideMirrorAxis': u'off', 'fatherMirrorName': [u'L_', u'R_'], 'childrenList': [], 'fatherGuideLoc': u'JointLoc3', 'guideCustomName': u'Head', 'fatherGuide': u'Spine__dpAR_1:Guide_Base', 'fatherInstance': u'dpAR_1', 'guideModuleName': u'Head', 'guideMirrorName': [u'L_', u'R_']}, u'Spine__dpAR_1:Guide_Base': {'fatherMirrorAxis': '', 'guideModuleNamespace': u'Spine__dpAR_1', 'fatherModule': '', 'fatherCustomName': '', 'fatherNode': '', 'parentNode': '', 'guideInstance': u'dpAR_1', 'guideMirrorAxis': u'off', 'fatherMirrorName': '', 'childrenList': [u'Head__dpAR_2:Guide_Base'], 'fatherGuideLoc': '', 'guideCustomName': u'Spine', 'fatherGuide': '', 'fatherInstance': '', 'guideModuleName': u'Spine', 'guideMirrorName': [u'L_', u'R_']}}