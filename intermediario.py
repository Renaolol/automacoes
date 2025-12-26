#Blocos

def descobrir_primo(valor:int):
    primo = False
    for num in range(valor):
        print(f'O valor {valor} módulo por {num+1} resulta em {(valor)% (num+1)}')
        if (valor) & (num+1) == 0:
            print(f'Operação {(valor) // (num+1)}')
    return primo

print(descobrir_primo(5))