from datetime import datetime
import pytest
from src.controllers.admin_controller import agendamento_realizados
from src.models.tabelas import Barbeiro, Cliente, Agendamento, session

@pytest.fixture
def barbeiro():
    return Barbeiro(nome='Barbeiro',cpf='123456',telefone='123456',email='<EMAIL>')

@pytest.fixture
def  cliente():
    return Cliente(nome='Cliente',cpf='123456',email='<EMAIL>')

@pytest.fixture
def agendamento(cliente,barbeiro):
    return Agendamento(cliente_id=cliente.id, barbeiro_id=barbeiro.id, data_agendamento=datetime.now(), hora_agendamento=datetime.now())

def test_agendamento_realizados(agendamento):
    response = agendamento_realizados()
    agendamentos = session.query(Agendamento).all()
    assert response == f'total  de agendamentos ={len(agendamentos)}'

