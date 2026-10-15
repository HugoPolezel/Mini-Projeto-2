# Anonimização de Dados com Python e LGPD

Projeto em Python que consulta registros de usuários em um banco de dados PostgreSQL, gera arquivos CSV com dados pessoais parcialmente anonimizados e registra o tempo de execução das funções responsáveis pela exportação.

## Funcionalidades

- Conexão com banco de dados PostgreSQL utilizando SQLAlchemy.
- Definição da estrutura da tabela `usuarios`.
- Anonimização parcial de nome, CPF, e-mail e telefone.
- Exportação dos registros anonimizados para arquivos CSV separados por ano de nascimento.
- Exportação de nome e CPF originais para o arquivo `todos.csv`.
- Medição do tempo de execução das funções de exportação, com registro em `tempo.log`.

## Tecnologias utilizadas

- Python
- SQLAlchemy
- PostgreSQL
- `psycopg2-binary`
- CSV

## Estrutura dos arquivos

```text
.
├── LGPD.py
├── decorator_tempo.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python instalado.
- Acesso a um servidor PostgreSQL compatível com a configuração do projeto.
- Dependências listadas em `requirements.txt`.

## Instalação

1. Clone ou baixe este repositório e entre na pasta do projeto.
2. (Opcional, mas recomendado) Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   No Windows:

   ```bash
   .venv\Scripts\activate
   ```

   No Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração do banco de dados

O arquivo `LGPD.py` contém a URL de conexão com o PostgreSQL diretamente no código. Antes de executar o projeto, confira se o servidor, a porta, o banco, o usuário e a senha estão corretos e se você tem autorização para acessar esse banco.

Por segurança, não publique credenciais reais no repositório. Em uma versão de produção, prefira carregar os dados de conexão por variáveis de ambiente.

O script declara a tabela `usuarios` com os campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador do usuário |
| `nome` | Nome |
| `cpf` | CPF |
| `email` | E-mail |
| `telefone` | Telefone |
| `data_nascimento` | Data de nascimento |
| `created_on` | Data e hora de criação |
| `updated_on` | Data e hora da última atualização |

O comando `metadata.create_all(engine)` cria a tabela caso ela ainda não exista; ele não insere registros de exemplo.

## Como executar

Na pasta do projeto, execute:

```bash
python LGPD.py
```

O programa consulta os registros da tabela `usuarios`, aplica a anonimização aos dados usados nos arquivos anuais e gera os arquivos CSV. Também imprime no terminal o primeiro registro anonimizado, caso existam registros no resultado da consulta.

## Regras de anonimização

- **Nome:** substitui por asteriscos as letras do primeiro nome, mantendo sua inicial e os demais nomes.
- **CPF:** mantém os três primeiros caracteres e substitui o restante por asteriscos.
- **E-mail:** mantém a primeira letra do usuário e o domínio, substituindo por asteriscos o restante do usuário.
- **Telefone:** mantém apenas os quatro últimos caracteres.
- **Outros campos:** o identificador, a data de nascimento e as datas de criação e atualização são mantidos nos arquivos anuais.

Essas funções fazem uma **mascaragem parcial** dos dados. Isso, por si só, não garante anonimização irreversível nem conformidade integral com a LGPD.

## Arquivos gerados

- **`AAAA.csv`** — um arquivo para cada ano de nascimento encontrado nos registros. Contém os campos do usuário, com nome, CPF, e-mail e telefone mascarados.
- **`todos.csv`** — contém as colunas `nome` e `cpf` com os valores originais consultados pelo programa.
- **`tempo.log`** — registra o tempo de execução das funções decoradas com `@medir_tempo`.

Os arquivos CSV usam ponto e vírgula (`;`) como separador e a codificação `utf-8-sig`.

> **Atenção:** `todos.csv` contém dados pessoais originais, sem mascaragem. Armazene-o com controle de acesso adequado e não o compartilhe publicamente. O projeto também precisa de autorização apropriada para consultar e exportar esses dados.

## Medição de tempo

O arquivo `decorator_tempo.py` define o decorador `medir_tempo`, que utiliza `time.perf_counter()` para medir a duração de uma função e grava o resultado em `tempo.log`. No código atual, ele é aplicado às funções `gerar_arquivos_por_ano` e `gerar_arquivo_todos`.

## Dependências

As bibliotecas externas são listadas em `requirements.txt`:

- `SQLAlchemy`
- `psycopg2-binary`

Os módulos `csv`, `time`, `logging`, `functools` e `datetime` fazem parte da biblioteca padrão do Python.

## Observações

- A consulta espera que a tabela `usuarios` contenha registros e que os campos tenham os formatos previstos pelo código.
- O script acessa `users[0]` para imprimir o primeiro registro; se a consulta não retornar usuários, essa linha causará um erro.
- A exportação para `todos.csv` preserva nome e CPF originais. Revise essa parte antes de usar o programa com dados reais.
- A implementação atual não configura a conexão por variáveis de ambiente nem inclui tratamento específico para falhas de conexão ou de escrita dos arquivos.

## Licença

Nenhuma licença foi especificada neste projeto.
