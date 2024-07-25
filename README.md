# Pitaco - Um jogo de advinhação para amantes de geografia

## Informações gerais
Pitaco é um jogo desenvolvido em Django, no qual o objetivo do usuário é acertar um país aleatório a partir de uma série de dicas, que vão sendo desbloqueadas a medida que palpites errados são feitos. Quanto mais dicas necessárias para o acerto, menos pontos o usuário ganhará.

É necessário estar logado para jogar o jogo! O site contém um leaderboard geral que exibe o top 10 usuários com mais pontos.
A partir do momento em que um usuário acerta um país no jogo, esse país não aparecerá mais em suas futuras partidas.

Funções de gerenciamento de usuários: Cadastro, login, logout, mudança de senha, exclusão de conta.

As informações dos países são obtidas por meio da API RestCountries.

O jogo deve ser jogado em inglês.

## Instruções para executar

### Configuração e execução automática:

Execute o script setup.sh com:

```bash
./setup.sh
```

Se a execução for bem sucedida, o servidor estará rodando e poderá ser acessado em http://127.0.0.1:8000/gg/home/.

Isso populará o DB com três usuários de exemplo e que podem ser usados para testes, cujas credenciais são:

| Nome de usuário   |   Senha       |
| ---------------   | ------------- |
| teste1            | x%0Y6FM9oM3G  |
| teste2            | g5Ai58AR"9yH  |
| teste3            | 2*k7FGtXd#g2  |

Caso haja algum problema, o processo manual está descrito a seguir:

### Configuração e execução manual:

#### 1. Criar e Ativar o Ambiente Virtual

Na pasta GG's/ :

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

#### 2. Instalar dependências

Na pasta GG's/gg_guess :

```bash
pip install -r requirements.txt
```

#### 3. Migrar o banco de dados

```bash
python manage.py migrate
```

#### 4. Carregar os dados de exemplo

```bash
python manage.py loaddata fixtures/db.json
```

#### 5. Para executar o servidor de desenvolvimento

```bash
python manage.py runserver
```

Então, o servidor estará rodando e poderá ser acessado em http://127.0.0.1:8000/gg/home/.
