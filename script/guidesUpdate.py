# Mudar prints para warnings.
from maya import cmds

def reloadAr():
    global autoRigUI
    autoRigUI = autoRig.DP_AutoRig_UI()

def updateGuides():
    
    # Remove objects different from transform and nurbscurbe from list.
    def filterNotNurbsCurveAndTransform(mayaObjList):
        returList = []
        for obj in mayaObjList:
            objType = cmds.objectType(obj)
            if objType == 'nurbsCurve' or objType == 'transform':
                returList.append(obj)
        return returList
    
    # Remove _Ant(Anotations) items from list of transforms
    def filterAnotation(dpArTransformsList):
        returList = []
        for obj in dpArTransformsList:
            if not '_Ant' in obj:
                returList.append(obj)
        return returList

    def getAttrValue(dpGuide, attr):
        try:
            return cmds.getAttr(dpGuide+'.'+attr, silent=True)
        except:
            return ''
    
    def getNewGuideInstance(newGuideName):
        newGuidesNamesList = map(lambda moduleInstance : moduleInstance.moduleGrp, newGuidesInstanceList)
        currentGuideInstanceIdx = newGuidesNamesList.index(newGuideName)
        return newGuidesInstanceList[currentGuideInstanceIdx]
    
    def translateLimbStyleValue(enumValue):
        if enumValue == 1:
            return autoRigUI.langDic[autoRigUI.langName]['m026_biped']
        elif enumValue == 2:
            return autoRigUI.langDic[autoRigUI.langName]['m037_quadruped']
        elif enumValue == 3:
            return autoRigUI.langDic[autoRigUI.langName]['m043_quadSpring']
        elif enumValue == 4:
            return autoRigUI.langDic[autoRigUI.langName]['m155_quadrupedExtra']
        else:
            return autoRigUI.langDic[autoRigUI.langName]['m042_default']
    
    def translateLimbTypeValue(enumValue):
        if enumValue == 1:
            return autoRigUI.langDic[autoRigUI.langName]['m030_leg']
        else:
            return autoRigUI.langDic[autoRigUI.langName]['m028_arm']

    def setAttrValue(dpGuide, attr, value):
        try:
            cmds.setAttr(dpGuide+'.'+attr, value)
        except:
            print('the attr '+attr+' from '+dpGuide+' could not be set.')

    def setAttrStrValue(dpGuide, attr, value):
        print(value)
        try:
            cmds.setAttr(dpGuide+'.'+attr, value, type='string')
        except:
            print('the attr '+attr+' from '+dpGuide+' could not be set.')
            
    def setGuideAttributes(dpGuide, attr, value):
        ignoreList = ['version', 'controlID', 'className', 'direction', 'pinGuideConstraint', 'moduleNamespace', 'customName', 'moduleInstanceInfo', 'hookNode', 'guideObjectInfo', 'rigType', 'dpARVersion']
        if attr not in ignoreList:
            if attr == 'nJoints':
                currentInstance = getNewGuideInstance(dpGuide)
                currentInstance.changeJointNumber(value)
            elif attr == 'style':
                currentInstance = getNewGuideInstance(dpGuide)
                expectedValue = translateLimbStyleValue(value)
                currentInstance.changeStyle(expectedValue)
            elif attr == 'type':
                currentInstance = getNewGuideInstance(dpGuide)
                expectedValue = translateLimbTypeValue(value)
                currentInstance.changeType(expectedValue)
            elif attr == 'mirrorAxis':
                currentInstance = getNewGuideInstance(dpGuide)
                currentInstance.changeMirror(value)
            elif attr == 'mirrorName':
                currentInstance = getNewGuideInstance(dpGuide)
                currentInstance.changeMirrorName(value)
            elif attr == 'fatherB':
                if value in updateData:
                    setAttrStrValue(dpGuide, attr, updateData[value]['newGuide'])
                else:
                    setAttrStrValue(dpGuide, attr, value)
            else:
                setAttrValue(dpGuide, attr, value)
    
    # Return a list of attributes, keyable and userDefined
    def listKeyUserAttr(objWithAttr):
        returnList = []
        keyable = cmds.listAttr(objWithAttr, keyable=True)
        if keyable:
            returnList.extend(keyable)
        userAttr = cmds.listAttr(objWithAttr, userDefined=True)
        if userAttr:
            returnList.extend(userAttr)
        # Guaranty no duplicated attr
        returnList = list(set(returnList))
        return returnList
    
    def getGuideParent(baseGuide):
        try:
            return cmds.listRelatives(baseGuide, parent=True)[0]
        except:
            return None

    def listChildren(baseGuide):
        childrenList = cmds.listRelatives(baseGuide, allDescendents=True, children=True, type='transform')
        childrenList = filterNotNurbsCurveAndTransform(childrenList)
        childrenList = filterAnotation(childrenList)
        return childrenList

    # Scan a dictionary for old guides and gather data needed to update then.
    def getGuidesToUpdateData():

        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)

        for baseGuide in guidesDictionary:
            guideVersion = cmds.getAttr(baseGuide+'.dpARVersion', silent=True)
            if guideVersion != currentDpArVersion:
                # Create the database holder where the key is the baseGuide
                updateData[baseGuide] = {}
                guideAttrList = listKeyUserAttr(baseGuide)
                # Create de attributes dictionary for each baseGuide
                updateData[baseGuide]['attributes'] = {}
                for attribute in guideAttrList:
                    attributeValue = getAttrValue(baseGuide, attribute)
                    updateData[baseGuide]['attributes'][attribute] = attributeValue

                updateData[baseGuide]['idx'] = instancedModulesStrList.index(updateData[baseGuide]['attributes']['moduleInstanceInfo'])
                
                updateData[baseGuide]['children'] = {}
                updateData[baseGuide]['parent'] = getGuideParent(baseGuide)
                childrenList = listChildren(baseGuide)
                for child in childrenList:
                    updateData[baseGuide]['children'][child] = {'attributes': {}}
                    guideAttrList = listKeyUserAttr(child)
                    for attribute in guideAttrList:
                        attributeValue = getAttrValue(child, attribute)
                        updateData[baseGuide]['children'][child]['attributes'][attribute] = attributeValue
            else:
                # Dictionary where the keys are the guides to possible reparent and values are its current parent
                guidesToReParentDict[baseGuide] = getGuideParent(baseGuide)

    def createNewGuides():
        for guide in updateData:
            guideType = autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].guideModuleName
            # create the new guide
            currentNewGuide = autoRigUI.initGuide("dp"+guideType, "Modules")
            # rename as it's predecessor
            guideName = updateData[guide]['attributes']['customName']
            currentNewGuide.editUserName(guideName)
            updateData[guide]['newGuide'] = currentNewGuide.moduleGrp
            newGuidesInstanceList.append(currentNewGuide)

    # THE TWO FOLLOWING FUNCTIONS ARE DEBUG FUNCTIONS WILL BE CLEARED LATER, LEFT HERE FOR LEARNING PURPOSE
    # Verify if modules are loaded to memory and guarantee they are instanced
    def checkMemory():
        print('checking..')
        if len(autoRigUI.modulesToBeRiggedList) == 0:
            print('Autorig recarregado instancias nao carregadas')
            reloadAr()
            return
        print('still checking..')
        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)
        for guide in updateData:
            try:
                instancedModulesStrList.index(updateData[guide]['attributes']['moduleInstanceInfo'])
            except:
                print('Autorig recarregado devido a endereco nao encontrado')
                reloadAr()
                return

    def showInfo():
        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)
        print(instancedModulesStrList)
        print(autoRigUI.modulesToBeRiggedList)

    def renameOldGuides():
        for guide in updateData:
            currentCustomName = updateData[guide]['attributes']['customName']
            if currentCustomName == '' or currentCustomName == None:
                autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].editUserName(autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].moduleGrp.split(':')[0]+'_OLD')
            else:
                autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].editUserName(currentCustomName+'_OLD')

    def retrieveNewParent(currentParent):
        currentParentBase = currentParent.split(':')[0]+":Guide_Base"
        if currentParentBase in updateData.keys():
            newParentBase = updateData[currentParentBase]['newGuide']
            newParentFinal = newParentBase.split(':')[0]+':'+currentParent.split(':')[1]
            return newParentFinal
        else:
            return currentParent

    def parentNewGuides():
        for guide in updateData:
            hasParent = updateData[guide]['parent']
            if hasParent != None:
                newParentFinal = retrieveNewParent(hasParent)
                try:
                    cmds.parent(updateData[guide]['newGuide'], newParentFinal)
                except:
                    print('It was not possible to find '+updateData[guide]['newGuide']+' parent.')

    def parentRetainGuides():
        if len(guidesToReParentDict) > 0:
            for retainGuide in guidesToReParentDict:
                hasParent = guidesToReParentDict[retainGuide]
                if hasParent != None:
                    newParentFinal = retrieveNewParent(hasParent)
                    try:
                        cmds.parent(retainGuide, newParentFinal)
                    except:
                        print('It was not possible to parent '+retainGuide)
    
    def sendTransformsToListEnd(elementList):
        toMoveList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
        for element in toMoveList:
            elementList.append(elementList.pop(elementList.index(element)))

    def copyAttrFromGuides(newGuide, oldGuideAttrDic):
        newGuideAttrList = listKeyUserAttr(newGuide)
        if 'translateX' in newGuideAttrList and 'rotateX' in newGuideAttrList:
            sendTransformsToListEnd(newGuideAttrList)
        # For each attribute in the new guide check if exists equivalent in the old one, and if its value is different, in that case
        # set the new guide attr value to the old one.
        for attr in newGuideAttrList:
            if attr in oldGuideAttrDic:
                currentValue = getAttrValue(newGuide, attr)
                if currentValue != oldGuideAttrDic[attr]:
                    setGuideAttributes(newGuide, attr, oldGuideAttrDic[attr])

    def setNewBaseGuidesTransAttr():
        for guide in updateData:
            onlyTransformDic = {}
            for attr in TRANSFORM_LIST:
                if attr in updateData[guide]['attributes']:
                    onlyTransformDic[attr] = updateData[guide]['attributes'][attr]
            copyAttrFromGuides(updateData[guide]['newGuide'], onlyTransformDic)
    
    def filterChildrenFromAnotherBase(childrenList, baseGuide):
        filteredList = []
        filterStr = baseGuide.split(':')[0]
        for children in childrenList:
            if filterStr in children:
                filteredList.append(children)
        return filteredList
    
    # Set all attributes from children with same BaseGuide to avoid double set
    def setChildrenGuides():
        for guide in updateData:
            newGuideChildrenList = listChildren(updateData[guide]['newGuide'])
            newGuideChildrenList = filterChildrenFromAnotherBase(newGuideChildrenList, updateData[guide]['newGuide'])
            oldGuideChildrenList = updateData[guide]['children'].keys()
            oldGuideChildrenList = filterChildrenFromAnotherBase(oldGuideChildrenList, guide)
            newGuideChildrenOnlyList = map(lambda name : name.split(':')[1], newGuideChildrenList)
            oldGuideChildrenOnlyList = map(lambda name : name.split(':')[1], oldGuideChildrenList)
            for i, newChild in enumerate(newGuideChildrenList):
                if newGuideChildrenOnlyList[i] in oldGuideChildrenOnlyList:
                    copyAttrFromGuides(newChild, updateData[guide]['children'][guide.split(':')[0]+':'+newGuideChildrenOnlyList[i]]['attributes'])
    
    def listNewAttr():
        for guide in updateData:
            oldGuideSet = set(updateData[guide]['attributes'])
            newGuideSet = set(listKeyUserAttr(updateData[guide]['newGuide']))
            newAttributesSet = newGuideSet - oldGuideSet
            if len(newAttributesSet) > 0:
                print('The guia '+guide+' has the following new attributes:')
                for attr in newAttributesSet:
                    print(attr)
    
    def setNewNonTransformAttr():
        nonTransformDic = {}
        for guide in updateData:
            for attr in updateData[guide]['attributes']:
                if attr not in TRANSFORM_LIST:
                    nonTransformDic[attr] = updateData[guide]['attributes'][attr]
            copyAttrFromGuides(updateData[guide]['newGuide'], nonTransformDic)
    
    if autoRig:
        # Dictionary that will hold data for update, whatever don't need update will not be saved
        updateData = {}
        currentDpArVersion = autoRigUI.dpARVersion
        # Receive the guides list from hook function
        guidesDictionary = autoRig.utils.hook()
        newGuidesInstanceList = []
        guidesToReParentDict = {}
        TRANSFORM_LIST = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
        # If there are guides on the dictionary go on.
        if len(guidesDictionary) > 0:
            # Only way sorted for now
            reloadAr()
            # Get all info nedeed and store in updateData dictionary
            getGuidesToUpdateData()
            # Rename guides to discard as *_OLD
            renameOldGuides()
            # Create the new base guides to replace the old ones
            createNewGuides()
            # Set all attributes except transforms, it's needed for parenting
            setNewNonTransformAttr()
            # Parent all new guides;
            parentNewGuides()
            # Set new base guides transform attrbutes
            setNewBaseGuidesTransAttr()
            # Set all children attributes
            setChildrenGuides()
            # After all new guides parented and set, reparent old ones that will be used.
            parentRetainGuides()
            # List and print new attributes from created guides for possible input
            listNewAttr()
        else:
            print('There is no guides on the scene')
    else:
        print('Start dpAutoRig and Run script again')

updateGuides()