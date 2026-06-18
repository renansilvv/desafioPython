import logging
import os
import re

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE")

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

MAX_CONTATOS = min(int(os.getenv("MAX_CONTATOS", 3)), 3)


def checar_configuracoes():
    variaveis = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "SUPABASE_TABLE": SUPABASE_TABLE,
        "ZAPI_INSTANCE_ID": ZAPI_INSTANCE_ID,
        "ZAPI_INSTANCE_TOKEN": ZAPI_INSTANCE_TOKEN,
        "ZAPI_CLIENT_TOKEN": ZAPI_CLIENT_TOKEN,
    }

    faltando = [nome for nome, valor in variaveis.items() if not valor]

    if faltando:
        logging.error("Variáveis obrigatórias não definidas no .env: %s", ", ".join(faltando))
        exit(1)


def formatar_numero(numero):
    return re.sub(r"\D", "", numero or "")


def buscar_contatos():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    resposta = (
        supabase
        .table(SUPABASE_TABLE)
        .select("id,nome,telefone")
        .limit(MAX_CONTATOS)
        .execute()
    )

    return resposta.data or []


def enviar_mensagem(contato):
    nome = contato.get("nome")
    telefone = formatar_numero(contato.get("telefone", ""))

    if not nome or not telefone:
        logging.warning("Contato ignorado por não ter nome ou telefone: %s", contato)
        return

    mensagem = f"Olá, {nome} tudo bem com você?"

    url = (
        f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}"
        f"/token/{ZAPI_INSTANCE_TOKEN}/send-text"
    )

    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN,
        "Content-Type": "application/json",
    }

    payload = {
        "phone": telefone,
        "message": mensagem,
    }

    try:
        resposta = requests.post(url, headers=headers, json=payload, timeout=15)

        if resposta.ok:
            logging.info("Mensagem enviada para %s", telefone)
        else:
            logging.error(
                "Erro ao enviar para %s. Status: %s. Resposta: %s",
                telefone,
                resposta.status_code,
                resposta.text,
            )

    except requests.exceptions.RequestException as erro:
        logging.error("Erro na requisição para a Z-API: %s", erro)


def main():
    checar_configuracoes()

    contatos = buscar_contatos()

    if not contatos:
        logging.info("Nenhum contato encontrado")
        return

    logging.info("%s contato(s) encontrado(s)", len(contatos))

    for contato in contatos:
        enviar_mensagem(contato)


if __name__ == "__main__":
    main()
