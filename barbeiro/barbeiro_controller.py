
from database.models.tabelas import session
from database.models.tabelas import Barbeiro 



def login_barbeiro():
    cpf=input('digite o cpf: ')
    email= input('digite o email: ')
    
    barbeiro = session.query(Barbeiro).filter_by(cpf=cpf, email=email).first()

    if barbeiro:
        print(f"✅ Bem-vindo, {barbeiro.nome}!")
        menu_barbeiro(barbeiro)
        
    else:
        print("❌ CPF ou e-mail incorretos. Tente novamente.")
        return None


def menu_barbeiro(barbeiro):
     while True:
        print(f"\n--- MENU DO CLIENTE: {barbeiro.nome} ---")
        print("[1] Agendar serviço")
        print("[2] Ver agendamentos")
        print("[3] Remover Horarios")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print(" Em construção: Agendar serviço")
        elif opcao == "2":
            print(" Em construção: Ver agendamentos")
        elif opcao == "3":
            print(" Em construção: Remover Horarios")
        elif opcao == "0":
            print(" Saindo do menu do barbeiro...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
