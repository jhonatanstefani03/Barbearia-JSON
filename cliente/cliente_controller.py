
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

