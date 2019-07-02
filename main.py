from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)
import os

app = Flask(__name__)
app.debug = False

line_bot_api = LineBotApi("rSGR6J4mVY3fQ8SqrCZyjtAxqT9dynuIGC87wtEGcbwLzxSGDMY2/l8YRD3cqxOcYY9JReg5uvD2kfyGGUdYp9yTWuoxgzFtyI5avM71zqwdCf4HuskTzn31LKFdAGnOsgLIt4fItpr1wOmQj5HN7wdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("d03905b4dadc5f6292597c595f3df85e")

@app.route("/get_mail", methods=['POST'])
def get_jeson():
    group_id = "C84a3f6c8f5e45507cdc2b6759bf558ac"
    mail_body = request.form['body']

    messages = TextSendMessage(text=mail_body)
    line_bot_api.push_message(group_id, messages=messages)

@app.route("/test", methods=['GET'])
def test():
    group_id = "C84a3f6c8f5e45507cdc2b6759bf558ac"

    messages = TextSendMessage(text="テスト：GET通信：テスト成功")
    line_bot_api.push_message(group_id, messages=messages)

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
    if event.type == "message":
        if (event.message.text == "Check: GroupID"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=event.source.group_id)
                ]
            )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)