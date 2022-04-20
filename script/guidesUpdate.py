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
            else:
                try:
                    return cmds.setAttr(dpGuide+'.'+attr, value)
                except:
                    print('the attr '+attr+' from '+dpGuide+' could not be set.')
    
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

    def listChildren(baseGuide):
        childrenList = cmds.listRelatives(baseGuide, allDescendents=True, children=True, type='transform')
        childrenList = filterNotNurbsCurveAndTransform(childrenList)
        childrenList = filterAnotation(childrenList)
        return childrenList

    # Receive a dictionary with guides and searches for custom attributes and also keyable attributes
    def getGuidesToUpdateData():

        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)

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

                updateData[baseGuide]['idx'] = instancedModulesStrList.index(updateData[baseGuide]['attributes']['moduleInstanceInfo'])
                
                updateData[baseGuide]['children'] = {}
                updateData[baseGuide]['parent'] = getGuideParent(baseGuide)
                # print(updateData[baseGuide]['parent'])
                childrenList = listChildren(baseGuide)
                for child in childrenList:
                    updateData[baseGuide]['children'][child] = {'attributes': {}}
                    # print(child)
                    guideAttrList = keyUserAttrList(child)
                    for attribute in guideAttrList:
                        attributeValue = getAttrValue(child, attribute)
                        updateData[baseGuide]['children'][child]['attributes'][attribute] = attributeValue
                    # print(updateData[baseGuide]['children'][child]['attributes'])
                # print(childrenList)

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
            autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].editUserName(currentCustomName+'_OLD')
    
    def parentNewGuides():
        for guide in updateData:
            hasParent = updateData[guide]['parent']
            if hasParent != None:
                newParentBase = updateData[hasParent.split(':')[0]+":Guide_Base"]['newGuide']
                newParentFinal = newParentBase.split(':')[0]+':'+hasParent.split(':')[1]
                try:
                    cmds.parent(updateData[guide]['newGuide'], newParentFinal)
                except:
                    print('It was not possible to find '+updateData[guide]['newGuide']+' parent.')

    def copyAttrFromGuides(newGuide, oldGuideAttrDic):
        newGuideAttrList = keyUserAttrList(newGuide)
        # For each attribute in the new guide check if exists equivalent in the old one, and if is different, in that case
        # set the old value to the new one.
        for attr in newGuideAttrList:
            if attr in oldGuideAttrDic:
                currentValue = getAttrValue(newGuide, attr)
                if currentValue != oldGuideAttrDic[attr]:
                    setAttrValue(newGuide, attr, oldGuideAttrDic[attr])

    
    def setNewBaseGuides():
        for guide in updateData:
            copyAttrFromGuides(updateData[guide]['newGuide'], updateData[guide]['attributes'])
    
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
            # print(newGuideChildrenList, oldGuideChildrenList)
            newGuideChildrenOnlyList = map(lambda name : name.split(':')[1], newGuideChildrenList)
            oldGuideChildrenOnlyList = map(lambda name : name.split(':')[1], oldGuideChildrenList)
            for i, newChild in enumerate(newGuideChildrenList):
                if newGuideChildrenOnlyList[i] in oldGuideChildrenOnlyList:
                    # print(newChild, guide.split(':')[0]+':'+newGuideChildrenOnlyList[i])
                    copyAttrFromGuides(newChild, updateData[guide]['children'][guide.split(':')[0]+':'+newGuideChildrenOnlyList[i]]['attributes'])
            
    if autoRig:
        # Dictionary that will hold data for update, whatever don't need update will not get here
        updateData = {}
        currentDpArVersion = autoRigUI.dpARVersion
        # Receive the guides list from hook function
        guidesDictionary = autoRig.utils.hook()
        newGuidesInstanceList = []
        # If there are guides on the dictionary go on.
        if len(guidesDictionary) > 0:
            # Unica forma encontrada por hora
            reloadAr()
            # Get all info nedeed and store in updateData dictionary
            getGuidesToUpdateData()
            # Renomeia guias antigas para _old para poder exclui-las, talvez ja seja possivel pré excluir.. verificar aqui será delete old guides
            renameOldGuides()
            # Cria novas guias que serão as atualizadas, ainda faltará preencher atributos
            createNewGuides()
            # Depois das guias novas criadas, parentear primeiro.
            parentNewGuides()
            # Set new base guides attr
            setNewBaseGuides()
            # Set children attributes
            setChildrenGuides()
        else:
            print('Não há guias na cena')
    else:
        print('Start dpAutoRig and Run script again')

updateGuides()

# CORRIGIR SEGMENTOS DOS FKLINES E VERIFICAR SETS DOS LIMBS, NA VERDADE TODAS AS GUIAS
# VERIFICAR QUANDO A GUIA NÃO TEM USERNAME.. TRATAR