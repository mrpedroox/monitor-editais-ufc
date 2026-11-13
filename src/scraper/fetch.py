import requests

HEADERS = {"User-Agent": "monitor-editais-ufc (projeto de estudo)"}


def fetch_html(url: str, timeout: int = 15) -> str:
    resposta = requests.get(url, headers=HEADERS, timeout=timeout)
    resposta.raise_for_status()
    resposta.encoding = "utf-8"
    return resposta.text