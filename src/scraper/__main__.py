from collections import Counter

from .export import save_json
from .fetch import fetch_html
from .prex import parse_prex

URL_PREX = "https://prex.ufc.br/pt/novos-editais/editais/"


def main() -> None:
    html = fetch_html(URL_PREX)
    itens = parse_prex(html, URL_PREX)

    for item in itens:
        print(f"[{item.ano}] {item.tipo:<9} {item.titulo}")

    por_tipo = Counter(i.tipo for i in itens)
    print(f"\n{len(itens)} itens: {dict(por_tipo)}")

    destino = save_json(itens)
    print(f"Salvo em {destino}")


if __name__ == "__main__":
    main()