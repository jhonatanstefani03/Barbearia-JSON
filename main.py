from src.controllers.admin_controller import login_admin
from src.controllers.cliente_controller import login_cliente
from src.controllers.barbeiro_controller import login_barbeiro


def linha(tam=30):
    print('-' * tam)


def mensagem(txt):
    linha(len(txt) + 4)
    print(f'* {txt} *')
    linha(len(txt) + 4)

def menu_principal():
    while True:
        mensagem('Bem vido  a Barbearia JSON!')
        print('selecione  uma opção: ')
        linha()
        print('1- Cliente')
        print('2- Barbeiro')
        print('3- Admin')
        escolha=input('informe o numero correspondente: ')

        if escolha =='1':
            login_cliente()
        elif escolha =='2':
            login_barbeiro()
        elif escolha == '3':
            login_admin()

menu_principal()