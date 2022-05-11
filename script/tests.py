import maya.cmds as cmds

# # Make a new window
# #
# window = cmds.window( title="Long Name", iconName='Short Name', widthHeight=(200, 55) )
# cmds.columnLayout( adjustableColumn=True )
# cmds.button( label='Do Nothing' )
# cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
# cmds.setParent( '..' )
# cmds.showWindow( window )


cmds.window( width=150 )
cmds.columnLayout( adjustableColumn=True )
cmds.text( label='Default' )
cmds.text( label='Left', align='left' )
cmds.text( label='Centre', align='center' )
cmds.text( label='Right', align='right' )
cmds.showWindow()