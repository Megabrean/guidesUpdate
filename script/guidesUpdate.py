# Arquivo para iniciar a programação

#print("I'm here")

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

name_space = cmds.namespace( exists='FkLine__dpAR_1' )

print(name_space)

#guide = "*Guide_Base*"

#print(guide)
