# Assistente Virtual CredenciaPE — Streamlit + Gemini + Manual

Projeto de chatbot institucional para apoiar usuários do CredenciaPE/GESIG com respostas baseadas no manual carregado.

## O que vem pronto

- Interface Streamlit em tema azul institucional.
- Logos CredenciaPE e GESIG.
- Manual do CredenciaPE já convertido para busca por páginas.
- Integração com Gemini API via REST usando `x-goog-api-key`.
- Fallback local: se a API falhar, o app ainda busca trechos relacionados no manual.
- Diagnóstico na barra lateral mostrando se a chave foi detectada.

## Como rodar

Entre na pasta do projeto e rode:

```bash
pip install -r requirements.txt
python tools/testar_gemini.py
streamlit run app.py
```

## Onde está a chave

A chave já foi colocada em:

- `.env`
- `.streamlit/secrets.toml`

Depois dos testes, troque por uma chave nova se for subir ou entregar para alguém.

## Trocar a chave

Edite o arquivo `.env`:

```env
GEMINI_API_KEY=SUA_CHAVE_NOVA_AQUI
GEMINI_MODEL=gemini-2.5-flash
```

Se usar Streamlit Cloud, edite também `.streamlit/secrets.toml` ou configure os secrets direto no painel.

## Teste rápido da API

```bash
python tools/testar_gemini.py
```

Se aparecer `OK: Gemini funcionando.`, a chave está funcionando.

Se aparecer 401/UNAUTHENTICATED, a chave não está válida para a Gemini API ou o projeto não tem acesso correto.

## Observação

O chatbot responde usando os trechos mais relacionados do manual. Quando a API não responde, ele entra em modo local e mostra os trechos encontrados no manual.
