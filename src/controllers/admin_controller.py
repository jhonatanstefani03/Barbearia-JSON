from src.models.tabelas import Cliente,Barbeiro,Agendamento,Servico, session
from datetime import*


def login_admin():
    print('Informe o login e senha:\n')
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    if usuario != "admin" or senha != "1234":
        print("Usuário ou senha incorretos!")
        return

    print("✅ Login realizado com sucesso!")

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
        print('[9] Criar serviços')
        print('[0] sair do sistema')

        escolha =  input('digite a opção desejada: ')

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
            case '9':
                criar_servico()
            case '0':
                break
            case __:
                print('opção  invalida!')
            

#####################################################################

def cadastrar_cliente():
    while True:
        nome = input('Digite o nome do cliente: ').strip()
        if nome.replace(' ', '').isalpha():
            break
        print('Nome inválido! Use apenas letras e espaços.')

    while True:
        try:
            cpf = int(input('Digite o CPF do cliente (apenas números): ').strip())
            break
        except ValueError:
            print('CPF inválido! Digite apenas números.')

    while True:
        try:
            telefone = int(input('Digite o telefone do cliente (apenas números): ').strip())
            break
        except ValueError:
            print('Telefone inválido! Digite apenas números.')

    while True:
        email = input('Digite o email do cliente: ').strip()
        if "@" in email:
            break
        print('Email inválido! Deve conter "@".')
    
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
    cpf = input('digite o cpf do  cliente  que deseja remover: ').strip()

    cliente =session.query(Cliente).filter_by(cpf=cpf).first()
    try:
        if cliente:
            session.delete(cliente)
            session.commit()
            print(f'Cliente {cliente.nome} removido com  sucesso!')
        else:
            print('cliente nao encontrado')
    except Exception:
        print('algo deu errado!')

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
    if barbeiro:
        session.delete(barbeiro)
        session.commit()
        print(f'barbeiro {barbeiro.nome} deletado com sucesso!')
    else:
        print('barbeiro nao  encontrado ou  nao cadastrado!')



def agendar_cliente():
    from  src.controllers.agendamentos import gerar_horarios_disponiveis
    clientes =  session.query(Cliente).all()
    servicos = session.query(Servico).all()
    barbeiros = session.query(Barbeiro).all()
    
    #cliente
    print('\n Escolha o  cliente:')
    for c in clientes:
        print(f'{c.id} - {c.nome} - {c.cpf}')
    escolha_cliente = input('escolha o  cliente (numero)')
    cliente_escolhido = session.query(Cliente).filter_by(id=escolha_cliente).first()
    if not cliente_escolhido:
        print('❌ Serviço não encontrado.')
        return

    #serviços
    print("\n📋 Serviços disponíveis:")
    for s in servicos:
        print(f'{s.id} - {s.tipo_servico} | R${s.preco} | {s.duracao} min')

    escolha_servico = input('Escolha um serviço (número): ')
    servico_escolhido = session.query(Servico).filter_by(id=escolha_servico).first()

    if not servico_escolhido:
        print('❌ Serviço não encontrado.')
        return
    #barbeiros
    print("\n✂️ Barbeiros disponíveis:")
    for b in barbeiros:
        print(f'{b.id} - {b.nome}')

    escolha_barbeiro = input('Escolha um barbeiro (número): ')
    barbeiro_escolhido = session.query(Barbeiro).filter_by(id=escolha_barbeiro).first()

    if not barbeiro_escolhido:
        print('❌ Barbeiro não encontrado.')
        return

    try:
        data_str = input('Digite a data do agendamento (YYYY-MM-DD): ')
        data = datetime.strptime(data_str, '%Y-%m-%d').date()

        if data < date.today():
            print('❌ Não é possível agendar para uma data no passado.')
            return
    
    except ValueError:
        print('❌ Data inválida.')
        return

    # 🔍 Gerar horários disponíveis
    horarios_disponiveis = gerar_horarios_disponiveis(
        barbeiro_id=barbeiro_escolhido.id,
        data=data,
        duracao_servico=servico_escolhido.duracao
    )

    if not horarios_disponiveis:
        print('❌ Nenhum horário disponível para este dia.')
        return

    print("\n⏰ Horários disponíveis:")
    for idx, h in enumerate(horarios_disponiveis):
        print(f"[{idx + 1}] {h.strftime('%H:%M')}")

    escolha_hora = input('Escolha um horário (número): ')

    try:
        escolha_hora = int(escolha_hora) - 1
        hora_escolhida = horarios_disponiveis[escolha_hora]
    except (ValueError, IndexError):
        print('❌ Escolha inválida.')
        return

    # ✅ Registrar o agendamento
    novo_agendamento = Agendamento(
        cliente_id=cliente_escolhido.id,
        barbeiro_id=barbeiro_escolhido.id,
        servico_id=servico_escolhido.id,
        data_agendamento=data,
        hora_agendamento=hora_escolhida
    )

    session.add(novo_agendamento)
    session.commit()

    print('✅ Agendamento realizado com sucesso!')
    print(f'🗓️ {data} às ⏰ {hora_escolhida.strftime("%H:%M")} com {barbeiro_escolhido.nome} para {servico_escolhido.tipo_servico}')
    

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


def criar_servico():
    nome=input('qual tipo  de serviço: ')
    preco = float(input('digite o preço do  serviço Ex(39.90): '))
    duracao = int(input('digite o  tempo  do serviço em minutos: '))
    novo_servico = Servico(
    tipo_servico=nome,
    duracao=duracao,
    preco=preco)

    session.add(novo_servico)
    session.commit()
    print(f'Serviço-{nome} add com sucesso!')
    return