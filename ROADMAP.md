# Roadmap · Monitor de Editais UFC

Plano de desenvolvimento por etapas. Cada etapa tem **uma branch**, **um conceito central** e um **critério de pronto**.

## Fluxo de trabalho

- `main`: sempre funcionando; só recebe merge via Pull Request
- `feat/<nome>`, `chore/<nome>`, `docs/<nome>`: uma branch por etapa, criada a partir da `main`
- Ao concluir: PR → merge → tag (`v0.1`, `v0.2`, ...) → marcar a etapa no README
- Commits no padrão Conventional Commits: `feat`, `fix`, `docs`, `test`, `chore`, `ci`
- Se uma etapa passar de ~5 commits, dividir em duas

---

## Etapa 0 · `chore/setup`

**Conceito:** estrutura de projeto, lint, testes, CI
**Objetivo:** base do repositório com lint e testes rodando no GitHub.

- `chore: inicializa repositório com estrutura de pastas`
- `docs: adiciona README com roadmap`
- `chore: configura ruff e pytest`
- `ci: adiciona workflow de lint e testes`

**Pronto quando:** o CI roda verde num PR vazio. · Tag `v0.0`

## Etapa 1 · `feat/scraper`

**Conceito:** HTTP, HTML, seletores CSS
**Objetivo:** listar os editais de uma página da UFC.

- `feat(scraper): coleta título, link e data da página de editais`
- `test(scraper): testa parser com HTML salvo como fixture`
- `feat(scraper): salva resultado em data/editais.json`

**Pronto quando:** um comando imprime os editais da página e o teste do parser passa sem acessar a internet. · Tag `v0.1`

## Etapa 2 · `feat/deteccao-novos`

**Conceito:** persistência e idempotência
**Objetivo:** saber o que é novo desde a última execução.

- `feat(storage): persiste editais em SQLite`
- `feat(scraper): detecta editais novos por hash do link`
- `test(storage): garante que rodar duas vezes não duplica`

**Pronto quando:** a segunda execução seguida retorna zero editais novos. · Tag `v0.2`

## Etapa 3 · `feat/ingestao-pdf`

**Conceito:** extração de texto, chunking, metadados
**Objetivo:** transformar PDFs em pedaços pesquisáveis.

- `feat(ingest): baixa PDFs dos editais`
- `feat(ingest): extrai texto por página com pymupdf`
- `feat(ingest): divide em chunks com metadados (edital, URL, página)`

**Pronto quando:** cada chunk sabe de qual edital, página e URL veio. · Tag `v0.3`

## Etapa 4 · `feat/indice-vetorial`

**Conceito:** embeddings e busca por similaridade
**Objetivo:** buscar os trechos relevantes para uma pergunta.

> Dica de aprendizado: faça uma primeira versão **sem LangChain** para entender o que o framework abstrai.

- `feat(rag): gera embeddings e indexa no Chroma`
- `feat(rag): implementa retriever com top-k`
- `feat(cli): script de busca para testar pelo terminal`

**Pronto quando:** uma pergunta no terminal retorna os trechos certos com metadados. · Tag `v0.4`

## Etapa 5 · `feat/rag-citacao`

**Conceito:** RAG, prompt e grounding
**Objetivo:** responder só com base nos documentos, citando a fonte.

- `feat(rag): cadeia LangChain com prompt que exige citação`
- `feat(rag): retorna resposta + URL + página`
- `test(rag): responde "não encontrei" quando não há contexto`

**Pronto quando:** toda resposta traz fonte e perguntas fora do escopo não são inventadas. · Tag `v0.5`

## Etapa 6 · `feat/bot-telegram`

**Conceito:** handlers, tokens e variáveis de ambiente
**Objetivo:** conversar com o sistema pelo Telegram.

- `feat(bot): comandos /start e /ajuda`
- `feat(bot): responde perguntas usando a cadeia RAG`
- `docs: documenta criação do bot e variáveis de ambiente`

**Pronto quando:** você pergunta no Telegram e recebe resposta com fonte. · Tag `v0.6`

## Etapa 7 · `feat/agendamento`

**Conceito:** cron, CI/CD e secrets
**Objetivo:** rodar sozinho e avisar sobre editais novos.

- `ci: workflow com schedule cron para rodar o scraper`
- `feat(notify): envia mensagem no Telegram quando há edital novo`
- `feat(ingest): reindexa apenas documentos novos`

**Decisões a tomar nesta etapa:**
- O GitHub Actions é efêmero e não mantém o bot ligado. Onde o bot roda? (seu PC, Render, Fly.io...)
- Onde o índice e o SQLite ficam guardados entre execuções? (artefato, commit, ou servidor do bot)

**Pronto quando:** um edital publicado gera aviso sem você fazer nada. · Tag `v0.7`

## Etapa 8 · `feat/avaliacao`

**Conceito:** avaliação de sistemas RAG
**Objetivo:** medir se o sistema realmente acerta.

- `test(eval): cria conjunto de 10 a 15 perguntas com resposta esperada`
- `feat(eval): script que mede se o retriever traz o trecho certo`
- `docs: registra resultados e limitações`

**Pronto quando:** existe um número (ex.: acerto do retriever em X de 15 perguntas) registrado no README. · Tag `v0.8`

## Etapa 9 · `docs/polimento`

**Objetivo:** deixar o projeto pronto para portfólio.

- `docs: diagrama de arquitetura e GIF de demonstração`
- `docs: seção "o que aprendi" e como rodar`
- `chore: release v1.0`

**Pronto quando:** alguém consegue clonar, rodar e entender o projeto só pelo README. · Tag `v1.0`

---

## Checklist de cada PR

- [ ] Testes passando e lint limpo
- [ ] README atualizado (etapa marcada, seção "o que aprendi" preenchida)
- [ ] Nenhum segredo ou PDF commitado (`.env`, `data/`)
- [ ] Mensagens de commit no padrão Conventional Commits
