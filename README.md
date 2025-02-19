# SEFI - Sistema de Envio e Fila de Impressão

O SEFI é um sistema web desenvolvido em Django para o projeto integrador (do 4º período) do curso de ADS no IFRN-PDF, feito para gerenciar solicitações de impressão. O sistema permite que professores enviem solicitações de impressão, que são processadas por coordenadores e entregues por bolsistas.

## 🚀 Funcionalidades

### Para Professores
- Envio de solicitações de impressão
- Acompanhamento do status das solicitações
- Edição e exclusão de solicitações pendentes
- Histórico de solicitações

### Para Bolsistas
- Visualização da fila de impressão
- Marcação de entrega de solicitações
- Histórico de entregas realizadas

### Para Coordenadores
- Gerenciamento completo de solicitações
- Alteração de status
- Visualização de estatísticas
- Gerenciamento de usuários

## 💻 Tecnologias

- Python
- Django
- PostgreSQL
- HTML/CSS
- JavaScript

## 📋 Pré-requisitos

- Python 3.x
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

## 🔧 Instalação

1. Clone o repositório
```bash
git clone https://github.com/llwkascarvalho/SEFI.git
cd SEFI
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
⚠️ Este projeto utiliza PostgreSQL como banco de dados. Certifique-se de ter o PostgreSQL instalado em sua máquina.

Download PostgreSQL:
- Windows: https://www.postgresql.org/download/windows/
- Linux: https://www.postgresql.org/download/linux/

Após instalar o PostgreSQL:
1. Crie um banco de dados para o projeto
2. Renomeie o arquivo .env.example para .env
3. Edite o arquivo .env com suas configurações:

# DJANGO_DEBUG=True
# DJANGO_SECRET_KEY=django_secret_key
# DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
# DATABASE_URL=psql://usuario:senha@localhost:5432/nome_do_banco

Certifique-se de substituir 'usuario', 'senha' e 'nome_do_banco' pelos valores que você configurou no PostgreSQL.
```

5. Execute as migrações
```bash
python manage.py migrate
```

6. Crie os grupos e usuários de teste
```bash
python manage.py create_groups
python manage.py create_users
```

7. Inicie o servidor
```bash
python manage.py runserver
```

## 👥 Usuários Padrão

### Coordenador (Admin)
- Username: admin
- Email: admin@example.com
- Senha: admin

### Professor
- Username: professor
- Email: professor@example.com
- Senha: testeProfessor123

### Bolsista
- Username: bolsista
- Email: bolsista@example.com
- Senha: testeBolsista123

## 📁 Estrutura do Projeto

### Apps
- **core**: Gerenciamento de usuários e funcionalidades principais
- **fila**: Gerenciamento da fila de solicitações
- **historico**: Registro de histórico de solicitações
- **solicitacao**: Gerenciamento de novas solicitações

## 🚧 Status do Projeto

### ✅ Funcionalidades Implementadas
- [x] Sistema de autenticação
- [x] Níveis de acesso (Bolsista, Professor, Administrador/Coordenador)
- [x] Sistema de permissões baseado em grupos
- [x] Upload de arquivos configurado
- [x] Formulário de solicitação de impressão
- [x] Sistema de status para acompanhamento de solicitações
- [x] Fila e histórico funcionais
- [x] Alteração do status para admin
- [x] Alterar/excluir solicitações pendentes
- [x] Dashboard funcional para todos os usuários
- [x] Sistema de filtros
- [x] Utilizar PostgreSQL como banco de dados

### ⏳ Funcionalidades Pendentes
- [ ] Sistema de notificações

## ✒️ Autores

* **Erisvaldo** - *Desenvolvimento* - [GitHub](https://github.com/ErisvaldoBalbino)
* **Lwkas** - *Desenvolvimento* - [GitHub](https://github.com/llwkascarvalho)

