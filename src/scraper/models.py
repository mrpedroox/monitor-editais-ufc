from dataclasses import dataclass


@dataclass
class Edital:
    fonte: str
    ano: int | None
    tipo: str          # "edital" | "aditivo" | "resultado"
    titulo: str
    descricao: str
    link: str
    edital_pai: str | None = None   # título do edital a que o aditivo pertence