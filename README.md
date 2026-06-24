# Assistente Virtual CredenciaPE - Streamlit + OpenRouter + Manual

Link: https://projeto-agente-de-ia-mucwnfknfb9vjq6fidyyba.streamlit.app/

Projeto de chatbot institucional para apoiar usuários do CredenciaPE/GESIG com respostas baseadas no manual carregado.

## O que vem pronto

- Interface Streamlit em tema azul institucional.
- Logos CredenciaPE e GESIG.
- Manual do CredenciaPE já convertido para busca por páginas.
- Integração com OpenRouter via REST usando `Authorization: Bearer`.
- Fallback local: se a API falhar, o app ainda busca trechos relacionados no manual.
- Diagnóstico na barra lateral mostrando se a chave foi detectada.

## Como rodar

Entre na pasta do projeto e rode:

```bash
pip install -r requirements.txt
python tools/testar_openrouter.py
streamlit run app.py
```

## Onde está a chave

A chave foi colocada em:

- `.env`
- `.streamlit/secrets.toml`

Depois dos testes, troque por uma chave nova se for subir ou entregar para alguém.

## Trocar a chave

Edite o arquivo `.env`:

```env
OPENROUTER_API_KEY=SUA_CHAVE_OPENROUTER_AQUI
OPENROUTER_MODEL=google/gemini-2.5-flash
```

Se usar Streamlit Cloud, edite também `.streamlit/secrets.toml` ou configure os secrets direto no painel.

## Teste rápido da API

```bash
python tools/testar_openrouter.py
```

Se aparecer `OK: OpenRouter funcionando.`, a chave está funcionando.

Se aparecer erro 401/403, confira a chave, créditos/cota do OpenRouter e o nome do modelo.

## Observação

O chatbot responde usando os trechos mais relacionados do manual. Quando a API não responde, ele entra em modo local e mostra os trechos encontrados no manual.
