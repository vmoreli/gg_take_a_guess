#!/bin/bash

# Defina a variável do diretório base
BASE_DIR="GG's"
PROJECT_DIR="$BASE_DIR/gg_guess"

# Verifica se está no diretório correto
if [ ! -d "$BASE_DIR" ] || [ ! -d "$PROJECT_DIR" ]; then
  echo "Certifique-se de estar no diretório pai de '$BASE_DIR' e que '$PROJECT_DIR' existe."
  exit 1
fi

# 1. Criar e ativar o ambiente virtual
cd "$BASE_DIR"
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# 2. Instalar dependências
cd "$PROJECT_DIR"
pip install -r requirements.txt

# 3. Migrar o banco de dados
python manage.py migrate

# 4. Carregar os dados de exemplo
python manage.py loaddata fixtures/db.json

echo "O banco de dados foi populado com dados de exemplo. As credenciais de teste são:"
echo "| Nome de usuário | Senha          |"
echo "| --------------- | -------------- |"
echo "| teste1          | x%0Y6FM9oM3G   |"
echo "| teste2          | g5Ai58AR\"9yH   |"
echo "| teste3          | 2*k7FGtXd#g2   |"

# 5. Iniciar o servidor de desenvolvimento
python manage.py runserver

echo "O servidor está rodando e pode ser acessado em http://127.0.0.1:8000/gg/home/"