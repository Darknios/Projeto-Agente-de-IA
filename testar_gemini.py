import json
import os
import urllib.parse
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
    key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    if not key or "SUA_CHAVE" in key or "COLE_SUA" in key:
        print("ERRO: configure GEMINI_API_KEY no arquivo .env.")
        return

    if key.startswith("ya29."):
        print("ERRO: a credencial parece token OAuth/login, não API key do Gemini.")
        print("Cole no .env a chave copiada em Google AI Studio > API keys.")
        return

    print("Chave detectada no .env/ambiente:", key[:6] + "..." + key[-4:] if len(key) > 10 else "configurada")
    print("Modelo:", model)

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(model, safe='')}:generateContent"
    )
    payload = {
        "contents": [{"parts": [{"text": "Responda apenas: Gemini funcionando."}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 80},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        print("OK:", text.strip())
    except Exception as exc:
        print("ERRO AO CHAMAR GEMINI:", exc)
        print("Se aparecer 401/UNAUTHENTICATED, a chave ainda está inválida ou o projeto não tem acesso à Gemini API.")


if __name__ == "__main__":
    main()
