# Arquivo para iniciar a programação

"""
ALGORITMO:
	verificar se tem guides do dpAR na scene aberta do Maya
		se sim
			3 - to do? (futuramente)
			lista as guias
			para cada guia listada
				1 - to do
				pegar os parâmetros da base guide
				guardar todos os transforms dos elementos da guide (children)
				renomear a guia como Old temporariamente
				renomear attributos de naming da guia como Old
				criar uma nova instância do módulo atual
				set todos os attributos igual da guia Old
				set todos os transforms dos elementos da guide nova igual aos elementos da Old (children)
			para cada guia listada
				get all parenting (guias filhas de quais guias pais)
				talvez juntar esses dados em um dicionário
			para cada guia listada
				remontar o parenteamento das guias novas igual aos das Olds
				2 - to do
			deletar a lista de guias Old
			4 - to do
		5 - to do
"""


import maya.cmds as cmds

# name_space = cmds.namespace( exists='FkLine__dpAR_1' )

# print(name_space)


# Testing dpUtils, hook function

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
# return hookDic
print (hookDic)