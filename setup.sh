#!/bin/bash

# Defina o diretório do projeto
PROJECT_DIR="gg_guess"

# Verifica se o diretório do projeto existe
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Certifique-se de que a pasta '$PROJECT_DIR' existe no diretório atual."
  exit 1
fi

# Defina o diretório do ambiente virtual
VENV_DIR="$PROJECT_DIR/venv"

# 1. Criar e ativar o ambiente virtual
if [ ! -d "$VENV_DIR" ]; then
  echo "Criando o ambiente virtual..."
  python3 -m venv "$VENV_DIR"
fi

# Ativar o ambiente virtual
source "$VENV_DIR/bin/activate"

# 2. Instalar dependências
echo "Instalando dependências..."
pip install -r "$PROJECT_DIR/requirements.txt"

# 3. Migrar o banco de dados
echo "Migrando o banco de dados..."
python "$PROJECT_DIR/manage.py" migrate

# 4. Carregar os dados de exemplo
echo "Carregando os dados de exemplo..."
python "$PROJECT_DIR/manage.py" loaddata "$PROJECT_DIR/fixtures/db.json"

echo "O banco de dados foi populado com dados de exemplo. As credenciais de teste são:"
echo "| Nome de usuário | Senha          |"
echo "| --------------- | -------------- |"
echo "| teste1          | x%0Y6FM9oM3G   |"
echo "| teste2          | g5Ai58AR\"9yH   |"
echo "| teste3          | 2*k7FGtXd#g2   |"

# 5. Iniciar o servidor de desenvolvimento
echo "Iniciando o servidor de desenvolvimento..."
python "$PROJECT_DIR/manage.py" runserver

echo "O servidor está rodando e pode ser acessado em http://127.0.0.1:8000/gg/home/"

