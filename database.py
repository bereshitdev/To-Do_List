"""Neste arquivo podemos importar os modelos de Banco de Dados
e criar a conexao com o banco de dados"""


from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
''' endereco URL  para conexao com BD ,neste caso SQLite
    e armazena-lo'''

SQLALCHEMY_DATABASE = "sqlite:///./To-Do-List.db"  

''' criando a interacao com o o banco de dados (o Motor)'''

engine = create_engine(SQLALCHEMY_DATABASE,connect_args={"check_same_thread":False})


# criando uma sessao de controle do bando de dados e controle

session_local = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base declarativa para os modelos
Base = declarative_base()

# modelo de tabela de tarefas

class Task(Base):
    __tablename__ = "tasks"

    id = Column("id",Integer,primary_key=True ,index=True)
    title = Column("title",String(100),nullable=False)
    description = Column("description",String(200),nullable=True)
    completed = Column("completed",Boolean,default=False)

# criando as tabelas no BD
def create_tables():
    Base.metadata.create_all(bind=engine)


# Dependencias para obter a sessao de do BD e tratamentos de erros

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
