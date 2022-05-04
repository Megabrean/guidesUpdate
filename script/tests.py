minhaLista = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']

dicPrincipal = {'translateX': 20, 'segments': 2, 'user_name': 'Head'}

def test():
    dicSecond = {}
    for key in dicPrincipal:
        if key not in minhaLista:
            dicSecond[key] = dicPrincipal[key]
    print(dicSecond, dicPrincipal)

test()

print(type('string'))
print(type(True))
print(type(12))