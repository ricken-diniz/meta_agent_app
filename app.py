from flask import Flask, request
import requests

app = Flask(__name__)
url = "https://graph.facebook.com/v22.0/672955145891181/messages"

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
        headers = {
            "Authorization": "Bearer EAAJZBIGsvHmsBO08ZAZB0ZBD97opWnvGs7lxkZC9PzlYmxZAdF8i2cZBfb2uylZCbgKl8ZAYYxzmZBsqhtdCKcjX4LoX8WiCnsenHCQEsmgLnQfVp3WmVUxND4DoOZA2QMzBREOmLiE3lBMoU7CLujrvDtIAHeKTHbk7GSeRr37ND17PbrQdHER4epVw6SNKzdA9LLLG2I34dfnfnXvRHjnGWP7A0mHdPeU",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": "5584987794399",
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {"code": "en_US"}
            }
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
        data = request.json
        print("📩 Evento recebido:", data)
        return "OK", 200

@app.route('/', methods=["GET"])
def index():
    # if request:
        
        # headers = {
        #     "Authorization": "Bearer EAAJZBIGsvHmsBO08ZAZB0ZBD97opWnvGs7lxkZC9PzlYmxZAdF8i2cZBfb2uylZCbgKl8ZAYYxzmZBsqhtdCKcjX4LoX8WiCnsenHCQEsmgLnQfVp3WmVUxND4DoOZA2QMzBREOmLiE3lBMoU7CLujrvDtIAHeKTHbk7GSeRr37ND17PbrQdHER4epVw6SNKzdA9LLLG2I34dfnfnXvRHjnGWP7A0mHdPeU",
        #     "Content-Type": "application/json"
        # }
        # data = {
        #     "messaging_product": "whatsapp",
        #     "to": "5584987794399",
        #     "type": "template",
        #     "template": {
        #         "name": "hello_world",
        #         "language": {"code": "en_US"}
        #     }
        # }

        # response = requests.post(url, headers=headers, json=data)

        # print(response.status_code)
        # print(response.json())
    return "Webhook is running!", 200

if __name__ == "__main__":
    app.run()