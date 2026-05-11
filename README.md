# API-4DSM-RECEPTOR-DADOS

## 📋 Como Rodar

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd API-4DSM-RECEPTOR-DADOS
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# Configurações do MongoDB
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/?appName=API-4DSM
MONGO_DATABASE=sensor_data
MONGO_COLLECTION=leituras

# Configurações da API Receptor
PORT=5000
API_URL=http://localhost:5000/receptor

# Configurações do Simulador
TOTAL_VIRTUAL_SENSORS=5
MESSAGES_PER_BURST=3
DELAY_BETWEEN_BURSTS=10
DELAY_IN_BURST=0.5
```

---

## 📊 Funcionamento

A aplicação funciona da seguinte forma:

- **Endpoint HTTP:** O servidor Flask expõe uma rota `/receptor` preparada para receber requisições `POST`.
- **Processamento de JSON:** Recebe o payload do sensor (ESP32 ou Simulador) e valida a presença de campos obrigatórios (`uid` e `unixtime`).
- **Persistência Flexível:** Os dados são inseridos diretamente no MongoDB. Como o banco é NoSQL, o sistema aceita novos campos (`temperatura`, `umidade`, `CO2`, etc.) sem necessidade de alterar o código.
- **Simulação:** O script de simulação gera comportamentos de diferentes tipos de sensores (Pluviômetro, Solo, Qualidade do Ar) para testar a carga e a flexibilidade do banco.

---

## 🚀 Execução

Para rodar o sistema completo, execute o receptor e, em seguida, o simulador em terminais separados:

**Terminal 1 — Receptor:**

```bash
python src/app.py
```

**Terminal 2 — Simulador:**

```bash
python src/simulator.py
```

---

## 🧪 Executando Testes

Para rodar os testes unitários e garantir que a lógica de geração de dados e a API estão íntegras:

```powershell
$env:PYTHONPATH = "src"; python -m pytest -v
```
---
