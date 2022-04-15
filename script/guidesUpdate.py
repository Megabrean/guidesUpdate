# Mudar prints para warnings.
from maya import cmds

def reloadAr():
    global autoRigUI
    autoRigUI = autoRig.DP_AutoRig_UI()

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

    def setAttrValue(baseGuide, attr, value):
        try:
            return cmds.setAttr(baseGuide+'.'+attr, value)
        except:
            print('the attr '+attr+' from '+baseGuide+' could not be set.')
    
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
    def getGuidesData():

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

    def createNewGuides():
        for guide in updateData:
            guideType = autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].guideModuleName
            print(guideType)
            # create the new guide
            currentNewGuide = autoRigUI.initGuide("dp"+guideType, "Modules")
            # rename as it's predecessor
            guideName = updateData[guide]['attributes']['customName']
            currentNewGuide.editUserName(guideName)
            print(currentNewGuide.moduleGrp)

            # setAttr section, extract to function
            newGuideAttrList = keyUserAttrList(currentNewGuide.moduleGrp)
            print(newGuideAttrList)
            print(updateData[guide]['attributes'].keys())
            # if len(newGuideAttrList) != len(updateData[guide]['attributes'].keys()):
            #     print('guia nova tem novos atributos')
            # else:
            #     print('guia nova tem mesmo numero de attr')

            # for attr in newGuideAttrList:
            #     if attr in newGuideAttrList:
            #         setAttrValue(currentNewGuide.moduleGrp, attr, updateData[guide]['attributes'][attr])
            #     else:
            #         print('The attribute '+attr+' from guide '+guideName+' is not present in its past version')
                   

            

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


    def renameOldGuides():
        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)
        # print(instancedModulesStrList)
        for guide in updateData:
            # print(updateData[guide]['attributes']['moduleInstanceInfo'])
            # idxTochange = instancedModulesStrList.index(updateData[guide]['attributes']['moduleInstanceInfo'])
            # print(idxTochange)
            currentCustomName = updateData[guide]['attributes']['customName']
            # print(currentCustomName)
            autoRigUI.modulesToBeRiggedList[updateData[guide]['idx']].editUserName(currentCustomName+'_OLD')
    
    def showInfo():
        instancedModulesStrList = map(str, autoRigUI.modulesToBeRiggedList)
        print(instancedModulesStrList)
        print(autoRigUI.modulesToBeRiggedList)
    
    def setNewGuides():
        print('maybe not')
            
    if autoRig:
        # Dictionary that will hold data for update, whatever don't need update will not get here
        updateData = {}
        currentDpArVersion = autoRigUI.dpARVersion
        # Receive the guides list from hook function
        guidesDictionary = autoRig.utils.hook()
        # If there are guides on the dictionary go on.
        if len(guidesDictionary) > 0:
            # Unica forma encontrada por hora
            reloadAr()
            # Get all info nedeed and store in updateData dictionary
            getGuidesData()
            # showInfo()
            # Renomeia guias antigas para _old para poder exclui-las, talvez ja seja possivel pré excluir.. verificar aqui será delete old guides
            renameOldGuides()
            # Cria novas guias que serão as atualizadas, ainda faltará preencher atributos
            createNewGuides()
            # Depois das guias novas criadas, parentear primeiro, depois setar attr guide and children
            setNewGuides()
        else:
            print('Não há guias na cena')
    else:
        print('Start dpAutoRig and Run script again')

updateGuides();