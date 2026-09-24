Presentation Letter System v1

Sistema web para gerenciamento e emissão de cartas de apresentação, desenvolvido com uma API REST em FastAPI e uma interface web em HTML, CSS e JavaScript.

O sistema permite autenticação de usuários, controle de acesso administrativo, gerenciamento de usuários, cadastro/importação de dados, geração de cartas de apresentação em PDF e consulta de informações relacionadas a promotores e lojas.

📋 Visão geral

O projeto foi desenvolvido com uma arquitetura separando backend e frontend.

Backend

A API foi desenvolvida utilizando:

Python

FastAPI

SQLAlchemy

PostgreSQL

Pydantic

JWT para autenticação

bcrypt para armazenamento seguro de senhas

Uvicorn como servidor ASGI

ReportLab para geração de PDFs

Frontend

A interface utiliza:

HTML5

CSS3

JavaScript puro

Fetch API para comunicação com o backend

Não é utilizado um framework frontend, como React ou Vue.

🚀 Funcionalidades
🔐 Autenticação

O sistema possui autenticação baseada em JWT.

O login é realizado utilizando:

CPF

Senha

Após uma autenticação válida, a API retorna um token de acesso que é utilizado nas requisições protegidas.

O CPF é normalizado antes da consulta, permitindo que sejam utilizados formatos como:

123.456.789-00


ou:

12345678900

👤 Gerenciamento de usuários

Usuários administradores possuem acesso à área de gerenciamento de usuários.

É possível:

Criar usuários.

Definir nome completo.

Definir username.

Definir CPF.

Definir senha.

Definir se o usuário é administrador.

Editar informações do usuário.

Alterar senha.

Desativar usuários.

Reativar usuários.

O sistema também impede o cadastro de:

CPF duplicado.

Username duplicado.

CPF com quantidade inválida de dígitos.

Senhas não são armazenadas em texto puro. O sistema utiliza hash de senha.

👮 Controle de acesso

Existem dois níveis básicos de acesso:

Usuário comum

Pode utilizar as funcionalidades disponibilizadas para usuários autenticados.

Administrador

Além das funcionalidades comuns, possui acesso às áreas administrativas, incluindo gerenciamento de usuários e dados do sistema.

A autorização administrativa é validada no backend. Portanto, esconder um botão ou link no frontend não é considerado uma medida de segurança suficiente.

🏪 Gerenciamento de lojas

A API possui rotas para gerenciamento das informações relacionadas às lojas utilizadas pelo sistema.

👥 Gerenciamento de promotores

O sistema possui funcionalidades relacionadas ao cadastro e gerenciamento de promotores.

📄 Cartas de apresentação

O sistema permite trabalhar com cartas de apresentação associadas aos dados cadastrados.

A API possui uma camada específica para geração dos documentos em PDF.

Os arquivos utilizados na composição dos documentos ficam em:

backend/app/static/letter_assets/


Atualmente, essa pasta contém elementos gráficos utilizados na geração das cartas, como logotipos e carimbos.

📊 Relatórios

O frontend possui uma área destinada à consulta e apresentação de informações relacionadas aos dados utilizados pelo sistema.

🏗️ Estrutura do projeto
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

⚙️ Requisitos

Para executar o projeto localmente, é necessário ter instalado:

Python 3.11+ recomendado

Git

PostgreSQL

Navegador moderno

Também é recomendado utilizar um ambiente virtual Python.

🔧 Instalação
1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/presentation-letter-system-v1.git


Entre na pasta:

cd presentation-letter-system-v1

2. Criar o ambiente virtual

No Windows:

python -m venv .venv


Ative o ambiente virtual:

.\.venv\Scripts\Activate.ps1


Caso o PowerShell esteja bloqueando a execução de scripts, pode ser necessário ajustar a política de execução do usuário.

3. Instalar as dependências

Com o ambiente virtual ativado:

pip install -r requirements.txt

🗄️ Configuração do banco de dados

O backend utiliza uma variável de ambiente para definir a conexão com o banco.

Crie:

backend/.env


Exemplo:

DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=uma_chave_secreta

Importante

O arquivo .env não deve ser enviado para o GitHub.

Ele está incluído no .gitignore justamente para evitar que credenciais e chaves secretas sejam versionadas.

Para compartilhar a configuração com outros desenvolvedores, recomenda-se criar um arquivo:

backend/.env.example


contendo apenas a estrutura das variáveis, sem valores reais:

DATABASE_URL=
SECRET_KEY=

▶️ Executando o backend

Entre na pasta backend:

cd backend


Com o ambiente virtual ativado, execute:

python -m uvicorn app.main:app --reload


A API ficará disponível, por padrão, em:

http://127.0.0.1:8000

📚 Documentação da API

O FastAPI gera automaticamente a documentação interativa.

Swagger UI:

http://127.0.0.1:8000/docs


ReDoc:

http://127.0.0.1:8000/redoc


A documentação Swagger permite visualizar os endpoints e realizar testes diretamente pelo navegador.

🔑 Autenticação

O endpoint de login está disponível em:

POST /auth/login


O login utiliza o padrão OAuth2 Password Flow.

O campo username utilizado pelo formulário OAuth2 representa o CPF do usuário neste sistema.

Exemplo conceitual:

CPF: 12345678900
Senha: ********


Após uma autenticação válida, a API retorna:

{
  "access_token": "TOKEN",
  "token_type": "bearer"
}


O token deve ser enviado nas requisições protegidas utilizando:

Authorization: Bearer TOKEN

👤 Usuário autenticado

Para consultar o usuário atualmente autenticado:

GET /auth/me


Esse endpoint retorna os dados do usuário associados ao token.

👮 Endpoints administrativos

As operações administrativas exigem um usuário autenticado com is_admin = true.

Usuários

Criar usuário:

POST /users/


Listar usuários:

GET /users/


Atualizar usuário:

PATCH /users/{user_id}


Desativar usuário:

DELETE /users/{user_id}


A autorização administrativa é validada no backend através da dependência de controle de acesso.

🧪 Testando o sistema

Após iniciar a API:

python -m uvicorn app.main:app --reload


acesse:

http://127.0.0.1:8000/docs


A partir do Swagger é possível testar os endpoints da API.

Um fluxo básico de teste é:

Criar/configurar um usuário administrador.

Realizar login utilizando CPF e senha.

Obter o access_token.

Autorizar o Swagger utilizando o token.

Consultar /auth/me.

Testar os endpoints protegidos.

Criar um novo usuário.

Testar as operações administrativas.

Testar as funcionalidades relacionadas às cartas.

🖥️ Executando o frontend

O frontend é composto por arquivos estáticos HTML, CSS e JavaScript.

A API deve estar executando antes de utilizar as telas que dependem do backend.

A pasta:

frontend/


contém as páginas da aplicação.

Dependendo da configuração utilizada no ambiente de desenvolvimento, os arquivos podem ser servidos por um servidor HTTP local.

Por exemplo, a partir da pasta frontend:

python -m http.server 5500


Depois, acessar:

http://127.0.0.1:5500


Observação: a configuração de execução do frontend pode variar conforme a forma como o projeto estiver sendo utilizado localmente.

🔐 Segurança

Algumas decisões importantes de segurança implementadas no projeto:

Autenticação baseada em JWT.

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


também é mantido fora do repositório público através do .gitignore, pois pode conter lógica destinada à criação/configuração inicial de um administrador.

🔄 Fluxo geral da aplicação

De forma simplificada:

                    ┌──────────────────┐
                    │     Frontend     │
                    │ HTML/CSS/JS      │
                    └────────┬─────────┘
                             │
                             │ HTTP / JSON
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │      Backend     │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
          Autenticação    Regras de      Geração
          e autorização   negócio        de PDF
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    PostgreSQL    │
                    └──────────────────┘

🧩 Principais módulos do backend
main.py

Ponto de entrada da aplicação FastAPI e configuração das rotas principais.

database.py

Configuração da conexão e sessão com o banco de dados.

models.py

Modelos SQLAlchemy utilizados para representar as entidades persistidas no banco.

schemas.py

Schemas Pydantic utilizados para validação de dados de entrada e saída da API.

crud.py

Operações de criação, consulta, atualização e exclusão dos registros.

security.py

Funções relacionadas à segurança, incluindo geração/verificação de senhas e criação/validação de tokens.

pdf_generator.py

Responsável pela geração das cartas de apresentação em PDF.

importers.py

Funções relacionadas à importação de dados.

routes/auth.py

Endpoints relacionados à autenticação e identificação do usuário atual.

routes/users.py

Endpoints administrativos relacionados aos usuários.

routes/letters.py

Endpoints relacionados às cartas de apresentação.

routes/promoters.py

Endpoints relacionados aos promotores.

routes/stores.py

Endpoints relacionados às lojas.

🧑‍💻 Desenvolvimento

Durante o desenvolvimento, recomenda-se manter o backend executando com:

python -m uvicorn app.main:app --reload


O parâmetro --reload faz com que o servidor seja reiniciado automaticamente quando alterações no código forem detectadas.

📌 Git

Depois de realizar alterações no projeto:

git status


Adicionar alterações:

git add .


Criar um commit:

git commit -m "Descrição da alteração"


Enviar para o GitHub:

git push


Arquivos sensíveis, ambiente virtual, caches e arquivos locais de configuração não devem ser adicionados ao repositório.

⚠️ Observações

Este projeto está estruturado principalmente como uma aplicação para execução e desenvolvimento local.

Antes de utilizar o sistema em produção, recomenda-se revisar pelo menos:

Configuração de CORS.

Gerenciamento e rotação da SECRET_KEY.

HTTPS.

Política de expiração e renovação dos tokens.

Configuração de banco de dados.

Logs.

Tratamento de erros.

Backup do banco.

Gerenciamento de credenciais.

Configuração de servidor de produção.

Permissões de acesso.

Política de criação e recuperação de senhas.

Testes automatizados.

📄 Licença

Este projeto não possui uma licença de código aberto definida neste momento.

Caso o projeto seja posteriormente disponibilizado como software open source, recomenda-se adicionar uma licença apropriada ao repositório.