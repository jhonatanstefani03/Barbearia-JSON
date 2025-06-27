from database.models.tabelas import session
from database.models.tabelas import Barbeiro
from cliente.cliente_controller import Cliente, Servico, Agendamento
from agendamentos.agendamentos import gerar_horarios_disponiveis
from datetime import datetime, date


def login_barbeiro():
    cpf = input('Digite o CPF: ')
    email = input('Digite o e-mail: ')

    barbeiro = session.query(Barbeiro).filter_by(cpf=cpf, email=email).first()

    if barbeiro:
        print(f"\n✅ Bem-vindo, {barbeiro.nome}!")
        menu_barbeiro(barbeiro)
    else:
        print("❌ CPF ou e-mail incorretos. Tente novamente.")
        return None


def menu_barbeiro(barbeiro):
    while True:
        print(f"\n--- MENU DO BARBEIRO: {barbeiro.nome} ---")
        print("[1] Agendar serviço para cliente")
        print("[2] Ver agendamentos")
        print("[3] Remover agendamento")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            agendar_para_cliente(barbeiro)
        elif opcao == "2":
            ver_agendamentos_barbeiro(barbeiro)
        elif opcao == "3":
            remover_agendamento_barbeiro(barbeiro)
        elif opcao == "0":
            print("👋 Saindo do menu do barbeiro...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")


def agendar_para_cliente(barbeiro):
    clientes = session.query(Cliente).all()
    servicos = session.query(Servico).all()

    print("\n👥 Clientes disponíveis:")
    for c in clientes:
        print(f"{c.id} - {c.nome}")
    id_cliente = input("Escolha o ID do cliente: ")
    cliente = session.query(Cliente).filter_by(id=id_cliente).first()

    if not cliente:
        print("❌ Cliente não encontrado.")
        return

    print("\n📋 Serviços disponíveis:")
    for s in servicos:
        print(f"{s.id} - {s.tipo_servico} | R${s.preco} | {s.duracao} min")
    id_servico = input("Escolha o ID do serviço: ")
    servico = session.query(Servico).filter_by(id=id_servico).first()

    if not servico:
        print("❌ Serviço não encontrado.")
        return

    try:
        data_str = input("Digite a data do agendamento (YYYY-MM-DD): ")
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        if data < date.today():
            print("❌ Data inválida (passada).")
            return
    except ValueError:
        print("❌ Formato de data inválido.")
        return

    horarios_disponiveis = gerar_horarios_disponiveis(
        barbeiro_id=barbeiro.id,
        data=data,
        duracao_servico=servico.duracao
    )

    if not horarios_disponiveis:
        print("❌ Nenhum horário disponível.")
        return

    print("\n⏰ Horários disponíveis:")
    for i, h in enumerate(horarios_disponiveis):
        print(f"[{i+1}] {h.strftime('%H:%M')}")
    try:
        escolha = int(input("Escolha um horário: ")) - 1
        hora_escolhida = horarios_disponiveis[escolha]
    except (IndexError, ValueError):
        print("❌ Escolha inválida.")
        return

    agendamento = Agendamento(
        cliente_id=cliente.id,
        barbeiro_id=barbeiro.id,
        servico_id=servico.id,
        data_agendamento=data,
        hora_agendamento=hora_escolhida
    )

    session.add(agendamento)
    session.commit()
    print("✅ Agendamento realizado com sucesso!")


def ver_agendamentos_barbeiro(barbeiro):
    agendamentos = session.query(Agendamento).filter_by(barbeiro_id=barbeiro.id).order_by(
        Agendamento.data_agendamento, Agendamento.hora_agendamento).all()

    if not agendamentos:
        print("📭 Nenhum agendamento encontrado.")
        return

    print(f"\n📅 Agendamentos de {barbeiro.nome}:")
    for ag in agendamentos:
        cliente = session.query(Cliente).filter_by(id=ag.cliente_id).first()
        servico = session.query(Servico).filter_by(id=ag.servico_id).first()
        print(f"🗓️ {ag.data_agendamento} às ⏰ {ag.hora_agendamento.strftime('%H:%M')} - Cliente: {cliente.nome} - Serviço: {servico.tipo_servico}")


def remover_agendamento_barbeiro(barbeiro):
    agendamentos = session.query(Agendamento).filter_by(barbeiro_id=barbeiro.id).all()

    if not agendamentos:
        print("📭 Nenhum agendamento para remover.")
        return

    print("\n🔴 Agendamentos:")
    for i, ag in enumerate(agendamentos):
        cliente = session.query(Cliente).filter_by(id=ag.cliente_id).first()
        servico = session.query(Servico).filter_by(id=ag.servico_id).first()
        print(f"[{i+1}] {ag.data_agendamento} {ag.hora_agendamento.strftime('%H:%M')} - Cliente: {cliente.nome} - Serviço: {servico.tipo_servico}")

    try:
        escolha = int(input("Escolha o número do agendamento para remover: ")) - 1
        agendamento_escolhido = agendamentos[escolha]
    except (IndexError, ValueError):
        print("❌ Escolha inválida.")
        return

    session.delete(agendamento_escolhido)
    session.commit()
    print("✅ Agendamento removido com sucesso.")

