Presentation Letter System v1

Sistema web para gerenciamento e emissão de cartas de apresentação, desenvolvido com uma API REST em FastAPI e uma interface web em HTML, CSS e JavaScript.

O sistema possui autenticação de usuários, controle de acesso administrativo, gerenciamento de usuários, gerenciamento de lojas e promotores, geração de cartas em PDF e funcionalidades de consulta e relatórios.

📌 Visão geral

O projeto é dividido em duas partes principais:

Backend: API REST desenvolvida em Python com FastAPI.

Frontend: interface web desenvolvida com HTML, CSS e JavaScript.

A comunicação entre frontend e backend é realizada através de requisições HTTP utilizando JSON.

A autenticação utiliza JWT (JSON Web Token) e o acesso às funcionalidades administrativas é controlado no backend.

🚀 Funcionalidades
🔐 Autenticação

O sistema possui autenticação baseada em JWT.

O login é realizado utilizando:

CPF

Senha

O CPF é normalizado antes da consulta ao banco de dados, permitindo formatos como:

123.456.789-00


ou:

12345678900


Após o login, a API retorna um token de acesso que deve ser utilizado nas requisições protegidas.

👤 Gerenciamento de usuários

Usuários administradores possuem acesso à área administrativa para gerenciamento de usuários.

É possível:

Criar usuários.

Definir nome completo.

Definir username.

Definir CPF.

Definir senha.

Definir se o usuário é administrador.

Editar informações.

Alterar senha.

Desativar usuários.

Reativar usuários.

O sistema também realiza validações para evitar:

CPF duplicado.

Username duplicado.

CPF com quantidade inválida de dígitos.

As senhas não são armazenadas em texto puro.

👮 Controle de acesso

O sistema possui dois níveis básicos de acesso:

Usuário comum

Pode acessar as funcionalidades disponíveis para usuários autenticados.

Administrador

Possui acesso às funcionalidades administrativas, incluindo gerenciamento de usuários e dados do sistema.

A autorização administrativa é validada no backend, garantindo que a segurança não dependa apenas da interface do frontend.

🏪 Gerenciamento de lojas

A API possui endpoints para gerenciamento das informações relacionadas às lojas utilizadas pelo sistema.

👥 Gerenciamento de promotores

O sistema possui funcionalidades para cadastro e gerenciamento de promotores.

📄 Cartas de apresentação

O sistema permite criar e gerenciar cartas de apresentação utilizando os dados cadastrados na aplicação.

A geração dos documentos em PDF é realizada pelo backend.

Os elementos gráficos utilizados na composição dos documentos ficam em:

backend/app/static/letter_assets/


Atualmente, essa pasta contém arquivos como logotipos e carimbos utilizados na geração das cartas.

📊 Relatórios

O frontend possui uma área destinada à consulta e apresentação de informações relacionadas aos dados utilizados pelo sistema.

🏗️ Arquitetura

A arquitetura básica da aplicação pode ser representada da seguinte forma:

+-----------------------+
|       Frontend        |
|     HTML / CSS / JS   |
+-----------+-----------+
            |
            | HTTP / JSON
            v
+-----------------------+
|        FastAPI        |
|        Backend        |
+-----------+-----------+
            |
     +------+------+
     |             |
     v             v
+---------+   +-----------+
|  Auth   |   |  Regras   |
|  JWT    |   | de negócio|
+---------+   +-----------+
                   |
                   v
            +-------------+
            | PostgreSQL  |
            +-------------+

                   |
                   v

            +-------------+
            | PDF Reports |
            |   / Letters |
            +-------------+

📁 Estrutura do projeto
presentation-letter-system-v1/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── letters.py
│   │   │   ├── promoters.py
│   │   │   ├── stores.py
│   │   │   └── users.py
│   │   │
│   │   ├── static/
│   │   │   └── letter_assets/
│   │   │
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── importers.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── pdf_generator.py
│   │   ├── schemas.py
│   │   └── security.py
│   │
│   ├── tests/
│   ├── README.md
│   └── create_admin.py
│
├── frontend/
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
├── .gitignore
├── requirements.txt
└── README.md


Observação: backend/.env, .venv/, arquivos __pycache__ e backend/create_admin.py são mantidos fora do repositório através do .gitignore.

🛠️ Tecnologias utilizadas
Backend
Tecnologia	Utilização
Python	Linguagem principal
FastAPI	Framework da API REST
SQLAlchemy	ORM
PostgreSQL	Banco de dados
Pydantic	Validação e serialização de dados
JWT	Autenticação
bcrypt	Hash de senhas
Uvicorn	Servidor ASGI
ReportLab	Geração de PDF
Frontend
Tecnologia	Utilização
HTML5	Estrutura das páginas
CSS3	Estilização
JavaScript	Lógica e comunicação com a API
Fetch API	Comunicação HTTP com o backend
⚙️ Requisitos

Para executar o projeto localmente, recomenda-se:

Python 3.11 ou superior

PostgreSQL

Git

Navegador moderno

📥 Instalação
1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/presentation-letter-system-v1.git


Entrar na pasta:

cd presentation-letter-system-v1

2. Criar o ambiente virtual

No Windows PowerShell:

python -m venv .venv


Ativar o ambiente virtual:

.\.venv\Scripts\Activate.ps1


Após a ativação, o terminal deverá apresentar algo semelhante a:

(.venv) PS C:\...\presentation-letter-system-v1>

3. Instalar as dependências
pip install -r requirements.txt

🗄️ Configuração do banco de dados

O backend utiliza PostgreSQL.

É necessário criar um banco de dados para executar a aplicação.

Depois, crie o arquivo:

backend/.env


Exemplo:

DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=sua_chave_secreta

⚠️ Importante

O arquivo .env não deve ser enviado para o GitHub.

Ele contém informações sensíveis utilizadas pela aplicação.

Para compartilhar a estrutura da configuração com outros desenvolvedores, pode ser criado um arquivo:

backend/.env.example


com:

DATABASE_URL=
SECRET_KEY=


Sem inserir credenciais reais.

▶️ Executando o backend

Entre na pasta do backend:

cd backend


Com o ambiente virtual ativado, execute:

python -m uvicorn app.main:app --reload


Se tudo estiver correto, o servidor será iniciado em:

http://127.0.0.1:8000


A opção --reload faz com que o servidor seja reiniciado automaticamente quando alterações no código forem detectadas.

📚 Documentação da API

O FastAPI disponibiliza automaticamente uma documentação interativa.

Swagger UI

Acesse:

http://127.0.0.1:8000/docs

ReDoc

Também é possível acessar:

http://127.0.0.1:8000/redoc


O Swagger permite visualizar e testar os endpoints diretamente pelo navegador.

🔑 Autenticação

O endpoint de login é:

POST /auth/login


O sistema utiliza o padrão OAuth2 Password Flow.

Neste projeto, o campo username utilizado pelo OAuth2 representa o CPF do usuário.

Exemplo:

CPF: 12345678900
Senha: ********


Após uma autenticação bem-sucedida, a API retorna:

{
  "access_token": "TOKEN",
  "token_type": "bearer"
}


O token deve ser enviado nas requisições protegidas através do header:

Authorization: Bearer TOKEN

👤 Usuário autenticado

Para consultar os dados do usuário atualmente autenticado:

GET /auth/me


Esse endpoint utiliza o token enviado na requisição para identificar o usuário.

👮 Endpoints administrativos

As operações administrativas exigem autenticação e privilégios de administrador.

Usuários

Criar usuário:

POST /users/


Listar usuários:

GET /users/


Atualizar usuário:

PATCH /users/{user_id}


Desativar usuário:

DELETE /users/{user_id}


A autorização é realizada no backend.

🧪 Testando a API

Depois de iniciar o backend:

python -m uvicorn app.main:app --reload


acesse:

http://127.0.0.1:8000/docs


Um fluxo básico de testes é:

Configurar o banco de dados.

Configurar as variáveis de ambiente.

Criar/configurar um usuário administrador.

Executar a API.

Realizar login utilizando CPF e senha.

Obter o access_token.

Autorizar o Swagger.

Consultar /auth/me.

Testar os endpoints protegidos.

Criar e gerenciar usuários.

Testar as funcionalidades de lojas e promotores.

Testar a geração das cartas.

🖥️ Executando o frontend

O frontend é composto por arquivos HTML, CSS e JavaScript.

A API deve estar executando antes de utilizar as páginas que dependem do backend.

Para executar os arquivos estáticos localmente, entre na pasta:

cd frontend


Execute um servidor HTTP simples:

python -m http.server 5500


Depois acesse:

http://127.0.0.1:5500


A forma de servir o frontend pode ser alterada dependendo do ambiente de desenvolvimento ou infraestrutura utilizada.

🔐 Segurança

O projeto possui algumas medidas básicas de segurança:

Autenticação utilizando JWT.

Senhas armazenadas utilizando hash.

Validação de CPF.

Verificação de CPF duplicado.

Verificação de username duplicado.

Controle de usuários ativos/inativos.

Controle de acesso administrativo no backend.

Uso de variáveis de ambiente para informações sensíveis.

.env excluído do controle de versão.

Ambiente virtual excluído do Git.

Arquivos compilados do Python excluídos do Git.

O arquivo:

backend/create_admin.py


também é mantido fora do repositório através do .gitignore.

🧩 Principais módulos do backend
main.py

Ponto de entrada da aplicação FastAPI e configuração das rotas.

database.py

Configuração da conexão com o banco de dados e criação das sessões.

models.py

Modelos SQLAlchemy utilizados pela aplicação.

schemas.py

Schemas Pydantic utilizados para validação e serialização dos dados.

crud.py

Funções responsáveis pelas operações de criação, consulta, atualização e exclusão de registros.

security.py

Funções relacionadas à segurança, incluindo hash/verificação de senhas e tokens JWT.

pdf_generator.py

Responsável pela geração dos documentos PDF.

importers.py

Funções relacionadas à importação de dados.

routes/auth.py

Endpoints relacionados à autenticação e identificação do usuário.

routes/users.py

Endpoints relacionados ao gerenciamento administrativo de usuários.

routes/letters.py

Endpoints relacionados às cartas de apresentação.

routes/promoters.py

Endpoints relacionados aos promotores.

routes/stores.py

Endpoints relacionados às lojas.

🔄 Fluxo básico da aplicação
Usuário
   |
   v
Frontend
   |
   | HTTP / JSON
   v
FastAPI
   |
   +-------------------+
   |                   |
   v                   v
Autenticação       Regras de negócio
   |                   |
   |                   +--------+
   |                            |
   v                            v
JWT                       PostgreSQL
                                |
                                v
                         Dados da aplicação
                                |
                                v
                         Geração de PDF

🔄 Fluxo de autenticação
+---------+
| Usuário |
+----+----+
     |
     | CPF + senha
     v
+------------+
|  /auth/    |
|   login    |
+-----+------+
      |
      v
+-------------+
| PostgreSQL  |
|             |
| CPF         |
| senha hash  |
+------+------+ 
       |
       | credenciais válidas
       v
+-------------+
| JWT Token   |
+------+------+ 
       |
       v
+----------------+
| Frontend       |
| guarda token   |
+-------+--------+
        |
        | Authorization: Bearer
        v
+----------------+
| Endpoints      |
| protegidos     |
+----------------+

🔄 Fluxo administrativo
Administrador
      |
      v
    Login
      |
      v
   JWT Token
      |
      v
Endpoint administrativo
      |
      v
require_admin()
      |
      +------ Não administrador ------> 403 Forbidden
      |
      v
Administrador autorizado
      |
      v
Operação solicitada

🧑‍💻 Desenvolvimento

Durante o desenvolvimento, recomenda-se executar o backend com:

python -m uvicorn app.main:app --reload


Após realizar alterações:

git status


Adicionar os arquivos modificados:

git add .


Criar um commit:

git commit -m "Descrição da alteração"


Enviar para o GitHub:

git push

📌 Arquivos que não devem ser versionados

O projeto utiliza .gitignore para evitar o envio de arquivos locais e informações sensíveis.

Entre eles:

.venv/
.env
__pycache__/
*.pyc
*.db
*.sqlite
*.sqlite3
backend/create_admin.py


Antes de realizar um git push, recomenda-se verificar:

git status --short --ignored

⚠️ Considerações para produção

Este projeto está preparado principalmente para desenvolvimento e testes locais.

Antes de utilizar a aplicação em produção, recomenda-se revisar:

HTTPS.

Configuração de CORS.

Gerenciamento e rotação da SECRET_KEY.

Expiração e renovação dos tokens.

Configuração do PostgreSQL.

Backup do banco de dados.

Logs e monitoramento.

Tratamento de erros.

Gerenciamento de credenciais.

Política de recuperação de senha.

Permissões de acesso.

Testes automatizados.

Configuração de servidor ASGI para produção.

📄 Licença

Este projeto não possui uma licença de código aberto definida no momento.

Caso o projeto seja posteriormente disponibilizado como software open source, recomenda-se adicionar uma licença apropriada ao repositório.