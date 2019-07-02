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

'''@app.route("/", methods=['GET'])
def webhook():
    PushDis = GetMail()

    if PushDis == 10:
        user_id = "Ue8baeea0f29de588e397c74e7b3dcf31"

        messages = TextSendMessage(text="あと１０ｍ以下です！早めの補充を！")
        line_bot_api.push_message(user_id, messages=messages)

        messagesImage = ImageSendMessage(
            original_content_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182927.jpg",
            preview_image_url="https://cdn-ak.f.st-hatena.com/images/fotolife/h/hahayata/20190214/20190214182927.jpg"
        )
        line_bot_api.push_message(user_id, messages=messagesImage)'''

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
        if (event.message.text == "a"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=event.source.user_id)
                ]
            )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)