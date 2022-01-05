# Arquivo para iniciar a programação
# Mudar prints para warnings.

import maya.cmds as cmds

def updateGuides():

    # Function from DpUtils ask how to use when integrate.
    def hook():
        """ Mount a dictionary with guide modules hierarchies.
            Return a dictionary with the father and children lists inside of each guide like:
            {guide{'guideModuleNamespace':"...", 'guideModuleName':"...", 'guideCustomName':"...", 'guideMirrorAxis':"...", 'guideMirrorName':"...", 'fatherGuide':"...", 'fatherNode':"...", 'fatherModule':"...", 'fatherCustomName':"...", 'fatherMirrorAxis':"...", 'fatherMirrorName':"...", 'fatherGuideLoc':"...", 'childrenList':[...]}}
        """
        hookDic = {}
        allList = cmds.ls(type='transform')
        for item in allList:
            if cmds.objExists(item+".guideBase") and cmds.getAttr(item+".guideBase") == 1:
                # module info:
                guideModuleNamespace = item[:item.find(":")]
                guideModuleName      = item[:item.find("__")]
                guideInstance        = item[item.rfind("__")+2:item.find(":")]
                guideCustomName      = cmds.getAttr(item+".customName")
                guideMirrorAxis      = cmds.getAttr(item+".mirrorAxis")
                tempAMirrorName      = cmds.getAttr(item+".mirrorName")
                guideMirrorName      = [tempAMirrorName[0]+"_" , tempAMirrorName[len(tempAMirrorName)-1:]+"_"]
                
                # get children:
                guideChildrenList = []
                childrenList = cmds.listRelatives(item, allDescendents=True, type='transform')
                if childrenList:
                    for child in childrenList:
                        if cmds.objExists(child+".guideBase"):
                            if cmds.getAttr(child+".guideBase"):
                                if cmds.getAttr(child+".guideBase") == 1:
                                    guideChildrenList.append(child)
                        if cmds.objExists(child+".hookNode"):
                            hookNode = cmds.getAttr(child+".hookNode")
                
                # get father:
                guideParentList = []
                fatherNodeList = []
                parentNode = ""
                parentList = cmds.listRelatives(item, parent=True, type='transform')
                if parentList:
                    nextLoop = True
                    while nextLoop:
                        if cmds.objExists(parentList[0]+".guideBase") and cmds.getAttr(parentList[0]+".guideBase") == 1:
                            guideParentList.append(parentList[0])
                            nextLoop = False
                        else:
                            if not fatherNodeList:
                                fatherNodeList.append(parentList[0])
                            parentList = cmds.listRelatives(parentList[0], parent=True, type='transform')
                            if parentList:
                                nextLoop = True
                            else:
                                nextLoop = False
                    if guideParentList:
                        # father info:
                        guideParent      = guideParentList[0]
                        fatherModule     = guideParent[:guideParent.find("__")]
                        fatherInstance   = guideParent[guideParent.rfind("__")+2:guideParent.find(":")]
                        fatherCustomName = cmds.getAttr(guideParent+".customName")
                        fatherMirrorAxis = cmds.getAttr(guideParent+".mirrorAxis")
                        tempBMirrorName  = cmds.getAttr(guideParent+".mirrorName")
                        fatherMirrorName = [tempBMirrorName[0]+"_" , tempBMirrorName[len(tempBMirrorName)-1:]+"_"]
                        if fatherNodeList:
                            fatherGuideLoc = fatherNodeList[0][fatherNodeList[0].find("Guide_")+6:]
                        else:
                            guideParentChildrenList = cmds.listRelatives(guideParent, children=True, type='transform')
                            if guideParentChildrenList:
                                for guideParentChild in guideParentChildrenList:
                                    if cmds.objExists(guideParentChild+'.nJoint'):
                                        if cmds.getAttr(guideParentChild+'.nJoint') == 1:
                                            if guideParent[:guideParent.rfind(":")] in guideParentChild:
                                                fatherNodeList = [guideParentChild]
                                                fatherGuideLoc = guideParentChild[guideParentChild.find("Guide_")+6:]
                    
                    # parentNode info:
                    parentNode = cmds.listRelatives(item, parent=True, type='transform')[0]
                
                # mounting dictionary:
                if guideParentList and guideChildrenList:
                    hookDic[item]={"guideModuleNamespace":guideModuleNamespace, "guideModuleName":guideModuleName, "guideInstance":guideInstance, "guideCustomName":guideCustomName, "guideMirrorAxis":guideMirrorAxis, "guideMirrorName":guideMirrorName, "fatherGuide":guideParent, "fatherNode":fatherNodeList[0], "fatherModule":fatherModule, "fatherInstance":fatherInstance, "fatherCustomName":fatherCustomName, "fatherMirrorAxis":fatherMirrorAxis, "fatherMirrorName":fatherMirrorName, "fatherGuideLoc":fatherGuideLoc, "parentNode":parentNode, "childrenList":guideChildrenList}
                elif guideParentList:
                    hookDic[item]={"guideModuleNamespace":guideModuleNamespace, "guideModuleName":guideModuleName, "guideInstance":guideInstance, "guideCustomName":guideCustomName, "guideMirrorAxis":guideMirrorAxis, "guideMirrorName":guideMirrorName, "fatherGuide":guideParent, "fatherNode":fatherNodeList[0], "fatherModule":fatherModule, "fatherInstance":fatherInstance, "fatherCustomName":fatherCustomName, "fatherMirrorAxis":fatherMirrorAxis, "fatherMirrorName":fatherMirrorName, "fatherGuideLoc":fatherGuideLoc, "parentNode":parentNode, "childrenList":[]}
                elif guideChildrenList:
                    hookDic[item]={"guideModuleNamespace":guideModuleNamespace, "guideModuleName":guideModuleName, "guideInstance":guideInstance, "guideCustomName":guideCustomName, "guideMirrorAxis":guideMirrorAxis, "guideMirrorName":guideMirrorName, "fatherGuide":"", "fatherNode":"", "fatherModule":"", "fatherInstance":"", "fatherCustomName":"", "fatherMirrorAxis":"", "fatherMirrorName":"", "fatherGuideLoc":"", "parentNode":parentNode, "childrenList":guideChildrenList}
                else:
                    hookDic[item]={"guideModuleNamespace":guideModuleNamespace, "guideModuleName":guideModuleName, "guideInstance":guideInstance, "guideCustomName":guideCustomName, "guideMirrorAxis":guideMirrorAxis, "guideMirrorName":guideMirrorName, "fatherGuide":"", "fatherNode":"", "fatherModule":"", "fatherInstance":"", "fatherCustomName":"", "fatherMirrorAxis":"", "fatherMirrorName":"", "fatherGuideLoc":"", "parentNode":parentNode, "childrenList":[]}
        return hookDic

    def getAttrValue(baseGuide, attr):
        try:
            return cmds.getAttr(baseGuide+'.'+attr, silent=True)
        except:
            return ''
    # Recebe o dicionário com as guias e busca os atributos do dpAr
    def getAttribs(guidesDictionary):
        for baseGuide in guidesDictionary:
            guideVersion = cmds.getAttr(baseGuide+'.dpARVersion', silent=True)
            # print(baseGuide+' version: '+guideVersion)
            if guideVersion != currentDpArVersion:
                # Create the database holder where the key is the baseGuide
                updateData[baseGuide] = {}
                guideAttrList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
                # listAttr(baseGuide, userDefined=True, keyable=True) -> pesquisar
                guideAttrList.extend(cmds.listAttr(baseGuide, userDefined=True))
                # print(guideAttrList)
                updateData[baseGuide]['attributes'] = {}
                for attribute in guideAttrList:
                    attributeValue = getAttrValue(baseGuide, attribute)
                    updateData[baseGuide]['attributes'][attribute] = attributeValue
            else:
                print('marcar como guia a ser usada')
            print(updateData[baseGuide]['attributes'])

    # Dictionary that will hold data for update
    updateData = {}
    # How to check this on dpAr?
    currentDpArVersion = '3.12.0'
    # Receive the guides list from hook function
    guidesDictionary = hook()
    # print(guidesDictionary)
    # If there are guides on the dictionary go on.
    if len(guidesDictionary) > 0:
        getAttribs(guidesDictionary)
    else:
        print('Não há guias na cena')

updateGuides();