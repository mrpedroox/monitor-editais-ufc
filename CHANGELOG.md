# Changelog

Registro do que foi implementado em cada etapa do projeto.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-br/1.1.0/).

## [Não lançado]

Próxima etapa: **Etapa 2 · `feat/deteccao-novos`** (SQLite e detecção de editais novos).
Também entra aqui a normalização de `n°` / `nº` nos títulos.

## [v0.1] · 2026-11-13 · Etapa 1 · `feat/scraper`

Lista os editais da PREX a partir do HTML da página, com parser testado offline.

### Decisões

- **Fonte inicial: PREX** (`https://prex.ufc.br/pt/novos-editais/editais/`). A **PROGRAD**
  entra depois, num mini-ciclo `feat/scraper-prograd` antes da Etapa 2. O `v0.1` cobre só a PREX.
- **HTML em vez de API REST:** `prex.ufc.br/wp-json/wp/v2/posts` retorna `401 rest_forbidden`.
  O conteúdo está no HTML bruto (confirmado com `curl` + `grep`), então `requests` + `BeautifulSoup` bastam.
- **Separar buscar de interpretar:** `fetch_html(url)` faz a rede; `parse_prex(html, base_url)` só
  recebe texto, e é ele que o teste exercita com fixture, sem internet.
- **Sem abstração prematura:** nada de classe base ou plugins com uma fonte só. Uma função de
  parse por fonte (`parse_prex`, depois `parse_prograd`) e uma fixture por fonte.
- **Modelo `Edital`:** `fonte`, `ano`, `tipo` (`edital` | `aditivo` | `resultado`), `titulo`,
  `descricao`, `link`, `edital_pai`. Não há data por item na página: só o ano, no marcador amarelo.
- **Parser como máquina de estados:** a página é uma sequência de irmãos soltos dentro do
  `article`, então `parse_prex` percorre os filhos em ordem guardando o ano atual e o último edital.
- **`edital_pai` só para itens dentro de `<ul>`:** itens soltos em `<p>` (aditivo e resultado)
  podem aparecer *antes* do edital a que pertencem (ex.: "Aditivo 01/2026" vem antes do Edital 02),
  então ficam com `edital_pai = None` em vez de guardar um dado possivelmente errado.
- **Tipo também dentro de `<ul>`:** há um "Resultado Final" num `<ul>` (edital 05/2025),
  então o tipo dos `<li>` passa por `classificar` em vez de ser sempre `aditivo`.

### Estrutura do HTML da PREX (para o parser)

- Tudo dentro de `article.article`, como irmãos soltos: `div` amarelo = ano, `p > a` = edital
  ou resultado, `ul > li > a` = aditivo do edital anterior.
- Parser percorre `find_all(recursive=False)` guardando o ano atual e o último edital visto.
- Casos de borda: título sem espaço (`nº04/2026`), formatos diferentes (`07/PREX/UFC/2025`),
  aditivo solto em `<p>`, "Resultado" sem nome do edital, "Resultado Final" dentro de `<ul>`,
  links do Google Drive e de páginas internas, `<em>` dentro da descrição,
  `<p>&nbsp;</p>` e `<h2></h2>` vazios.

### Adicionado

- `src/scraper/models.py`: dataclass `Edital`
- `src/scraper/prex.py`: `classificar` e `parse_prex(html, base_url)`, com links resolvidos por
  `urljoin` e descrição extraída do texto depois do título
- `src/scraper/fetch.py`: `fetch_html(url)` com timeout, User-Agent próprio e `raise_for_status()`
- `src/scraper/export.py`: `save_json` grava `data/editais.json` com acentos legíveis
- `src/scraper/__main__.py`: `python -m src.scraper` imprime os editais e salva o JSON
- `tests/fixtures/prex.html`: fixture reduzida (10 KB) com 2026 e 2025 completos e o início de 2024.
  Contagem esperada: **44 itens (22 editais, 18 aditivos, 4 resultados)**; 2026 tem 17 itens
- `tests/test_parser_prex.py`: contagem por tipo, "Resultado Final" dentro de `<ul>` com
  `edital_pai`, e título sem espaço com descrição e ano. Roda sem internet
- `tests/test_export.py`: garante acentos preservados e criação da pasta de saída

### Alterado

- Contagem da fixture corrigida de 19 aditivos / 3 resultados para **18 / 4**: o "Resultado Final"
  dentro de um `<ul>` havia sido contado como aditivo
- `src/scraper/fecth.py` renomeado para `fetch.py` (erro de digitação)

### Removido

- `tests/test_smoke.py`: teste de sanidade da Etapa 0, substituído pelos testes do parser

### Resultado da execução real

`python -m src.scraper`: **137 itens da PREX (105 editais, 28 aditivos, 4 resultados)**,
de 2016 a 2026. `pytest -q`: 4 testes passando.

### Limitações conhecidas

- Um link com texto "neste link" (2021) vira um item com título genérico.
- Grafia mista `n°` / `nº` nos títulos (2023); normalizar na Etapa 2.
- Um título de 2023 termina com vírgula (`Aditivo n° 02/2024,`), vinda do texto da página.
- Itens soltos em `<p>` (aditivo, resultado) ficam sem `edital_pai`.
- Só a PREX; a PROGRAD entra em `feat/scraper-prograd`.

### Critério de pronto

- Um comando imprime os editais da página e o teste do parser passa sem acessar a internet

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
- `tests/test_smoke.py`: teste de sanidade (removido na Etapa 1)
- `.github/workflows/ci.yml`: roda `ruff check .` e `pytest` em PRs e em
  pushes na `main`

### Critério de pronto

- CI verde no PR de `chore/setup`
