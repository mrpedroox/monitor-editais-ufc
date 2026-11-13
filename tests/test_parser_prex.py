from collections import Counter
from pathlib import Path

from src.scraper.prex import parse_prex

HTML = Path("tests/fixtures/prex.html").read_text(encoding="utf-8")
BASE = "https://prex.ufc.br"


def test_contagem():
    itens = parse_prex(HTML, BASE)
    assert len(itens) == 44
    assert Counter(i.tipo for i in itens) == {"edital": 22, "aditivo": 18, "resultado": 4}
    assert sum(1 for i in itens if i.ano == 2026) == 17


def test_resultado_final_dentro_de_ul():
    itens = parse_prex(HTML, BASE)
    final = next(i for i in itens if i.titulo == "Resultado Final")
    assert final.tipo == "resultado"
    assert final.edital_pai == "Edital nº 05/PREX/UFC/2025"


def test_descricao_e_titulo_sem_espaco():
    itens = parse_prex(HTML, BASE)
    ed4 = next(i for i in itens if i.titulo == "Edital nº04/2026/PREX")
    assert ed4.descricao.startswith("Eleição para representantes")
    assert ed4.ano == 2026