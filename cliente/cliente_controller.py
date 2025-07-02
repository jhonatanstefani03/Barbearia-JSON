
from database.models.tabelas import session
from database.models.tabelas import Cliente,Servico,Barbeiro,Agendamento
from datetime import *
from  agendamentos.agendamentos import gerar_horarios_disponiveis





def login_cliente():
    cpf =input('digite o seu cpf: ')
    email= input('digite o seu email: ')
    

    cliente = session.query(Cliente).filter_by(cpf=cpf, email=email).first()

    if cliente:
        print(f"✅ Bem-vindo, {cliente.nome}!")
        menu_cliente(cliente)
        
    else:
        print("❌ CPF ou e-mail incorretos. Tente novamente.")
        return None


def menu_cliente(cliente):
    while True:
        print(f"\n--- MENU DO CLIENTE: {cliente.nome} ---")
        print("[1] Agendar serviço")
        print("[2] Ver agendamentos")
        print("[3] Editar dados")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            agendar_cliente(cliente)
        elif opcao == "2":
            print("📅 Em construção: Ver agendamentos")
        elif opcao == "3":
            print("✏️ Em construção: Editar dados")
        elif opcao == "0":
            print("👋 Saindo do menu do cliente...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

def agendar_cliente(cliente):
    servicos = session.query(Servico).all()
    barbeiros = session.query(Barbeiro).all()

    print("\n📋 Serviços disponíveis:")
    for s in servicos:
        print(f'{s.id} - {s.tipo_servico} | R${s.preco} | {s.duracao} min')

    escolha_servico = input('Escolha um serviço (número): ')
    servico_escolhido = session.query(Servico).filter_by(id=escolha_servico).first()

    if not servico_escolhido:
        print('❌ Serviço não encontrado.')
        return

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

        data_agendadas = session.query(Agendamento).filter_by(data_agendamento=data_str).all()
        if data_agendadas:
            print('Já possui agendamento para esta data!')
            return

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
        cliente_id=cliente.id,
        barbeiro_id=barbeiro_escolhido.id,
        servico_id=servico_escolhido.id,
        data_agendamento=data,
        hora_agendamento=hora_escolhida
    )

    session.add(novo_agendamento)
    session.commit()

    print('✅ Agendamento realizado com sucesso!')
    print(f'🗓️ {data} às ⏰ {hora_escolhida.strftime("%H:%M")} com {barbeiro_escolhido.nome} para {servico_escolhido.tipo_servico}')
    