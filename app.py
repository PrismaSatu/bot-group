import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('FF9CIVxmNSoQJ3B4Ux7nf3HscXu0IFpjcz7OzViePiqWEtzAj9TzeOOLu//2aZJcX795lvk4NdM/oDri7bXREzrtnb8Bl6xYXXG4RYmG1ocU5Eutmjo7nEpVcdYgePwKX1ZcBUJZmIy9J0s61vVpNwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1ccd1b7d54d856ea0ceb3bfad63ba95a')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
