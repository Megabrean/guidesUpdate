# Arquivo para iniciar a programação
# Mudar prints para warnings.

import maya.cmds as cmds

def updateGuides():

    # ----------
    # FUNCTIONS FROM DPAR
    # ----------
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

        """ This method will create a new module instance for a duplicated guide found.
            Returns a guideBase for a new module instance.
        """
        # Duplicating a module guide
        # print self.langDic[self.langName]['i067_duplicating']

        # declaring variables
        transformAttrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        nSegmentsAttr = "nJoints"
        customNameAttr = "customName"
        mirrorAxisAttr = "mirrorAxis"
        dispAnnotAttr = "displayAnnotation"

        # unparenting
        parentList = cmds.listRelatives(selectedItem, parent=True)
        if parentList:
            cmds.parent(selectedItem, world=True)
            selectedItem = selectedItem[selectedItem.rfind("|"):]

        # getting duplicated item values
        moduleNamespaceValue = cmds.getAttr(selectedItem+"."+"moduleNamespace")
        moduleInstanceInfoValue = cmds.getAttr(selectedItem+"."+"moduleInstanceInfo")
        # generating naming values
        origGuideName = moduleNamespaceValue+":"+"Guide_Base"
        thatClassName = moduleNamespaceValue.partition("__")[0]
        thatModuleName = moduleInstanceInfoValue[:moduleInstanceInfoValue.rfind(thatClassName)-1]
        thatModuleName = thatModuleName[thatModuleName.rfind(".")+1:]
        moduleDir = moduleInstanceInfoValue[:moduleInstanceInfoValue.rfind(thatModuleName)-1]
        moduleDir = moduleDir[moduleDir.rfind(".")+1:]

        # initializing a new module instance
        newGuideInstance = eval('self.initGuide("'+thatModuleName+'", "'+moduleDir+'")')
        newGuideName = cmds.ls(selection=True)[0]
        newGuideNamespace = cmds.getAttr(newGuideName+"."+"moduleNamespace")
        
        # reset radius as original
        origRadius = cmds.getAttr(moduleNamespaceValue+":"+"Guide_Base"+"_RadiusCtrl.translateX")
        cmds.setAttr(newGuideName+"_RadiusCtrl.translateX", origRadius)
        
        # getting a good attribute list
        toSetAttrList = cmds.listAttr(selectedItem)
        guideBaseAttrIdx = toSetAttrList.index("guideBase")
        toSetAttrList = toSetAttrList[guideBaseAttrIdx:]
        toSetAttrList.remove("guideBase")
        toSetAttrList.remove("moduleNamespace")
        toSetAttrList.remove(customNameAttr)
        toSetAttrList.remove(mirrorAxisAttr)
        
        # check for special attributes
        if cmds.objExists(selectedItem+"."+nSegmentsAttr):
            toSetAttrList.remove(nSegmentsAttr)
            nJointsValue = cmds.getAttr(selectedItem+'.'+nSegmentsAttr)
            if nJointsValue > 1:
                newGuideInstance.changeJointNumber(nJointsValue)
        if cmds.objExists(selectedItem+"."+customNameAttr):
            customNameValue = cmds.getAttr(selectedItem+'.'+customNameAttr)
            if customNameValue != "" and customNameValue != None:
                newGuideInstance.editUserName(customNameValue)
        if cmds.objExists(selectedItem+"."+mirrorAxisAttr):
            mirroirAxisValue = cmds.getAttr(selectedItem+'.'+mirrorAxisAttr)
            if mirroirAxisValue != "off":
                newGuideInstance.changeMirror(mirroirAxisValue)
        if cmds.objExists(selectedItem+"."+dispAnnotAttr):
            toSetAttrList.remove(dispAnnotAttr)
            currentDisplayAnnotValue = cmds.getAttr(selectedItem+'.'+dispAnnotAttr)
            newGuideInstance.displayAnnotation(currentDisplayAnnotValue)
        
        # get and set transformations
        childrenList = cmds.listRelatives(selectedItem, children=True, allDescendents=True, fullPath=True, type="transform")
        if childrenList:
            for child in childrenList:
                if not "|Guide_Base|Guide_Base" in child:
                    newChild = newGuideNamespace+":"+child[child.rfind("|")+1:]
                    for transfAttr in transformAttrList:
                        try:
                            cmds.setAttr(newChild+"."+transfAttr, cmds.getAttr(child+"."+transfAttr))
                        except:
                            pass
        # set transformation for Guide_Base
        for transfAttr in transformAttrList:
            cmds.setAttr(newGuideName+"."+transfAttr, cmds.getAttr(selectedItem+"."+transfAttr))
        
        # setting new guide attributes
        for toSetAttr in toSetAttrList:
            try:
                cmds.setAttr(newGuideName+"."+toSetAttr, cmds.getAttr(selectedItem+"."+toSetAttr))
            except:
                if cmds.getAttr(selectedItem+"."+toSetAttr):
                    cmds.setAttr(newGuideName+"."+toSetAttr, cmds.getAttr(selectedItem+"."+toSetAttr), type="string")
        
        # parenting correctly
        if parentList:
            cmds.parent(newGuideName, parentList[0])

        cmds.delete(selectedItem)
        return newGuideName
    # ----------
    # END OF FUNCTIONS FROM DPAR
    # ----------

    # Remove objects different from transform and nurbscurbe from list.
    def filterNurbsCurveAndTransform(mayaObjList):
        returList = []
        for obj in mayaObjList:
            objType = cmds.objectType(obj)
            if objType == 'nurbsCurve' or objType == 'transform':
                returList.append(obj)
        return returList
    
    # Remove _Ant items from list of transforms
    def filterAnt(dpArTransformsList):
        returList = []
        for obj in dpArTransformsList:
            if not '_Ant' in obj:
                returList.append(obj)
        return returList

    def getAttrValue(baseGuide, attr):
        try:
            return cmds.getAttr(baseGuide+'.'+attr, silent=True)
        except:
            return ''
    
    # Return a list of attributes, keyable and userDefined
    def keyUserAttrList(objWithAttr):
        returnList = []
        keyable = cmds.listAttr(objWithAttr, keyable=True)
        if keyable:
            returnList.extend(keyable)
        userAttr = cmds.listAttr(objWithAttr, userDefined=True)
        if userAttr:
            returnList.extend(userAttr)
        return returnList
    
    def getGuideParent(baseGuide):
        try:
            return cmds.listRelatives(baseGuide, parent=True)[0]
        except:
            return None

    # Receive a dictionary with guides and searches for custom attributes and also keyable attributes
    def getGuidesData(guidesDictionary):
        for baseGuide in guidesDictionary:
            guideVersion = cmds.getAttr(baseGuide+'.dpARVersion', silent=True)
            # print(baseGuide+' version: '+guideVersion)
            if guideVersion != currentDpArVersion:
                # Create the database holder where the key is the baseGuide
                updateData[baseGuide] = {}
                guideAttrList = keyUserAttrList(baseGuide)
                # Create de attributes dictionary for each baseGuide
                updateData[baseGuide]['attributes'] = {}
                for attribute in guideAttrList:
                    attributeValue = getAttrValue(baseGuide, attribute)
                    updateData[baseGuide]['attributes'][attribute] = attributeValue
                
                updateData[baseGuide]['children'] = {}
                updateData[baseGuide]['parent'] = getGuideParent(baseGuide)
                # print(updateData[baseGuide]['parent'])
                childrenList = cmds.listRelatives(baseGuide, allDescendents=True, children=True, type='transform')
                childrenList = filterNurbsCurveAndTransform(childrenList)
                childrenList = filterAnt(childrenList)
                for child in childrenList:
                    updateData[baseGuide]['children'][child] = {'attributes': {}}
                    # print(child)
                    guideAttrList = keyUserAttrList(child)
                    for attribute in guideAttrList:
                        attributeValue = getAttrValue(child, attribute)
                        updateData[baseGuide]['children'][child]['attributes'][attribute] = attributeValue
                    # print(updateData[baseGuide]['children'][child]['attributes'])
                # print(childrenList)
            else:
                print('marcar como guia a ser usada')
    
    def renameGuides(guidesDictionary):
        print('rename')

    # Dictionary that will hold data for update
    updateData = {}
    # How to check this on dpAr?
    currentDpArVersion = '3.13.00'
    # Receive the guides list from hook function
    guidesDictionary = hook()
    # If there are guides on the dictionary go on.
    if len(guidesDictionary) > 0:
        getGuidesData(guidesDictionary)
        renameGuides(guidesDictionary)
    else:
        print('Não há guias na cena')

updateGuides();