# Meu Middleware Mensagem (Mínimo Viável)

Instruções rápidas para rodar o projeto e os testes.

Requisitos: Python 3.9+

Como rodar a demo local (PowerShell):

1. Criar e ativar virtualenv (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Rodar o servidor demo (abre o broker e registra serviço):

```powershell
python -m src.app_demo.app_server
```

3. Em outra janela, rodar o cliente demo:

```powershell
python -m src.app_demo.app_client
```

4. Rodar testes:

```powershell
pytest -q
```

Notas:
- O broker é in-process e baseado em `asyncio` para facilitar avaliação local.
- Mensagens têm TTL (em milissegundos). Mensagens expiradas são descartadas pela fila.
