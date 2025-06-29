from database.models.tabelas import Cliente,Barbeiro,Agendamento, session


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
        print('[8] Atendimentos do dia')
        print('[0] sair do sistema')

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
            case '8':
                agendamento_dia()
            case '0':
                break
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
    cpf = input('qual cpf do cliente que deseja remover? ')
    data=  input('qual da data? ')
    cliente = session.query(Cliente).filter_by(cpf=cpf).first()
    if cliente:
        agendamento= session.query(Agendamento).filter_by(cliente_id=cliente.id, data_agendamento=data).first()

        if agendamento:
            session.delete(agendamento)
            session.commit()
            print(f'agendamento  de {cliente.id} do dia{data} removido com  sucesso!')
    else:
        print('agendamento nao encontrado')


def agendamento_realizados():
    agendamentos =  session.query(Agendamento).all()
    for i, ag in enumerate(agendamentos, start=1):
        print(f'{i}-{ag.cliente.nome}|barbeiro:{ag.barbeiro.nome} data:{ag.data_agendamento}|{ag.hora_agendamento}')
    print(f'total  de agendamentos ={len(agendamentos)}')


def agendamento_dia():
    data = input(' digite a data dos agendamento (YYYY-MM-DD): ')
    agendamentos = session.query(Agendamento).filter_by(data_agendamento=data).all()
    
    if agendamentos:
        for i, ag in enumerate(agendamentos, start=1):
            print(f"{i}) Cliente: {ag.cliente.nome} | Barbeiro: {ag.barbeiro.nome} | Serviço: {ag.servico.tipo_servico} | Hora: {ag.hora_agendamento}")
        print(f'total do  dia: {len(agendamentos)}')
    else:
        print('Nenhum agendamento encontrado para essa data.')