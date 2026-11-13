import json

from src.scraper.export import save_json
from src.scraper.models import Edital


def test_save_json_preserva_acentos(tmp_path):
    itens = [Edital("PREX", 2026, "edital", "Edital nº 01/2026/PREX", "Seleção", "https://x.br/a.pdf")]
    destino = save_json(itens, str(tmp_path / "saida" / "editais.json"))

    texto = destino.read_text(encoding="utf-8")
    assert "nº" in texto and "Seleção" in texto  # sem \u00ba

    dados = json.loads(texto)
    assert dados[0]["titulo"] == "Edital nº 01/2026/PREX"
    assert dados[0]["edital_pai"] is None