from agendamentos import agendamentos
from database.models.tabelas import session
from database.models.tabelas import Cliente,Servico,Barbeiro





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
            agendar_cliente()
        elif opcao == "2":
            print("📅 Em construção: Ver agendamentos")
        elif opcao == "3":
            print("✏️ Em construção: Editar dados")
        elif opcao == "0":
            print("👋 Saindo do menu do cliente...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

def agendar_cliente():
    servicos = session.query(Servico).all()
    for s in servicos:
        print(f'{s.id}-{s.tipo_servico} preço R${s.preco} Tempo: {s.duracao}min')
    
    escolha=input('escolha um serviço baseado no numero ')
    
    servico_escolhido = next((s for s in servicos if str(s.id) == escolha), None)
    
    if servico_escolhido:
        print(f'Você escolheu {servico_escolhido.id} - {servico_escolhido.tipo_servico}')
    else:
        print('Serviço não encontrado.')

def ver_agendamentos(cliente):
    agendamentos_do_cliente = session.query(Agendamento).filter_by(cliente_id=cliente.id).order_by(Agendamento.data_agendamento, Agendamento.hora_agendamento).all()

    if not agendamentos_do_cliente:
        print("📭 Você ainda não possui nenhum agendamento marcado.")
        return

    print("Aqui estão seus próximos agendamentos:")
    for agendamento in agendamentos_do_cliente:
        print(f" -Serviço:{agendamento.servico} Data: {agendamento.data_hora}")

def editar_dados(cliente):

    while True:
        print("\nQual informação você gostaria de editar?")
        print("[1] Nome")
        print("[2] e-mail")
        print("[3] cpf")
        print("[4] senha")
        print("[0] Voltar ao Menu anterior")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            novo_nome = input("Digite o novo nome: ")
            cliente.nome = novo_nome
            session.commit()
            print("Nome atualizado com sucesso!")
        elif opcao == "2":
            novo_email = input("Digite o novo email: ")
            cliente.email = novo_email
            session.commit()
            print("Email atualizado com sucesso!")
        elif opcao == "3":
            novo_cpf = input("Digite o novo cpf: ")
            cliente.cpf = novo_cpf
            session.commit()
            print("CPF atualizado com sucesso!")
        elif opcao == "4":
            novo_senha = input("Digite a nova senha: ")]
            cliente.senha = novo_senha
            session.commit()
            print("Senha atualizada com sucesso!")
        elif opcao == "0":
            print("Retornando ao menu do cliente..."]
            break
        else:
            print("Opção inválida!Tente novamente.")

    continuar = input("Deseja editar mais alguma coisa? [S/N]: ").lower()
    if continuar != "S":
    break
