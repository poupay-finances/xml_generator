from Generator import gerador

import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    opcao = input("Deseja gerar dados de soja ou gado:")
    while (True):
        if opcao.lower() in ['soja', 'gado']:
            gerador(opcao)
            break
        else:
            print("Digite um opção valida")
            cls()


if __name__ == '__main__':
    menu()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
