# Changelog

Registro do que foi implementado em cada etapa do projeto.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-br/1.1.0/).

## [Não lançado]

Próxima etapa: **Etapa 1 · `feat/scraper`** (coleta de editais da página da UFC).

## [v0.0] · 2026-11-13 · Etapa 0 · `chore/setup`

Base do repositório com lint e testes rodando no GitHub.

### Adicionado

- Estrutura de pastas: `src/scraper/`, `src/rag/`, `src/bot/`, `tests/`,
  `tests/fixtures/`, `data/` e `.github/workflows/`
- `.gitignore` (ignora `.venv/`, `.env`, `data/` e caches)
- `.env.example` com `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` e `LLM_API_KEY`
- `requirements.txt` com `requests`, `beautifulsoup4`, `pytest` e `ruff`
- `README.md` com arquitetura, stack e roadmap
- `ROADMAP.md` com as etapas 0 a 9, branches e critérios de pronto
- `pyproject.toml` com a configuração do ruff e do pytest
- `tests/test_smoke.py`: teste de sanidade (será removido na Etapa 1)
- `.github/workflows/ci.yml`: roda `ruff check .` e `pytest` em PRs e em
  pushes na `main`

### Critério de pronto

- CI verde no PR de `chore/setup`