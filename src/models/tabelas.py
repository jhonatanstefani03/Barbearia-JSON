from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,Float,ForeignKey,Date,Time
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine("mysql+pymysql://root:root@localhost:3306/barbearia")
Base= declarative_base()

class Cliente(Base):
    __tablename__='clientes'
    id=Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cpf=Column(String(11))
    telefone=Column(String(12))
    email=Column(String(50))

class Barbeiro(Base):
    __tablename__='barbeiros'
    id=Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cpf=Column(String(11))
    telefone=Column(String(12))
    email=Column(String(50))

class Servico(Base):
    __tablename__='serviços'
    id=Column(Integer, primary_key=True, autoincrement=True)
    tipo_servico=Column(String(20))
    duracao=Column(Integer,nullable=False)
    preco=Column(Float,nullable=False)





class Agendamento(Base):
    __tablename__='agendamentos'
    id=Column(Integer, primary_key=True, autoincrement=True)
    cliente_id=Column(Integer, ForeignKey('clientes.id'))
    barbeiro_id=Column(Integer, ForeignKey('barbeiros.id'))
    servico_id=Column(Integer, ForeignKey('serviços.id'))
    data_agendamento=Column(Date, nullable=False)
    hora_agendamento=Column(Time, nullable=False)

    cliente = relationship('Cliente')
    barbeiro = relationship('Barbeiro')
    servico = relationship('Servico')


Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()



# novo_cliente = Cliente(nome='teste',cpf='1',telefone='123456',email='1')
# session.add(novo_cliente)
# session.commit()

# novo_servico = Servico(
#         tipo_servico='Corte Cabelo',
#         duracao=40,
#         preco=45.90)

# session.add(novo_servico)
# session.commit()

