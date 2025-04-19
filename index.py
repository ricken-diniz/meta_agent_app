from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = "meu_token_de_verificacao"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Erro de verificação", 403

    elif request.method == "POST":
        data = request.json
        print("📩 Evento recebido:", data)
        return "OK", 200

if __name__ == "__main__":
    app.run()