from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import g4f, os
from datetime import datetime
import pytz

app = Flask(__name__)

def responder(msg):
    try:
        fuso = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(fuso).strftime("%d/%m %H:%M Goiania")
        prompt = f"Voce e NEON 2.0 de Goiania, amiga do Chefe. Agora {agora}. Usuario: {msg}. Resposta curta PT-BR."
        client = g4f.client.Client()
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
        return r.choices[0].message.content
    except Exception as e:
        return f"To on Chefe! Erro: {e}"

@app.route("/")
def home():
    return "NEON 2.0 ONLINE"

@app.route("/whatsapp", methods=['POST'])
def zap():
    msg = request.values.get('Body','')
    txt = responder(msg)
    resp = MessagingResponse()
    resp.message(txt)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
