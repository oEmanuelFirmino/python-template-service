# FastAPI Template

📦 Template genérico de API com **FastAPI**, **Pydantic Settings** e suporte cross-platform para setup automático.

Este template oferece uma **estrutura inicial completa** para projetos Python com FastAPI, incluindo:

- Configurações via `.env`
- Endpoints básicos (`/` e `/health`)
- Middleware CORS configurável
- Scripts para setup e execução em **Windows, Linux e macOS**
- Estrutura pronta para expansão (routers, serviços, core)

---

## 🔹 Estrutura do projeto

```
fastapi-template/
├── api # Camada de roteadores e dependências
│   ├── __init__.py
│   ├── container.py # Configuração de dependências
│   ├── dependencies.py # Funções de dependência
│   ├── health_router.py # Roteador para /health
│   └── root_router.py # Roteador para /
├── core # Lógica central, utilitários e configurações
│   ├── decorators # Decoradores reutilizáveis
│   │   ├── cache.py # Decorador de cache simples
│   │   ├── log_execution.py # Decorador para logar execução de funções
│   │   ├── measure_memory.py # Decorador para medir uso de memória
│   │   ├── rate_limit.py # Decorador para limitar taxa de chamadas
│   │   ├── retry.py  # Decorador para retry automático
│   │   ├── singleton.py  # Decorador para singleton
│   │   ├── timeout.py  # Decorador para timeout de funções
│   │   └── validate_dto.py # Decorador para validar DTOs com Pydantic
│   ├── __init__.py
│   ├── logger.py # Configuração de logging
│   └── settings.py # Configurações do app com Pydantic Settings
├── domain  # Lógica de negócio, modelos e repositórios
│   ├── models # Modelos de domínio
│   ├── repositories  # Repositórios para acesso a dados
│   │   └── base.py # Repositório base com operações CRUD genéricas
│   ├── services # Serviços de negócio
│   │   └── base.py # Serviço base com lógica comum
│   └── __init__.py
├── infrastructure # Implementações de infraestrutura (banco, cache, etc)
│   └── __init__.py
├── interfaces #  Interfaces de comunicação (HTTP, gRPC, etc)
│   ├── http # Implementação de interface HTTP com FastAPI
│   │   ├── decorators # Decoradores específicos para rotas HTTP
│   │   │   ├── error_handler.py # Decorador para tratamento de erros em rotas
│   │   │   └── inject.py # Decorador para injeção de dependências em rotas
│   │   ├── errors.py # Definição de erros HTTP personalizados
│   │   ├── http_status.py # Códigos de status HTTP personalizados
│   │   └── reponse.py # Modelos de resposta HTTP personalizados
│   └── __init__.py
├── modules # Módulos específicos do domínio (ex: usuários, produtos, etc)
│   └── __init__.py
├── resources # Recursos estáticos (ex: arquivos de configuração, templates, etc)
│   └── __init__.py
├── tests # Testes unitários e de integração
│   └── __init__.py
├── utils # Utilitários genéricos e scripts de conversão
│   ├── json # Utilitários para manipulação de JSON
│   │   └── json_to_jsonl.py # Script para converter JSON para JSONL
│   └── __init__.py
├── __init__.py
└── main.py
```

## 🔹 Variáveis de ambiente (`.env`)

Exemplo mínimo:

```env
# ================================
# 📌 Identidade da aplicação
# ================================
APP_NAME="FastAPI Template"
DESCRIPTION="Template para APIs python com FastAPI"
ENVIRONMENT=development   # development | production | testing

# ================================
# ⚙️ Configurações do servidor
# ================================
HOST=0.0.0.0
PORT=8000
DEBUG=False

# ================================
# 🌍 CORS
# ================================
ALLOWED_ORIGINS=["*"]
ALLOWED_CREDENTIALS=True
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
```

> O `Pydantic Settings` mapeia automaticamente essas variáveis para `app.core.settings.Settings`.

---

## 🔹 Scripts de setup

**Linux/macOS**

```bash
./setup.sh
```

- Cria `.venv` se não existir
- Ativa .venv
- Atualiza pip
- Instala dependências
- Instruções para rodar `uvicorn` no final

**Windows PowerShell**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

**Windows CMD**

```cmd
setup.bat
```

**Rodar aplicação**

```bash
uvicorn app.main:app --reload
```

---

## 🔹 Endpoints básicos

| Endpoint | Método |                                              Descrição |
| :------- | :----: | -----------------------------------------------------: |
| /        |  GET   | Retorna informações do app e servidor {`RootResponse`} |
| /health  |  GET   |                 Health check da API {`HealthResponse`} |

**Modelos de resposta**

```json
// RootResponse
{
  "application": {
    "name": "FastAPI Template",
    "description": "Template genérico de API",
    "environment": "development"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false
  }
}

// HealthResponse
{
  "status": "ok",
  "message": "O serviço está funcionando corretamente!"
}
```

---

## 🔹 Dependências principais

- FastAPI
- Uvicorn
- Pydantic Settings
- Python >= 3.12

---

## 🔹 Dependências principais

- `.venv` isolado do sistema
- Configuração CORS pronta para uso
- Separação clara entre core, routers, services
- Script cross-plataform para setup rápido
- Preparado para expansão modular
