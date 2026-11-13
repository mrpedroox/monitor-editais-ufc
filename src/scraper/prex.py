from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from .models import Edital

FONTE = "PREX"
SEPARADORES = " –—-:"


def classificar(texto: str) -> str:
    t = texto.lower()
    if t.startswith("aditivo"):
        return "aditivo"
    if t.startswith("resultado"):
        return "resultado"
    return "edital"


def _texto(el: Tag) -> str:
    """Texto do elemento com espaços normalizados."""
    return " ".join(el.get_text(" ", strip=True).split())


def _descricao(container: Tag, a: Tag) -> str:
    """O que vem depois do título do link, sem o traço separador."""
    titulo, texto = _texto(a), _texto(container)
    if texto.startswith(titulo):
        return texto[len(titulo):].strip(SEPARADORES)
    return ""


def _eh_marcador_ano(el: Tag) -> bool:
    estilo = (el.get("style") or "").lower()
    return el.name == "div" and "yellow" in estilo and el.get_text(strip=True).isdigit()


def _montar_item(container: Tag, a: Tag, base_url: str, ano, tipo: str, pai) -> Edital:
    return Edital(
        fonte=FONTE,
        ano=ano,
        tipo=tipo,
        titulo=_texto(a),
        descricao=_descricao(container, a),
        link=urljoin(base_url, a["href"]),
        edital_pai=pai.titulo if pai else None,
    )


def parse_prex(html: str, base_url: str) -> list[Edital]:
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("article.article")
    if article is None:
        return []

    itens, ano, ultimo_edital = [], None, None

    for el in article.find_all(recursive=False):
        if _eh_marcador_ano(el):
            ano = int(el.get_text(strip=True))

        elif el.name == "p":
            a = el.find("a", href=True)
            if a is None:  # <p>&nbsp;</p>
                continue
            tipo = classificar(_texto(a))
            # item solto: a posição na página não garante a que edital pertence
            item = _montar_item(el, a, base_url, ano, tipo, None)
            itens.append(item)
            if tipo == "edital":
                ultimo_edital = item

        elif el.name == "ul":
            for li in el.find_all("li", recursive=False):
                a = li.find("a", href=True)
                if a is None:
                    continue
                tipo = "resultado" if classificar(_texto(a)) == "resultado" else "aditivo"
                itens.append(_montar_item(li, a, base_url, ano, tipo, ultimo_edital))

    return itens