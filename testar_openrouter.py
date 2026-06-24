import json
import os
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"


def carregar_env():
    if not ENV_FILE.exists():
        return
    for linha in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        k, v = linha.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")


def main():
    carregar_env()
    key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
    model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash").strip()
    if not key or "SUA_CHAVE" in key or "COLE_SUA" in key:
        print("ERRO: configure OPENROUTER_API_KEY no arquivo .env.")
        return

    print("Chave detectada no .env/ambiente:", key[:8] + "..." + key[-4:] if len(key) > 12 else "configurada")
    print("Modelo:", model)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Responda apenas: OpenRouter funcionando."}],
        "temperature": 0.1,
        "max_tokens": 80,
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Assistente CredenciaPE",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        print("OK:", str(text).strip())
    except Exception as exc:
        print("ERRO AO CHAMAR OPENROUTER:", exc)
        print("Confira a chave, créditos/cota do OpenRouter, internet e o nome do modelo.")


if __name__ == "__main__":
    main()
