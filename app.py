from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# SUAS CHAVES DA Z-API - CONFERE SE ESTÃO NO RENDER EM ENVIRONMENT
INSTANCE_ID = os.getenv("INSTANCE_ID")
TOKEN = os.getenv("TOKEN")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN") # aquele token grande da aba Security

@app.route("/")
def home():
    return "NEON ONLINE - webhook em /webhook"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"CHEGOU: {data}") # ISSO TEM QUE APARECER NO LOG

    try:
        # Pega a mensagem que veio da Z-API
        phone = data.get("phone")
        message_text = data.get("text", {}).get("message") or data.get("message") or ""

        if not phone or not message_text:
            print("Sem phone ou mensagem")
            return jsonify({"status": "ignorado"}), 200

        # Ignora mensagem minha mesma
        if data.get("fromMe"):
            return jsonify({"status": "fromMe"}), 200

        # RESPOSTA SIMPLES PRA TESTAR (depois a gente coloca a IA)
        resposta = f"NEON RECEBEU: {message_text} 🚀"

        # Envia pela Z-API
        url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"
        payload = {
            "phone": phone,
            "message": resposta
        }
        headers = {
            "Content-Type": "application/json",
            "Client-Token": CLIENT_TOKEN
        }
        r = requests.post(url, json=payload, headers=headers)
        print(f"ENVIO Z-API: {r.text}")

    except Exception as e:
        print(f"ERRO: {e}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
