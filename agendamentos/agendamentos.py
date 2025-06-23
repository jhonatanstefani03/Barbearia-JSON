from database.models.tabelas import Agendamento, Servico
from datetime import datetime, timedelta, time
from database.models import tabelas
from sqlalchemy.orm import  session
from cliente.cliente_controller import *

def gerar_horarios_disponiveis(barbeiro_id, data, duracao_servico):
    # Definir horário de trabalho
    hora_abertura = time(9, 0)   # 09:00
    hora_fechamento = time(18, 0) # 18:00

    # Lista de horários ocupados
    agendamentos = session.query(Agendamento).filter_by(barbeiro_id=barbeiro_id,data_agendamento=data).all()

    horarios_ocupados = []
    for ag in agendamentos:
        ag_inicio = datetime.combine(ag.data_agendamento, ag.hora_agendamento)
        servico_ag = session.query(Servico).filter_by(id=ag.servico_id).first()
        ag_fim = ag_inicio + timedelta(minutes=servico_ag.duracao)
        horarios_ocupados.append((ag_inicio, ag_fim))

    # Gerar todos os horários possíveis
    horarios_disponiveis = []
    hora_atual = datetime.combine(data, hora_abertura)
    hora_limite = datetime.combine(data, hora_fechamento)

    while hora_atual + timedelta(minutes=duracao_servico) <= hora_limite:
        hora_inicio = hora_atual
        hora_fim = hora_inicio + timedelta(minutes=duracao_servico)

        conflito = False
        for ocupado_inicio, ocupado_fim in horarios_ocupados:
            if (hora_inicio < ocupado_fim) and (hora_fim > ocupado_inicio):
                conflito = True
                break

        if not conflito:
            horarios_disponiveis.append(hora_inicio.time())

        hora_atual += timedelta(minutes=15)  # Incremento de 15 minutos (pode ajustar)

    return horarios_disponiveis
