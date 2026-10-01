from flask import Flask, request, jsonify
import g4f, os
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

# SUAS CHAVES Z-API
ID_INSTANCIA = "3F9FD98A60CA5174C71F72533F9B1D1F"
TOKEN_INSTANCIA = "FB93981B97FCDBB3A2F48246"

def responder(msg):
    try:
        fuso = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(fuso).strftime('%H:%M')
        prompt = f"Voce e NEON 2.0 de Goiania, assistente brabo do chefe. Hora agora {agora}. Responda curto e direto: {msg}"
        client = g4f.client.Client()
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
        return r.choices[0].message.content
    except Exception as e:
        return f"To on Chefe! Erro: {e}"

@app.route("/")
def home():
    return "NEON 2.0 ONLINE 🔥"

@app.route("/webhook", methods=['POST'])
def zap():
    data = request.json
    try:
        telefone = data.get('phone')
        mensagem = data.get('text', {}).get('message')

        if not mensagem or not telefone:
            return jsonify({"status": "ignorado"})

        print(f"Mensagem de {telefone}: {mensagem}")

        resposta_ia = responder(mensagem)

        # Envia de volta pro Zap
        url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN_INSTANCIA}/send-text"
        payload = {"phone": telefone, "message": resposta_ia}
        requests.post(url, json=payload)

    except Exception as e:
        print(f"Erro webhook: {e}")

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
