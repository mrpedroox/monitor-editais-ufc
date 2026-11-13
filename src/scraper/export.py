import json
from dataclasses import asdict
from pathlib import Path

from .models import Edital


def save_json(itens: list[Edital], caminho: str = "data/editais.json") -> Path:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps([asdict(i) for i in itens], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return destino