# from dpAutoRigSystem.Extras import dpSelectAllControls

# autoRig.rigInfo.UpdateRigInfo.updateRigInfoLists()
# myVar = dpSelectAllControls.SelectAllControls(autoRigUI, autoRigUI.langName, autoRigUI.langDic)

# mylist = [10,2,3]
# print(mylist[0])

class Carro():
    def __init__(eumesmo) -> None:
        eumesmo.velocidade = 0

    def acelerar(eumesmo):
        eumesmo.velocidade += 1
    

uno = Carro()
gol = Carro()

uno.acelerar()
print("Velocidade do Uno "+str(uno.velocidade))
print("Velocidade do Gol "+str(gol.velocidade))
