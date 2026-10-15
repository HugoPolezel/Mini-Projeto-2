import csv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import String, Date, DateTime, insert, text
from datetime import datetime
from decorator_tempo import medir_tempo

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2")
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)


def anonimizar_nome(nome):
    palavras = nome.split()
    primeiro_nome = palavras[0]
    primeira_letra = primeiro_nome[0]
    quantidade = len(primeiro_nome) - 1
    palavras[0] = primeira_letra + "*" * quantidade
    return " ".join(palavras)


def anonimizar_cpf(cpf):
    inicio = cpf[:3]
    return inicio + ".***.***-**"


def anonimizar_email(email):
    partes = email.split("@")
    usuario = partes[0]
    dominio = partes[1]
    quantidade = len(usuario) - 1
    return usuario[0] + "*" * quantidade + "@" + dominio


def anonimizar_telefone(telefone):
    return telefone[-4:]


def LGPD(row):
    id = row[0]
    nome = anonimizar_nome(row[1])
    cpf = anonimizar_cpf(row[2])
    email = anonimizar_email(row[3])
    telefone = anonimizar_telefone(row[4])
    data_nascimento = row[5]
    created_on = row[6]
    updated_on = row[7]
    return (id, nome, cpf, email, telefone, data_nascimento, created_on, updated_on)


@medir_tempo
def gerar_arquivos_por_ano(users):
    anos = []
    for registro in users:
        ano = registro[5].year
        if ano not in anos:
            anos.append(ano)

    for ano in anos:
        arquivo = open(str(ano) + ".csv", "w", newline="", encoding="utf-8-sig")
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["id", "nome", "cpf", "email", "telefone", "data_nascimento", "created_on", "updated_on"])
        for registro in users:
            if registro[5].year == ano:
                escritor.writerow(registro)
        arquivo.close()


@medir_tempo
def gerar_arquivo_todos(originais):
    arquivo = open("todos.csv", "w", newline="", encoding="utf-8-sig")
    escritor = csv.writer(arquivo, delimiter=";")
    escritor.writerow(["nome", "cpf"])
    for row in originais:
        escritor.writerow([row[1], row[2]])
    arquivo.close()


originais = []
users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios;"))
    for row in result:
        originais.append(tuple(row))
        row = LGPD(row)
        users.append(row)

print(users[0])

gerar_arquivos_por_ano(users)
gerar_arquivo_todos(originais)

print("Arquivos gerados. Tempos gravados em tempo.log.")