# Assistente Virtual CredenciaPE - Streamlit + Gemini + Manual

Este projeto cria uma página em Streamlit para um chatbot institucional do CredenciaPE/GESIG.

A IA responde com base no manual incluído em `data/manual_credenciape_paginas.json`. O app primeiro busca os trechos relevantes do manual e depois, se houver chave Gemini configurada, envia esses trechos para o Gemini responder sem inventar informações.

## O que foi corrigido nesta versão

- O app agora lê arquivo `.env` automaticamente.
- O app aceita `GEMINI_API_KEY` ou `GOOGLE_API_KEY`.
- Removida dependência de chave fixa dentro do código.
- Se o pacote Gemini der erro, o app tenta chamar a API Gemini direto por REST.
- O modo local agora só fica como fallback quando não há chave, sem internet, chave inválida, cota estourada ou erro de API.
- Sidebar tem diagnóstico mostrando se a chave foi detectada.

## Como rodar

Abra o terminal dentro da pasta do projeto e execute:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como ativar o Gemini

### Opção 1 - arquivo `.env` dentro da pasta do projeto

Crie um arquivo chamado `.env` na mesma pasta do `app.py`:

```env
GEMINI_API_KEY=SUA_CHAVE_GEMINI_AQUI
GEMINI_MODEL=gemini-2.5-flash
```

Depois rode:

```bash
streamlit run app.py
```

### Opção 2 - variável de ambiente no Windows CMD

```cmd
setx GEMINI_API_KEY "SUA_CHAVE_GEMINI_AQUI"
setx GEMINI_MODEL "gemini-2.5-flash"
```

Feche e abra o terminal novamente. Depois rode:

```bash
streamlit run app.py
```

### Opção 3 - secrets do Streamlit

Copie o arquivo:

```txt
.streamlit/secrets.toml.example
```

para:

```txt
.streamlit/secrets.toml
```

E coloque sua chave real:

```toml
GEMINI_API_KEY = "SUA_CHAVE_GEMINI_AQUI"
GEMINI_MODEL = "gemini-2.5-flash"
```

## Como saber se o Gemini está ativo

Na barra lateral do app deve aparecer:

```txt
Chave detectada: xxxxxx...xxxx
```

Se aparecer “Sem chave Gemini”, o app continuará em modo local.

Se aparecer chave detectada, mas a resposta ainda cair no local, geralmente é um destes casos:

- chave inválida;
- API Gemini sem permissão;
- sem internet;
- cota gratuita estourada;
- modelo digitado errado;
- dependências não instaladas.

## Como funciona a resposta pelo manual

1. Usuário pergunta algo no chat.
2. O sistema busca os trechos mais parecidos dentro do manual.
3. Se a chave Gemini existir, o Gemini responde usando somente esses trechos.
4. Se não existir chave ou a API falhar, o app mostra resposta local com os trechos encontrados.
5. O usuário pode abrir o expander “Trechos do manual usados na resposta” para conferir a fonte.

## Como trocar o manual

Coloque o novo PDF em qualquer pasta e rode:

```bash
python tools/extrair_manual_pdf.py "caminho/do/novo_manual.pdf"
```

Depois rode novamente:

```bash
streamlit run app.py
```

## Arquivos principais

```txt
app.py
requirements.txt
assets/logo_credencia_pe.jpeg
assets/logo_gesig.jpeg
data/manual_credenciape.pdf
data/manual_credenciape_paginas.json
data/manual_credenciape.txt
tools/extrair_manual_pdf.py
.streamlit/secrets.toml.example
.env.example
```

## Observação importante

Este chatbot é uma ferramenta de apoio ao usuário. Se a informação não estiver no manual, o assistente deve dizer que não encontrou no documento e orientar o usuário a consultar o setor responsável.


## Chave Gemini já configurada

Este ZIP já vem com `.env` e `.streamlit/secrets.toml` configurados para teste local.
Depois da apresentação/teste, troque a chave e não suba esses arquivos para GitHub.

Para testar rapidamente:

```bash
python tools/testar_gemini.py
streamlit run app.py
```
