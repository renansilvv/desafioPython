# Desafio Python + Supabase + Z-API

Script em Python que busca contatos cadastrados no Supabase e envia uma mensagem personalizada pelo WhatsApp usando a Z-API.

---

## Mensagem enviada

```txt
Olá, <nome> tudo bem com você?
```

---

## Tecnologias utilizadas

* Python
* Supabase
* Z-API
* Requests
* python-dotenv

---

## Estrutura da tabela no Supabase

A tabela usada no projeto se chama `contatos`.

Campos esperados:

| Campo      | Descrição                            |
| ---------- | ------------------------------------ |
| `id`       | Identificador do contato             |
| `nome`     | Nome usado na mensagem personalizada |
| `telefone` | Número de telefone do contato        |

Exemplo de criação da tabela:

```sql
create table contatos (
    id bigint generated always as identity primary key,
    nome text not null,
    telefone text not null,
    created_at timestamptz default now()
);
```

Exemplo de registros:

```sql
insert into contatos (nome, telefone)
values
    ('Nome1', '5511999999999'),
    ('Nome2', '5511988888888'),
    ('Nome3', '5511977777777');
```

O telefone pode ser salvo com ou sem máscara. O código remove caracteres que não são números antes do envio.

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`.

```env
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_TABLE=contatos

ZAPI_INSTANCE_ID=
ZAPI_INSTANCE_TOKEN=
ZAPI_CLIENT_TOKEN=

MAX_CONTATOS=3
```

---

## Como rodar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o script:

```bash
python main.py
```

---

## Observação

O script busca no máximo 3 contatos, conforme solicitado.