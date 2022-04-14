# Arquivo para iniciar a programação
# Mudar prints para warnings.

import maya.cmds as cmds
# import dpAutoRigSystem.dpAutoRig as autoRig
# reload(autoRig)
# autoRigUI = autoRig.DP_AutoRig_UI()

def updateGuides():
    
    # Remove objects different from transform and nurbscurbe from list.
    def filterNurbsCurveAndTransform(mayaObjList):
        returList = []
        for obj in mayaObjList:
            objType = cmds.objectType(obj)
            if objType == 'nurbsCurve' or objType == 'transform':
                returList.append(obj)
        return returList
    
    # Remove _Ant(Anotations) items from list of transforms
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
                print('marcar como guia a ser usada, ou seja nao sera atualizada')

    # RASCUNHO DUPLICA A GUIA NA ORIGEM FALTA PEGAR OS ANTIGOS ATRIBUTOS
    def duplicateGuides():
        for guide in guidesDictionary:
            guideType = guidesDictionary[guide]['guideModuleNamespace'][:guidesDictionary[guide]['guideModuleNamespace'].find('_')]
            print(guideType)
            autoRigUI.initGuide("dp"+guideType, "Modules")

    def renameGuides(guidesDictionary):
        # Verify if modules are loaded to memory
        if len(autoRigUI.modulesToBeRiggedList) == 0:
            print('Autorig recarregado')
            reload(autoRig)
        
        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)
        print(instancedModulesStrList)
        for guide in guidesDictionary:
            idxTochange = instancedModulesStrList.index(updateData[guide]['attributes']['moduleInstanceInfo'])
            currentCustomName = updateData[guide]['attributes']['customName']
            autoRigUI.modulesToBeRiggedList[idxTochange].editUserName(currentCustomName+'_OLD')
            


    if autoRig:
        # Dictionary that will hold data for update
        updateData = {}
        # How to check this on dpAr?
        currentDpArVersion = autoRigUI.dpARVersion
        # Receive the guides list from hook function
        guidesDictionary = autoRig.utils.hook()
        # If there are guides on the dictionary go on.
        if len(guidesDictionary) > 0:
            getGuidesData(guidesDictionary)
            renameGuides(guidesDictionary)
            # duplicateGuides()
        else:
            print('Não há guias na cena')
    else:
        print('Start dpAutoRig and Run script again')

updateGuides();