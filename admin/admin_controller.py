from database.models.tabelas import Cliente,Barbeiro, session


def login_admin():
    print("Login funcionando!")
    while True:
        print("\n--- MENU DO ADMIN  ---")
        print("[1] Cadastrar Cliente")
        print("[2] Cadastrar Barbeiro")
        print("[3] Remover Cliente")
        print("[4] Remover Barbeiro")
        print("[5] Agendar cliente")
        print("[6] Remover agendamento")
        print('[7] Atendimentos Realizados')

        escolha =  input('digite a opçãpo desejada: ')

        match escolha:

            case '1':
                cadastrar_cliente()
            case '2' :
                cadastrar_barbeiro()
            case '3':
                remover_cliente()
            case '4' :
                remover_barbeiro()
            case '5' :
                agendar_cliente()
            case '6':
                remover_agendamento()
            case '7':
                agendamento_realizados()
            case __:
                print('opçap  invalida!')
            

#####################################################################

def cadastrar_cliente():
    nome = input('digite o nome do cliente: ')
    cpf = input('digite o cpf do cliente: ')
    telefone =  input('digite o telefone: ')
    email= input('digite o email: ')
    
    cliente_existente =  session.query(Cliente).filter_by(cpf=cpf).first()
    if cliente_existente:
        print(f'Cliente ja cadastrado  com o cpf {cpf}. Cadastro nao realizado')
        return
    
    else:
        novo_cliente = Cliente(nome=nome,cpf=cpf,telefone=telefone,email=email)
        session.add(novo_cliente)
        session.commit()
        print(f'cadastro do cliente {novo_cliente.nome} realizado com sucesso!')
    

def remover_cliente():
    clientes =session.query(Cliente).all()
    for cliente in clientes:
        print(f'{cliente.nome} cpf:{cliente.cpf}')
    cpf = input('digite o cpf do  cliente  que deseja remover: ')

    cliente =session.query(Cliente).filter_by(cpf=cpf).first()
    
    if cliente:
        session.delete(cliente)
        session.commit()
        print(f'Cliente {cliente.nome} removido com  sucesso!')
    else:
        print('cliente nao encontrado')

def cadastrar_barbeiro():
    nome =input('digite o nome do Barbeiro: ')
    cpf = input('digite o  cpf : ')
    telefone = input('digite o  telefone: ')
    email =input('digite o  email : ')
    novo_barbeiro = Barbeiro(nome=nome,cpf=cpf,telefon=telefone,email=email)
    session.add(novo_barbeiro)
    session.commit()

def remover_barbeiro():
    cpf = input('digite o cpf  do barbeiro que deseja remover: ')
    barbeiro =  session.query(Barbeiro).filter_by(cpf=cpf).first()
    session.delete(barbeiro)
    session.commit()



def agendar_cliente():
    pass

def remover_agendamento():
    pass

def agendamento_realizados():
    pass