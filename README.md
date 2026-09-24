# Presentation Letter System

Sistema web para gerenciamento e geração de cartas de apresentação, desenvolvido com **FastAPI**, **SQLAlchemy**, **PostgreSQL** e frontend em **HTML, CSS e JavaScript puro**.

O sistema permite autenticação de usuários, controle de acesso por perfil, gerenciamento de lojas e promotores, importação de dados, geração de cartas de apresentação em PDF e consulta de relatórios.

---

## Visão geral

O projeto é dividido em duas partes principais:

- **Backend:** API REST desenvolvida com FastAPI.
- **Frontend:** aplicação web desenvolvida com HTML, CSS e JavaScript.

A comunicação entre frontend e backend é realizada através de requisições HTTP utilizando JSON.

O sistema possui autenticação baseada em **JWT (JSON Web Token)** e controle de acesso para usuários administradores.

---

## Principais funcionalidades

### Autenticação

- Login utilizando CPF e senha.
- Autenticação baseada em JWT.
- Controle de sessão do usuário.
- Validação de usuário ativo.
- Proteção dos endpoints da API.
- Controle de acesso administrativo.

### Gerenciamento de usuários

Administradores podem:

- Criar novos usuários.
- Definir se o usuário é administrador.
- Editar dados do usuário.
- Alterar senha.
- Desativar usuários.
- Reativar usuários.
- Consultar usuários cadastrados.

### Gerenciamento de promotores

O sistema permite trabalhar com informações de promotores utilizadas no processo de geração das cartas.

### Gerenciamento de lojas

Permite cadastrar e consultar informações relacionadas às lojas.

### Importação de dados

O backend possui estrutura para importação de dados utilizados pelo sistema.

### Geração de cartas

O sistema permite gerar cartas de apresentação utilizando os dados cadastrados.

As cartas podem ser geradas em formato PDF através do backend.

### Relatórios

O frontend possui uma área de relatórios para consulta das informações disponíveis no sistema.

---

# Arquitetura do sistema

A arquitetura simplificada do projeto pode ser representada da seguinte forma:

```text
+----------------------+
|      FRONTEND        |
|                      |
| HTML / CSS / JS      |
+----------+-----------+
           |
           | HTTP / JSON
           v
+----------------------+
|       FASTAPI        |
|       BACKEND        |
|                      |
| REST API             |
+----------+-----------+
           |
           +-------------------+
           |                   |
           v                   v
+----------------+    +----------------+
|  PostgreSQL    |    |  PDF Generator |
|                |    |                |
| Dados usuários |    | Cartas em PDF  |
| Lojas          |    +----------------+
| Promotores     |
+----------------+
```

---

# Fluxo de autenticação

O processo de login funciona da seguinte maneira:

```text
+-------------+
|   Usuário   |
+------+------+
       |
       | CPF + senha
       v
+-------------------+
| Frontend / Login  |
+---------+---------+
          |
          | POST /auth/login
          v
+-------------------+
|     FastAPI       |
|                   |
| Valida CPF        |
| Valida senha      |
| Verifica usuário  |
| Verifica status   |
+---------+---------+
          |
          | Credenciais válidas
          v
+-------------------+
|    JWT Token      |
+---------+---------+
          |
          | Token
          v
+-------------------+
|     Frontend      |
|                   |
| Armazena token    |
+---------+---------+
          |
          | Requisições autenticadas
          v
+-------------------+
|     API REST      |
+-------------------+
```

---

# Fluxo de autorização administrativa

Algumas operações são restritas aos administradores.

```text
+----------------+
| Usuário logado |
+-------+--------+
        |
        v
+---------------------+
| JWT válido?         |
+---------+-----------+
          |
       +--+--+
       |     |
      NÃO    SIM
       |     |
       v     v
    401   +------------------+
          | É administrador? |
          +--------+---------+
                   |
                +--+--+
                |     |
               NÃO    SIM
                |     |
                v     v
              403   Permite
                    operação
```

---

# Estrutura do projeto

A estrutura principal do projeto é:

```text
presentation-letter-system-v1/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── importers.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── pdf_generator.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   │
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── letters.py
│   │   │   ├── promoters.py
│   │   │   ├── stores.py
│   │   │   └── users.py
│   │   │
│   │   └── static/
│   │       └── letter_assets/
│   │           ├── carimbo_sb.jpeg
│   │           ├── logo_ever.png
│   │           └── logo_tirolez.jpg
│   │
│   ├── tests/
│   │   └── __init__.py
│   │
│   └── README.md
│
├── frontend/
│   │
│   ├── css/
│   │   └── styles.css
│   │
│   ├── js/
│   │   ├── admin-import.js
│   │   ├── admin-users.js
│   │   ├── api.js
│   │   ├── cartas.js
│   │   ├── home.js
│   │   ├── login.js
│   │   ├── perfil.js
│   │   └── relatorios.js
│   │
│   ├── admin-promoters.html
│   ├── admin-stores.html
│   ├── admin-users.html
│   ├── cartas.html
│   ├── index.html
│   ├── login.html
│   ├── perfil.html
│   └── relatorios.html
│
├── requirements.txt
└── .gitignore
```

---

# Backend

O backend foi desenvolvido utilizando **Python + FastAPI**.

## Principais componentes

### `main.py`

É o ponto de entrada da aplicação FastAPI.

Responsável pela inicialização da API e registro das rotas.

### `database.py`

Responsável pela configuração da conexão com o banco de dados através do SQLAlchemy.

### `models.py`

Contém os modelos utilizados pelo banco de dados.

### `schemas.py`

Define os schemas Pydantic utilizados para validação dos dados de entrada e saída da API.

### `crud.py`

Concentra operações de criação, consulta, atualização e exclusão de dados.

### `security.py`

Responsável pelos recursos relacionados à segurança, incluindo:

- Hash de senhas.
- Verificação de senhas.
- Criação de tokens JWT.
- Validação de tokens.

### `pdf_generator.py`

Responsável pela geração das cartas em formato PDF.

### `importers.py`

Contém funções relacionadas à importação de dados.

---

# Rotas da API

As principais áreas da API são:

```text
/auth
/users
/stores
/promoters
/letters
```

## Autenticação

```text
POST /auth/login
GET  /auth/me
```

O endpoint de login recebe CPF e senha e retorna um token JWT quando as credenciais são válidas.

---

## Usuários

```text
POST   /users/
GET    /users/
PATCH  /users/{user_id}
DELETE /users/{user_id}
```

As operações administrativas são protegidas por autenticação e autorização.

---

## Lojas

As rotas relacionadas às lojas ficam disponíveis através do módulo:

```text
/routes/stores.py
```

---

## Promotores

As rotas relacionadas aos promotores ficam disponíveis através do módulo:

```text
/routes/promoters.py
```

---

## Cartas

As operações relacionadas às cartas ficam disponíveis através do módulo:

```text
/routes/letters.py
```

---

# Banco de dados

O projeto utiliza banco de dados relacional através do SQLAlchemy.

A conexão é configurada através da variável de ambiente:

```text
DATABASE_URL
```

Por segurança, o arquivo `.env` **não deve ser versionado no GitHub**.

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=sua_chave_secreta
```

Nunca utilize credenciais reais no README ou no código-fonte versionado.

---

# Segurança

O sistema possui algumas medidas de segurança implementadas:

- Senhas armazenadas através de hash.
- Autenticação utilizando JWT.
- Proteção dos endpoints autenticados.
- Controle de acesso administrativo.
- Validação de CPF.
- Verificação de usuário ativo.
- Variáveis sensíveis armazenadas em `.env`.
- Arquivos sensíveis ignorados pelo Git.

O arquivo `.env` não deve ser enviado para o repositório.

---

# Requisitos

Para executar o projeto localmente, é necessário ter instalado:

- Python 3.13 ou compatível.
- Git.
- PostgreSQL.
- Visual Studio Code ou outro editor de código.
- Navegador web.

---

# Instalação

## 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entrar na pasta:

```bash
cd presentation-letter-system-v1
```

---

## 2. Criar ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ativar o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Após a ativação, o terminal deverá apresentar algo semelhante a:

```text
(.venv) PS C:\Users\Usuario\presentation-letter-system-v1>
```

---

## 3. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
pip install -r requirements.txt
```

---

# Configuração do ambiente

Dentro da pasta `backend`, criar um arquivo:

```text
backend/.env
```

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=uma_chave_secreta_forte
```

Os valores devem ser substituídos pelas configurações do ambiente local.

O arquivo `.env` está incluído no `.gitignore` e não deve ser enviado ao GitHub.

---

# Configuração do banco de dados

Crie um banco PostgreSQL para o projeto.

Exemplo:

```text
presentation_letter
```

Depois configure a conexão no arquivo:

```text
backend/.env
```

Exemplo:

```env
DATABASE_URL=postgresql://postgres:senha@localhost:5432/presentation_letter
SECRET_KEY=chave_secreta_para_desenvolvimento
```

---

# Executando o backend

Entre na pasta `backend`:

```powershell
cd backend
```

Com o ambiente virtual ativado, execute:

```powershell
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

---

# Documentação da API

O FastAPI disponibiliza automaticamente uma documentação interativa.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

Através do Swagger é possível visualizar e testar os endpoints da API.

---

# Executando o frontend

O frontend é composto por arquivos HTML, CSS e JavaScript.

Estrutura:

```text
frontend/
├── css/
├── js/
└── arquivos HTML
```

Durante o desenvolvimento, os arquivos podem ser executados através de um servidor HTTP local.

Uma opção simples é utilizar a extensão **Live Server** no Visual Studio Code.

Outra opção é utilizar o servidor HTTP do Python:

```powershell
cd frontend
python -m http.server 5500
```

Depois acessar:

```text
http://127.0.0.1:5500
```

---

# Fluxo completo para testar o sistema

Depois de configurar o banco, backend e frontend:

```text
+---------------------------+
| 1. Iniciar PostgreSQL     |
+-------------+-------------+
              |
              v
+---------------------------+
| 2. Ativar .venv           |
+-------------+-------------+
              |
              v
+---------------------------+
| 3. Iniciar FastAPI        |
|    porta 8000             |
+-------------+-------------+
              |
              v
+---------------------------+
| 4. Iniciar Frontend       |
|    porta 5500             |
+-------------+-------------+
              |
              v
+---------------------------+
| 5. Abrir sistema          |
|    no navegador           |
+-------------+-------------+
              |
              v
+---------------------------+
| 6. Fazer login            |
|    CPF + senha            |
+-------------+-------------+
              |
              v
+---------------------------+
| 7. Utilizar o sistema     |
+---------------------------+
```

---

# Criação do usuário administrador

O projeto possui um script utilizado durante a configuração local:

```text
backend/create_admin.py
```

Esse arquivo é utilizado para criação inicial de um usuário administrador durante a configuração do ambiente.

Por motivos de segurança, o arquivo está incluído no `.gitignore` e não faz parte do versionamento público do projeto.

Caso seja necessário configurar um ambiente de desenvolvimento a partir do repositório, o procedimento de criação do administrador deve ser realizado conforme a configuração local do projeto.

---

# Organização das responsabilidades

De forma simplificada:

```text
+-------------------+
|     Frontend      |
|                   |
| HTML / CSS / JS   |
+---------+---------+
          |
          | HTTP / JSON
          v
+-------------------+
|      FastAPI      |
|                   |
|      Backend      |
+---------+---------+
          |
          +-------------------+
          |                   |
          v                   v
+----------------+    +----------------+
|   SQLAlchemy   |    | PDF Generator  |
+-------+--------+    +-------+--------+
        |                     |
        v                     v
+---------------+      +--------------+
|  PostgreSQL   |      |  Carta PDF   |
+---------------+      +--------------+
```

---

# Fluxo de geração de cartas

O processo de geração de cartas pode ser representado da seguinte forma:

```text
+--------------------+
| Dados do sistema  |
+---------+----------+
          |
          v
+--------------------+
| Letters Route      |
| /letters           |
+---------+----------+
          |
          v
+--------------------+
| PDF Generator      |
+---------+----------+
          |
          v
+--------------------+
| Arquivo PDF        |
+--------------------+
```

---

# Desenvolvimento

Durante o desenvolvimento, recomenda-se executar o backend com:

```powershell
python -m uvicorn app.main:app --reload
```

O parâmetro `--reload` permite que o servidor seja reiniciado automaticamente quando houver alterações no código.

---

# Git e versionamento

O projeto possui um `.gitignore` configurado para evitar o versionamento de arquivos sensíveis ou desnecessários.

Entre eles:

```text
.venv/
.env
.env.*
__pycache__/
*.pyc
*.db
*.sqlite
*.sqlite3
.vscode/
.idea/
*.log
build/
dist/
*.egg-info/
backend/create_admin.py
```

Arquivos contendo credenciais, senhas ou chaves secretas nunca devem ser enviados ao repositório.

---

# Estrutura simplificada da aplicação

```text
                    +------------------+
                    |     USUÁRIO      |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |     FRONTEND     |
                    |                  |
                    | HTML / CSS / JS  |
                    +--------+---------+
                             |
                             | HTTP / JSON
                             v
                    +------------------+
                    |      FASTAPI     |
                    |      BACKEND     |
                    +--------+---------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
     +---------+        +---------+        +---------+
     |  Auth   |        |  Users  |        | Letters |
     +---------+        +---------+        +---------+
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                    +------------------+
                    |    SQLAlchemy    |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |    PostgreSQL    |
                    +------------------+
```

---

# Tecnologias utilizadas

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- JWT
- Passlib / bcrypt
- Uvicorn
- ReportLab
- OpenPyXL

## Frontend

- HTML5
- CSS3
- JavaScript

## Desenvolvimento

- Git
- GitHub
- Visual Studio Code
- Python Virtual Environment (`venv`)

---

# Status do projeto

Projeto em desenvolvimento.

A estrutura atual contempla:

- Autenticação de usuários.
- Login através de CPF e senha.
- Controle de acesso administrativo.
- Gerenciamento de usuários.
- Gerenciamento de lojas.
- Gerenciamento de promotores.
- Importação de dados.
- Geração de cartas em PDF.
- Relatórios.
- Frontend web.

---

# Observações

Este projeto foi desenvolvido inicialmente para execução em ambiente local e pode exigir ajustes de configuração para utilização em produção.

Antes de realizar um deploy em ambiente produtivo, recomenda-se revisar:

- Configuração de segurança.
- CORS.
- Chaves secretas.
- Configuração do banco de dados.
- HTTPS.
- Logs.
- Controle de permissões.
- Política de backup.
- Configuração de ambiente.
- Processo de criação do usuário administrador.

---

# Licença

Projeto desenvolvido para fins de desenvolvimento e utilização conforme as regras definidas pelo proprietário do projeto.

Copyright © 2026.
